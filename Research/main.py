from orchestrator import orchestrator_workflow

def main():
    user_stories = [
        "As a user, I want to register an account so that I can access my profile.",
        "As an admin, I want to manage users so that I can control access."
    ]

    print("Starting LLM-Orchestrator Workflow...")
    
    # Run workflow
    final_state = orchestrator_workflow.invoke({"user_stories": user_stories})

    print("Workflow Completed!")
    print(f"Generated Project Path: /GeneratedApp")

    # Print Generated Structure
    import json
    print(json.dumps(final_state["generated_files"], indent=4))

if __name__ == "__main__":
    main()
