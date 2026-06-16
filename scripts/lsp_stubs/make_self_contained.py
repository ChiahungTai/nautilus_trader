"""
Post-process stubgen-pyx output to be NT-self-contained and pyright-clean.

Four transformations:
1. Cross-Cython type symbols (imported from nautilus_trader.*) -> Any, and
   those ImportFrom lines dropped. NT stub constraint: never import another
   Cython module (the whole chain is .pyx, pyright cannot resolve).
2. typing asname aliases (e.g. `Any as _Any`) normalized: the merged typing
   import drops asnames, and all `_Any` usages rewritten to `Any`.
3. CPython-internal imports (cpython.*) rewritten to their stdlib names
   (cpython.datetime -> datetime), which pyright can resolve.
4. Parameters with a None default but a concrete annotation get ``| None``
   (stubgen-pyx emits ``x: set = None``; pyright wants ``set | None = None``).

Usage: python make_self_contained.py <input.pyi> <output.pyi>
"""
import ast
import sys
from pathlib import Path


def _is_any(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id == "Any"


def _is_already_optional(node: ast.AST) -> bool:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return any(
            isinstance(s, ast.Name) and s.id == "None" for s in (node.left, node.right)
        )
    return False


def _collapse_ellipsis(annotation: ast.expr) -> ast.expr:
    """
    stubgen-pyx trims undefined names to ``...``; in a type annotation the
    Ellipsis is invalid (e.g. ``... | None``) -> replace with Any.
    """
    if isinstance(annotation, ast.Constant) and annotation.value is ...:
        return ast.copy_location(ast.Name(id="Any", ctx=ast.Load()), annotation)
    if isinstance(annotation, ast.BinOp):
        annotation.left = _collapse_ellipsis(annotation.left)
        annotation.right = _collapse_ellipsis(annotation.right)
    return annotation


def _collapse_ellipsis_annotations(tree: ast.Module) -> None:
    """Apply _collapse_ellipsis to all annotations (arg/return/AnnAssign)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.arg) and node.annotation is not None:
            node.annotation = _collapse_ellipsis(node.annotation)
        elif isinstance(node, ast.FunctionDef) and node.returns is not None:
            node.returns = _collapse_ellipsis(node.returns)
        elif isinstance(node, ast.AnnAssign) and node.annotation is not None:
            node.annotation = _collapse_ellipsis(node.annotation)


class SelfContainedTransformer(ast.NodeTransformer):
    def __init__(self, cross: set[str], typing_aliases: dict[str, str]):
        self.cross = cross
        self.typing_aliases = typing_aliases

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id in self.cross:
            return ast.copy_location(ast.Name(id="Any", ctx=node.ctx), node)
        if node.id in self.typing_aliases:
            return ast.copy_location(
                ast.Name(id=self.typing_aliases[node.id], ctx=node.ctx), node
            )
        if node.id == "callable":
            return ast.copy_location(ast.Name(id="Callable", ctx=node.ctx), node)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        """
        Cross-Cython symbol's attribute access (e.g. ``AccountType.CASH``)
        is unresolvable to pyright -> collapse the whole chain to Any.
        """
        self.generic_visit(node)
        if isinstance(node.value, ast.Name) and node.value.id == "Any":
            return ast.copy_location(ast.Name(id="Any", ctx=node.ctx), node)
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        """
        Cross-Cython class instantiation (e.g. ``Price('0.00001')``) is
        unresolvable -> collapse the whole call to a bare Any.
        """
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == "Any":
            return ast.copy_location(ast.Name(id="Any", ctx=ast.Load()), node)
        return node

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        """
        stubgen-pyx trims undefined names to ``...``; in a type union like
        ``... | None`` the Ellipsis is invalid -> replace with Any.
        """
        self.generic_visit(node)
        for attr in ("left", "right"):
            operand = getattr(node, attr)
            if isinstance(operand, ast.Constant) and operand.value is ...:
                setattr(
                    node,
                    attr,
                    ast.copy_location(ast.Name(id="Any", ctx=ast.Load()), operand),
                )
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self.generic_visit(node)
        args = node.args
        positional = list(args.posonlyargs) + list(args.args)
        n_defaultless = len(positional) - len(args.defaults)
        for i, arg in enumerate(positional):
            if i < n_defaultless:
                continue
            j = i - n_defaultless
            default = args.defaults[j]
            self._maybe_optional(arg, default)
            if isinstance(default, ast.Name) and default.id == "Any":
                args.defaults[j] = ast.copy_location(ast.Constant(value=...), default)
        for i, arg in enumerate(args.kwonlyargs):
            default = args.kw_defaults[i]
            if default is not None:
                self._maybe_optional(arg, default)
                if isinstance(default, ast.Name) and default.id == "Any":
                    args.kw_defaults[i] = ast.copy_location(ast.Constant(value=...), default)
        return node

    def _maybe_optional(self, arg: ast.arg, default: ast.AST) -> None:
        ann = arg.annotation
        if ann is None or _is_any(ann) or _is_already_optional(ann):
            return
        if isinstance(default, ast.Constant) and default.value is None:
            arg.annotation = ast.BinOp(
                left=ann, op=ast.BitOr(), right=ast.Name(id="None", ctx=ast.Load())
            )


def _merge_typing_and_drop_imports(tree: ast.Module) -> None:
    """
    Drop nautilus_trader imports; merge all typing imports into one line,
    normalizing away asnames (e.g. stubgen-pyx emits `Any as _Any`, which would
    leave the bare `Any` name we emit undefined); rewrite cpython.* to stdlib.
    """
    typing_names: set[str] = set()
    kept: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("nautilus_trader"):
                continue
            node.module = node.module.removeprefix("cpython.")
            if node.module == "typing":
                for alias in node.names:
                    typing_names.add(alias.name)
                continue
        kept.append(node)

    typing_names.add("Any")
    typing_names.add("Callable")
    typing_import = ast.ImportFrom(
        module="typing", names=[ast.alias(n) for n in sorted(typing_names)], level=0
    )
    tree.body = [typing_import, *kept]


def make_self_contained(src: str, dst: str) -> int:
    tree = ast.parse(Path(src).read_text(encoding="utf-8"))

    cross: set[str] = set()
    typing_aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("nautilus_trader"):
                for alias in node.names:
                    cross.add(alias.asname or alias.name)
            elif node.module == "typing":
                for alias in node.names:
                    if alias.asname:
                        typing_aliases[alias.asname] = alias.name

    SelfContainedTransformer(cross, typing_aliases).visit(tree)
    ast.fix_missing_locations(tree)
    # Collapse Ellipsis (stubgen-pyx undefined-name trim) in all annotations —
    # the transformer's visit_BinOp doesn't reach arg.annotation in the visit chain.
    _collapse_ellipsis_annotations(tree)
    ast.fix_missing_locations(tree)
    _merge_typing_and_drop_imports(tree)
    ast.fix_missing_locations(tree)

    header = "# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)\n"
    Path(dst).write_text(header + ast.unparse(tree), encoding="utf-8")

    return len(cross)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_self_contained.py <input.pyi> <output.pyi>")
        sys.exit(2)
    n = make_self_contained(sys.argv[1], sys.argv[2])
    print(f"[OK] {sys.argv[1]} -> {sys.argv[2]} ({n} cross-symbols -> Any)")
