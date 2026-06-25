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
        # __init__ always returns None; stubgen-pyx omits the annotation when the
        # .pyx declares no return type, tripping downstream disallow_untyped_calls.
        if node.name == "__init__" and node.returns is None:
            node.returns = ast.Constant(value=None)
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


def _pyi_exports(pyi_path: Path) -> set[str]:
    """Top-level names a .pyi exports (classes, functions, assignments)."""
    try:
        tree = ast.parse(pyi_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
    return names


def _merge_typing_and_drop_imports(
    tree: ast.Module, preserved_imports: dict[str, list[ast.alias]]
) -> None:
    """
    Drop nautilus_trader imports (cross-Cython, unresolvable to pyright); merge
    all typing imports into one line, normalizing away asnames (e.g. stubgen-pyx
    emits `Any as _Any`, which would leave the bare `Any` name we emit
    undefined); rewrite cpython.* to stdlib.

    Exception: same-package .pyi imports in ``preserved_imports`` are KEPT, but
    re-emitted with ONLY the symbols the target .pyi actually exports. Symbols
    the target doesn't export stay dropped (Any-ified), avoiding pyright `unknown
    import symbol` on incomplete hand-written stubs.
    """
    typing_names: set[str] = set()
    kept: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("nautilus_trader"):
                pres = preserved_imports.get(node.module)
                if pres:
                    kept.append(
                        ast.ImportFrom(module=node.module, names=pres, level=0)
                    )
                continue  # drop other nautilus_trader (cross-Cython) imports
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


def _same_package_pyi_exports(tree: ast.Module, dst: Path) -> dict[str, set[str]]:
    """
    For each nautilus_trader import module that is same-package with ``dst`` AND
    has a co-located .pyi, return {module: set of exported symbol names}.

    Only exported symbols are preserveable; this handles incomplete hand-written
    stubs (e.g. model/data.pyi doesn't re-export OrderBookDepth10 that book.pyx
    cimports) — unexported symbols stay Any instead of producing pyright `unknown
    import symbol`.
    """
    # nt_root = the .../nautilus_trader package dir, at any stub depth
    # (stubs live 2 levels deep like cache/cache.pyi, or 3+ like model/orders/market.pyi).
    nt_root = next((p for p in dst.parents if p.name == "nautilus_trader"), None)
    if nt_root is None:
        return {}
    try:
        dst_pkg_rel = dst.parent.relative_to(nt_root)  # Path("cache") or Path("model/orders")
    except ValueError:
        return {}

    out: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.startswith("nautilus_trader.")
        ):
            continue
        mod_rel = node.module.removeprefix("nautilus_trader.")  # e.g. cache.base
        mod_pkg = mod_rel.rsplit(".", 1)[0] if "." in mod_rel else ""  # cache / model.orders
        if Path(*mod_pkg.split(".")) != dst_pkg_rel:
            continue  # not same package (compare as Path: dot-form vs slash-form)
        mod_path = nt_root.joinpath(*mod_rel.split(".")).with_suffix(".pyi")
        if mod_path.exists():
            out[node.module] = _pyi_exports(mod_path)
    return out


def make_self_contained(src: str, dst: str) -> int:
    tree = ast.parse(Path(src).read_text(encoding="utf-8"))

    dst_path = Path(dst)
    same_pkg_exports = _same_package_pyi_exports(tree, dst_path)
    preserved_imports: dict[str, list[ast.alias]] = {}

    cross: set[str] = set()
    typing_aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("nautilus_trader"):
                exports = same_pkg_exports.get(node.module)
                if exports is None:
                    for alias in node.names:
                        cross.add(alias.asname or alias.name)
                else:
                    # preserve only symbols the target .pyi exports; Any-ify the rest
                    for alias in node.names:
                        if alias.name in exports:
                            preserved_imports.setdefault(node.module, []).append(alias)
                        else:
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
    _merge_typing_and_drop_imports(tree, preserved_imports)
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
