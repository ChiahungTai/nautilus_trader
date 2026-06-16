"""
Apply the local `cdef readonly` patch to stubgen-pyx in a venv.

Why this exists
---------------
stubgen-pyx (v0.2.14) collects only `cdef public` class attributes and skips
`cdef readonly` (see stubgen_pyx/analysis/visitor.py visit_CVarDefNode). NT's
convention is `cdef readonly` for Python-readable attributes (e.g.
`indicator.value`, `cache.has_backing`), so unpatched stubs miss the
attributes downstream reads most. This flips the collector to accept both
`public` and `readonly`.

Properties
----------
- Idempotent: detects already-patched and skips.
- Version-aware: warns if the expected source pattern is absent (e.g. a
  future stubgen-pyx release fixed this upstream, or restructured the file).
- Venv-flexible: pass a venv path; defaults to `.venv`.

Run after `uv sync` / `uv pip install stubgen-pyx`.

Usage: uv run python scripts/lsp_stubs/patch_stubgen_pyx.py [venv_path]
"""
import sys
from pathlib import Path


OLD = 'if self.in_class and visibility == "public":'
NEW = 'if self.in_class and visibility in ("public", "readonly"):'


def find_visitor(venv: Path) -> Path | None:
    candidates = list(venv.glob("lib/python*/site-packages/stubgen_pyx/analysis/visitor.py"))
    return candidates[0] if candidates else None


def main(venv_str: str = ".venv") -> int:
    venv = Path(venv_str)
    visitor = find_visitor(venv)
    if visitor is None:
        print(f"[FAIL] stubgen_pyx/analysis/visitor.py not found under {venv}")
        print("       is stubgen-pyx installed in this venv?")
        return 1

    text = visitor.read_text()
    if NEW in text:
        print(f"[SKIP] already patched: {visitor}")
        return 0
    if OLD not in text:
        print(f"[WARN] expected pattern not found: {visitor}")
        print("       stubgen-pyx may have changed (fixed upstream? restructured?).")
        print("       Inspect visit_CVarDefNode manually before regenerating stubs.")
        return 1

    visitor.write_text(text.replace(OLD, NEW, 1))
    print(f"[OK] patched readonly support: {visitor}")
    return 0


if __name__ == "__main__":
    venv_arg = sys.argv[1] if len(sys.argv) > 1 else ".venv"
    sys.exit(main(venv_arg))
