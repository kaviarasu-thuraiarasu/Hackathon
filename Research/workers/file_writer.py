import os

from orchestrator import CodeGenState


def write_files_to_disk(state: CodeGenState) -> CodeGenState:
    """Creates folders and writes files based on LLM output."""

    project_name = "GeneratedApp"
    base_path = os.path.join(os.getcwd(), project_name)

    project_structure = state.project_structure

    for folder, files in project_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file_name, content in files.items():
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as f:
                f.write(content)

    state.generated_files = project_structure
    return state
