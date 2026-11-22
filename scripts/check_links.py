"""Find relative links in *.md and llms.txt that point to files that don't exist.

Usage: python3 scripts/check_links.py [root]
External links (http, https, mailto) are not checked, so this works offline.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SKIP_DIRS = {".git", ".claude", "node_modules", ".superpowers"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def _files(root: Path):
    for p in [*root.rglob("*.md"), *root.rglob("llms.txt")]:
        if not SKIP_DIRS & set(p.relative_to(root).parts):
            yield p


def find_broken_links(root: Path) -> list[tuple[Path, str]]:
    root = Path(root)
    broken = []
    for file in sorted(_files(root)):
        text = INLINE_CODE.sub("", FENCE.sub("", file.read_text(encoding="utf-8")))
        for target in LINK.findall(text):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            path = unquote(target.split("#")[0].split("?")[0])
            resolved = root / path.lstrip("/") if path.startswith("/") else file.parent / path
            if not resolved.exists():
                broken.append((file, target))
    return broken


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    broken = find_broken_links(root)
    for file, target in broken:
        print(f"{file.relative_to(root)}: {target}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
