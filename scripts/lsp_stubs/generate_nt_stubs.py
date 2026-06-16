"""
One-shot orchestrator: patch stubgen-pyx -> generate -> self-contained -> place.

Generates self-contained .pyi stubs for NT Cython modules so pyright/LSP can
resolve them (bare .pyx/.so are invisible to pyright). Run after NT version
upgrade, rebase upstream, or when a covered module changes.

This script only orchestrates three independent CLIs (no cross-imports, so
pyright stays clean):
  1. patch_stubgen_pyx.py   — ensure stubgen-pyx collects `cdef readonly`
  2. stubgen-pyx            — read .pyx -> raw .pyi (types/sigs/attrs/docstrings)
  3. make_self_contained.py — Any-ify cross-Cython, normalize typing aliases,
                              cpython->stdlib, None-default Optional

Usage:
  uv run python scripts/lsp_stubs/generate_nt_stubs.py <pyx_relpath> [<pyx_relpath> ...]
  e.g. uv run python scripts/lsp_stubs/generate_nt_stubs.py nautilus_trader/cache/cache.pyx
"""
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SD = ROOT / "scripts" / "lsp_stubs"


def _run(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=ROOT)  # noqa: S603 - trusted: fixed CLI + user-supplied pyx paths


def main(pyx_rels: list[str]) -> int:
    _run("uv", "run", "python", str(SD / "patch_stubgen_pyx.py"), str(ROOT / ".venv"))

    for pyx_rel in pyx_rels:
        pyx = ROOT / pyx_rel
        print(f">>> {pyx_rel}")
        with tempfile.NamedTemporaryFile(suffix=".pyi", delete=False) as tmp:
            raw = Path(tmp.name)
        try:
            _run(
                "uv", "run", "stubgen-pyx", str(pyx.parent), "--file", pyx.name,
                "--output-file", str(raw), "--continue-on-error",
            )
            dst = pyx.with_suffix(".pyi")
            _run("uv", "run", "python", str(SD / "make_self_contained.py"), str(raw), str(dst))
            print(f"[DONE] {pyx_rel} -> {dst.relative_to(ROOT)}")
        finally:
            raw.unlink(missing_ok=True)

    print("Restart Claude Code (or reload window) for LSP to pick up changed stubs.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
