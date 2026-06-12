#!/usr/bin/env python3
"""Verify .pyi stubs are in sync with .pyx source after upstream rebase.

Usage:
    uv run python scripts/verify_stubs.py           # full check
    uv run python scripts/verify_stubs.py --diff     # only check .pyx changed since last rebase
    uv run python scripts/verify_stubs.py --update   # update baseline with current scores
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_FILE = Path(__file__).resolve().parent / ".stubs-baseline.json"

# Modules with hand-written stubs
STUBBED_MODULES = [
    "nautilus_trader.model.objects",
    "nautilus_trader.model.data",
    "nautilus_trader.model.identifiers",
    "nautilus_trader.trading.strategy",
    "nautilus_trader.core.correctness",
]


def run_pyright_verifytypes(module: str) -> dict:
    result = subprocess.run(
        ["pyright", "--verifytypes", module],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    output = result.stdout

    score = 0.0
    exported_known = 0
    exported_total = 0
    in_exported_section = False

    for line in output.splitlines():
        if line.startswith("Type completeness score:"):
            score = float(line.split(":")[1].strip().rstrip("%"))
        if line.startswith("Symbols exported"):
            in_exported_section = True
            parts = line.split(":")
            if len(parts) >= 2:
                exported_total = int(parts[-1].strip())
        elif line.startswith("Other symbols referenced"):
            in_exported_section = False
        if in_exported_section and "With known type:" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                exported_known = int(parts[-1].strip())

    return {
        "score": score,
        "exported_known": exported_known,
        "exported_total": exported_total,
    }


def get_changed_pyx_files() -> list[str]:
    """Find .pyx files changed since the merge-base with upstream."""
    try:
        merge_base = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/master"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        ).stdout.strip()

        if not merge_base:
            return []

        diff = subprocess.run(
            ["git", "diff", "--name-only", merge_base, "HEAD", "--", "*.pyx"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        return [f for f in diff.stdout.strip().splitlines() if f]
    except Exception:
        return []


def get_stub_for_pyx(pyx_path: str) -> str | None:
    """Map a .pyx path to its stubbed module name."""
    path = Path(pyx_path)
    parts = list(path.parts)

    if "nautilus_trader" not in parts:
        return None

    idx = parts.index("nautilus_trader")
    module_parts = parts[idx:]
    module_parts[-1] = module_parts[-1].replace(".pyx", "")
    return ".".join(module_parts)


def main():
    if not shutil.which("pyright"):
        print("[FAIL] pyright not found. Install: npm install -g pyright")
        sys.exit(1)

    args = sys.argv[1:]
    diff_mode = "--diff" in args
    update_mode = "--update" in args

    # Load baseline
    baseline = {}
    if BASELINE_FILE.exists():
        baseline = json.loads(BASELINE_FILE.read_text())

    results = {}
    issues = []

    # Determine which modules to check
    if diff_mode:
        changed_pyx = get_changed_pyx_files()
        if not changed_pyx:
            print("No .pyx files changed since last rebase. All good.")
            sys.exit(0)

        print(f"Changed .pyx files ({len(changed_pyx)}):")
        for f in changed_pyx:
            print(f"  {f}")
        print()

        modules_to_check = set()
        for pyx in changed_pyx:
            mod = get_stub_for_pyx(pyx)
            if mod and mod in STUBBED_MODULES:
                modules_to_check.add(mod)
            elif mod:
                print(f"  WARNING: {pyx} has no stub (not in STUBBED_MODULES)")

        if not modules_to_check:
            print("No stubbed modules affected. All good.")
            sys.exit(0)
    else:
        modules_to_check = set(STUBBED_MODULES)

    print(f"Checking {len(modules_to_check)} stubbed modules...\n")

    for module in sorted(modules_to_check):
        info = run_pyright_verifytypes(module)
        results[module] = info

        prev = baseline.get(module, {})
        prev_score = prev.get("score", 0)

        status = "OK"
        if info["score"] < prev_score - 5:
            status = "REGRESSION"
            issues.append(
                f"  {module}: {prev_score:.1f}% -> {info['score']:.1f}% "
                f"(was {prev.get('exported_known', '?')} known / {prev.get('exported_total', '?')} total, "
                f"now {info['exported_known']} / {info['exported_total']})"
            )
        elif info["score"] < 50:
            status = "LOW"
            issues.append(f"  {module}: {info['score']:.1f}% (below 50% threshold)")

        symbol = "OK" if status == "OK" else "!!"
        print(f"  [{symbol}] {module}: {info['score']:.1f}% ({info['exported_known']}/{info['exported_total']} known)")

    if update_mode:
        BASELINE_FILE.write_text(json.dumps(results, indent=2) + "\n")
        print(f"\nBaseline updated: {BASELINE_FILE}")

    if issues:
        print(f"\n{'='*60}")
        print(f"ISSUES ({len(issues)}):")
        for issue in issues:
            print(issue)
        print(f"\nAction required:")
        print(f"  1. Review changed .pyx files listed above")
        print(f"  2. Update .pyi stubs in nautilus_trader/")
        print(f"  3. Run: uv run python scripts/verify_stubs.py --update")
        sys.exit(1)
    else:
        print("\nAll stubs healthy.")


if __name__ == "__main__":
    main()
