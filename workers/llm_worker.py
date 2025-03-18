import openai

from orchestrator import CodeGenState


def generate_project_structure(state: CodeGenState) -> CodeGenState:
    """Uses LLM to generate project folder structure and file content."""
    
    user_stories = "\n".join(state.user_stories)
    prompt = f"""
    Given these user stories:
    {user_stories}

    Generate a JSON-like structure of the folder hierarchy with filenames and their corresponding content.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a software architect."},
                  {"role": "user", "content": prompt}]
    )

    project_structure = response["choices"][0]["message"]["content"]
    
    # Convert response to a dictionary (LLM should return JSON format)
    import json
    project_structure = json.loads(project_structure)

    state.project_structure = project_structure
    return state
