import os

# Path to the beginner folder
directory = 'beginner'

# Initialize a list to hold project details
projects = []

# Walk through the directory for project files
for root, dirs, files in os.walk(directory):
    for file in files:
        # Only consider .py files and ignore __init__.py
        if file.endswith('.py') and file != '__init__.py':
            # Extract project name and path
            project_name = os.path.splitext(file)[0]
            project_path = os.path.join(root, file)
            projects.append((project_name, project_path))

# Generate README content
readme_content = '# Dynamic README for ROS2 Project\n\n'
readme_content += '## Project Structure\n\n'
readme_content += '```
'
for project, path in projects:
    readme_content += f'- {project}: {path}\n'
readme_content += '```
\n'
readme_content += '## List of Projects\n'
for project, _ in projects:
    readme_content += f'- {project}\n'

# Write README to a file
def write_readme(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

write_readme('README.md', readme_content)
