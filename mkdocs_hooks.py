from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
ALERT_KIND_MAP = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "info",
    "WARNING": "warning",
    "CAUTION": "danger",
}


def _source_path_for(src_uri: str) -> Path | None:
    normalized = src_uri.replace("\\", "/")
    if normalized == "readme.md":
        return ROOT / "README.md"
    if normalized.startswith("subtopics/"):
        candidate = ROOT / normalized
        if candidate.exists():
            return candidate
    return None


def _strip_level_two_sections(markdown: str, headings: set[str]) -> str:
    lines = markdown.splitlines()
    stripped: list[str] = []
    skip_section = False

    for line in lines:
        heading_match = re.match(r"##\s+(.*)", line)
        if heading_match:
            current_heading = heading_match.group(1).strip()
            skip_section = current_heading in headings
            if skip_section:
                continue

        if not skip_section:
            stripped.append(line)

    if markdown.endswith("\n"):
        return "\n".join(stripped) + "\n"
    return "\n".join(stripped)


def _convert_github_alerts(markdown: str) -> str:
    lines = markdown.splitlines()
    converted: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        match = re.match(r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)", line)
        if not match:
            converted.append(line)
            index += 1
            continue

        alert_kind = ALERT_KIND_MAP[match.group(1)]
        body_lines = []
        first_line = match.group(2).strip()
        if first_line:
            body_lines.append(first_line)

        index += 1
        while index < len(lines) and lines[index].startswith(">"):
            quoted_line = lines[index][1:]
            if quoted_line.startswith(" "):
                quoted_line = quoted_line[1:]
            body_lines.append(quoted_line)
            index += 1

        converted.append(f"!!! {alert_kind}")
        if not body_lines:
            converted.append("    ")
            continue

        for body_line in body_lines:
            converted.append(f"    {body_line}" if body_line else "    ")

    if markdown.endswith("\n"):
        return "\n".join(converted) + "\n"
    return "\n".join(converted)


def on_page_read_source(page, config):
    source_path = _source_path_for(page.file.src_uri)
    if source_path is None:
        return None

    markdown = source_path.read_text(encoding="utf-8")
    if source_path.name == "README.md":
        markdown = _convert_github_alerts(markdown)
        markdown = _strip_level_two_sections(markdown, {"Table of Contents", "Local Docs"})
    return markdown
