from pathlib import Path

from check_links import find_broken_links


def write(root: Path, rel: str, text: str = "") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def test_ok_relative_link(tmp_path):
    write(tmp_path, "a.md", "[b](b.md)")
    write(tmp_path, "b.md")
    assert find_broken_links(tmp_path) == []


def test_broken_link_reported(tmp_path):
    write(tmp_path, "a.md", "see [x](missing.md)")
    assert find_broken_links(tmp_path) == [(tmp_path / "a.md", "missing.md")]


def test_anchor_and_line_range_stripped(tmp_path):
    write(tmp_path, "a.md", "[code](x.py#L1-L3) and [setup](b.md#setup)")
    write(tmp_path, "x.py")
    write(tmp_path, "b.md")
    assert find_broken_links(tmp_path) == []


def test_external_and_anchor_only_ignored(tmp_path):
    write(tmp_path, "a.md", "[w](https://x.org) [m](mailto:a@b.c) [t](#top)")
    assert find_broken_links(tmp_path) == []


def test_links_in_code_fence_ignored(tmp_path):
    write(tmp_path, "a.md", "```\n[x](nope.md)\n```\nand `[y](nope2.md)` inline")
    assert find_broken_links(tmp_path) == []


def test_skips_dot_claude_dir(tmp_path):
    write(tmp_path, ".claude/s/SKILL.md", "[x](nope.md)")
    assert find_broken_links(tmp_path) == []


def test_llms_txt_scanned(tmp_path):
    write(tmp_path, "llms.txt", "- [Page](missing.md): note")
    assert find_broken_links(tmp_path) == [(tmp_path / "llms.txt", "missing.md")]


def test_folder_link_and_root_relative(tmp_path):
    write(tmp_path, "docs/a.md", "[ex](../examples/) [root](/README.md) [img](pic%20one.png)")
    write(tmp_path, "examples/x.py")
    write(tmp_path, "README.md")
    write(tmp_path, "docs/pic one.png")
    assert find_broken_links(tmp_path) == []
