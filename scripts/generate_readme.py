

from pathlib import Path

ROOT = Path(".")
README_PATH = ROOT / "README.md"

LEVEL_DIRS = ["beginner", "intermediate", "advanced"]
IGNORE_DIRS = {".git", ".github", "__pycache__", ".venv", "venv", "node_modules"}

def parse_simple_yaml(file_path):
    data = {}
    if not file_path.exists():
        return data

    current_key = None
    for line in file_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if value:
                data[key] = value
                current_key = None
            else:
                data[key] = []
                current_key = key

        elif line.startswith("-") and current_key:
            data[current_key].append(line[1:].strip())

    return data


def format_status(status):
    mapping = {
        "planning": "⚪ Planning",
        "in progress": "🟡 In Progress",
        "done": "🟢 Completed"
    }
    return mapping.get(status.lower(), status)


def generate_structure():
    lines = ["```text", "ros2-project/"]

    for level in LEVEL_DIRS:
        level_path = ROOT / level
        if not level_path.exists():
            continue

        lines.append(f"└── {level}/")

        projects = sorted([p for p in level_path.iterdir() if p.is_dir()])

        for project in projects:
            lines.append(f"    └── {project.name}/")

    lines.append("```")
    return "\n".join(lines)


def generate_projects():
    lines = []

    for level in LEVEL_DIRS:
        level_path = ROOT / level
        if not level_path.exists():
            continue

        projects = sorted([p for p in level_path.iterdir() if p.is_dir()])
        if not projects:
            continue

        lines.append(f"### {level.capitalize()}")
        lines.append("")
        lines.append("| Project | Description | Status | Tags |")
        lines.append("|--------|-------------|-------|------|")

        for project in projects:
            meta = parse_simple_yaml(project / "project.yaml")

            desc = meta.get("description", "")
            status = format_status(meta.get("status", "planning"))
            tags = ", ".join(meta.get("tags", []))

            link = f"[{project.name}]({level}/{project.name})"

            lines.append(
                f"| {link} | {desc} | {status} | {tags} |"
            )

        lines.append("")

    return "\n".join(lines)


def generate_progress():
    lines = []
    lines.append("| Stage | Progress |")
    lines.append("|------|---------|")

    for level in LEVEL_DIRS:
        level_path = ROOT / level

        if not level_path.exists():
            lines.append(f"| {level.capitalize()} | ⚪ 0 projects |")
            continue

        projects = sorted([p for p in level_path.iterdir() if p.is_dir()])
        count = len(projects)

        if count == 0:
            icon = "⚪"
        else:
            icon = "🟡"

        lines.append(f"| {level.capitalize()} | {icon} {count} projects |")

    return "\n".join(lines)


def replace_section(content, start, end, body):
    s = content.find(start)
    e = content.find(end)

    if s == -1 or e == -1:
        return content

    s += len(start)

    return content[:s] + "\n" + body + "\n" + content[e:]


def main():

    content = README_PATH.read_text(encoding="utf-8")

    structure = generate_structure()
    projects = generate_projects()
    progress = generate_progress()

    content = replace_section(
        content,
        "<!-- AUTO-PROGRESS-START -->",
        "<!-- AUTO-PROGRESS-END -->",
        progress
    )

    content = replace_section(
        content,
        "<!-- AUTO-STRUCTURE-START -->",
        "<!-- AUTO-STRUCTURE-END -->",
        structure
    )

    content = replace_section(
        content,
        "<!-- AUTO-PROJECTS-START -->",
        "<!-- AUTO-PROJECTS-END -->",
        projects
    )

    README_PATH.write_text(content, encoding="utf-8")
    print("README updated")


if __name__ == "__main__":
    main()
