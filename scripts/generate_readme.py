from pathlib import Path
import re

ROOT = Path(".")
README_PATH = ROOT / "README.md"

LEVEL_DIRS = ["beginner", "intermediate", "advanced", "projects"]
IGNORE_DIRS = {".git", ".github", "__pycache__", ".venv", "venv", "node_modules"}

def build_tree(path: Path, prefix=""):
    entries = sorted(
        [p for p in path.iterdir() if p.name not in IGNORE_DIRS],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    lines = []
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))
    return lines

def parse_simple_yaml(file_path: Path):
    data = {}
    if not file_path.exists():
        return data

    current_key = None
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue

        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = value
                current_key = None
            else:
                data[key] = []
                current_key = key
        elif line.strip().startswith("- ") and current_key:
            data[current_key].append(line.strip()[2:].strip())

    return data

def generate_structure_section():
    lines = ["```text", "ros2-project/"]
    for level in LEVEL_DIRS:
        level_path = ROOT / level
        if level_path.exists():
            lines.append(f"├── {level}/" if level != LEVEL_DIRS[-1] else f"└── {level}/")
            projects = sorted([p for p in level_path.iterdir() if p.is_dir() and p.name not in IGNORE_DIRS])
            for idx, project in enumerate(projects):
                is_last_level = (level == LEVEL_DIRS[-1])
                is_last_project = (idx == len(projects) - 1)
                if is_last_level:
                    prefix = "    "
                else:
                    prefix = "│   "
                branch = "└── " if is_last_project else "├── "
                lines.append(f"{prefix}{branch}{project.name}/")
        else:
            lines.append(f"├── {level}/" if level != LEVEL_DIRS[-1] else f"└── {level}/")
    lines.append("```")
    return "\n".join(lines)

def generate_projects_section():
    lines = []
    for level in LEVEL_DIRS:
        level_path = ROOT / level
        lines.append(f"### {level.capitalize()}")
        if not level_path.exists():
            lines.append("- 아직 프로젝트가 없습니다.\n")
            continue

        projects = sorted([p for p in level_path.iterdir() if p.is_dir() and p.name not in IGNORE_DIRS])

        if not projects:
            lines.append("- 아직 프로젝트가 없습니다.\n")
            continue

        for project in projects:
            meta = parse_simple_yaml(project / "project.yaml")

            lines.append(f"#### {project.name}")
            title = meta.get("title", project.name)
            description = meta.get("description", "설명이 아직 없습니다.")
            status = meta.get("status", "unknown")
            tags = meta.get("tags", [])

            lines.append(f"- **Title**: {title}")
            lines.append(f"- **Description**: {description}")
            lines.append(f"- **Status**: {status}")
            if tags:
                lines.append(f"- **Tags**: {', '.join(tags)}")
            lines.append("")
    return "\n".join(lines).strip()

def replace_section(content, start_marker, end_marker, new_body):
    start = content.find(start_marker)
    end = content.find(end_marker)

    if start == -1 or end == -1 or start > end:
        return content

    start += len(start_marker)
    return content[:start] + "\n" + new_body + "\n" + content[end:]

def main():
    if not README_PATH.exists():
        README_PATH.write_text(
            "# ROS2 Project\n\n"
            "## Auto-generated Structure\n\n"
            "<!-- AUTO-STRUCTURE-START -->\n"
            "<!-- AUTO-STRUCTURE-END -->\n\n"
            "## Auto-generated Project Summary\n\n"
            "<!-- AUTO-PROJECTS-START -->\n"
            "<!-- AUTO-PROJECTS-END -->\n",
            encoding="utf-8"
        )

    content = README_PATH.read_text(encoding="utf-8")

    structure_body = generate_structure_section()
    projects_body = generate_projects_section()

    content = replace_section(
        content,
        "<!-- AUTO-STRUCTURE-START -->",
        "<!-- AUTO-STRUCTURE-END -->",
        structure_body
    )

    content = replace_section(
        content,
        "<!-- AUTO-PROJECTS-START -->",
        "<!-- AUTO-PROJECTS-END -->",
        projects_body
    )
    print("STRUCTURE BODY:")
    print(structure_body)
    print("PROJECTS BODY:")
    print(projects_body)
    
    README_PATH.write_text(content, encoding="utf-8")
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()

