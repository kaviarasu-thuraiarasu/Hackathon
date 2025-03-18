from nuverlan.llm.model import model
def generate_comprehensive_spec(user_stories):

    combined_spec_prompt = """
    You are an expert system architect and technical writer. Based on the following user stories, generate a comprehensive specification document, including the following components:
    1. **Functional Design**: Describe how the features described in the user stories will function from a user’s perspective.
    2. **Technical Design**: Provide the technical architecture, including the technology stack, authentication methods, and database schema.
    3. **Architecture Diagram**: Provide a detailed text description of the system architecture, which can be used to generate a diagram. The system should include:
    - **Frontend (Client)**: What technologies are used to build the frontend (e.g., React.js, Angular, etc.).
    - **Backend (Server)**: What backend technology is used (e.g., Node.js, Django, Flask, etc.), and how the system will handle authentication (e.g., JWT or OAuth).
    - **Database**: Describe the database choice and how it stores user data (e.g., PostgreSQL, MySQL).
    - **Authentication Service**: Describe how authentication will be managed (e.g., using JWT tokens or OAuth).
    - **Data Flow**: Explain how data moves through the system.
    - **Admin Management**: How will admins interact with the system?

    Please ensure that the generated content is comprehensive and clear. Provide details about the functional and technical aspects of the system design and how all components interact.

    User Stories:
    {user_stories}

    Functional Design and Technical Design are mandatory. Also, provide a diagram of the system architecture that can be used to create a diagram.
    Give me the responsei in fancy PDF format
    """
    prompt = combined_spec_prompt.format(
    user_stories="\n".join([f"- {story}" for story in user_stories])
    )
 
    response = model().process().invoke(prompt)
    return response.content
