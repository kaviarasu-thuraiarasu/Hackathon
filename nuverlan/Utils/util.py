from nuverlan.llm.model import model
import os
from pathlib import Path
import json

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





def generate_and_save_code(response):
   
    # code, path_filename = response.strip().split("\n\nPath: ")
    # path, filename = path_filename.split("\nFilename: ")
    # path = path.replace("`","")
    # filename = filename.replace("`","")
    # print("Path **************",path)
    # print("filename **************",filename)
   
    #osDir = Path(path+filename)
    lines = response.splitlines()
    file_list = []

    # if lines[0].startswith("```") and lines[-1].startswith("```"):
    #     cleaned_code = "\n".join(lines[1:-1])  # Exclude the first and last lines
    # else:
    #     cleaned_code = response  # No changes if backticks are not present
    print("**************PRE-PROCESSING*****************")
    if lines[0].startswith("["):
        #response = lines
        print("==============IF===============")
    else:
        response = response.split("[\n  {")[1]
        response = "[\n  {" + response
        response = response.split("\n```")[0]
    
    
    # print(response)
    data = json.loads((response))
    print(type(data))
    for dir in data:
       
        directory = dir['filePath']
        if dir['filePath'][-1]=="/":
            ...
        else:
            dir['filePath'] = dir['filePath']+"/"

        directory = dir['filePath']

        if "." in directory:
            directory = directory.rsplit('/', 1)[0]
            filePath = "E:/AgenticAI/Hackathon/Output/"+directory
        else:
            filePath= "E:/AgenticAI/Hackathon/Output/"+directory + dir["fileName"]

        os.makedirs("E:/AgenticAI/Hackathon/Output/"+ os.path.dirname(directory), exist_ok=True)
        
        with open(filePath, 'w') as file:
            file.write(dir['code'])
            file_list.append(filePath)
    
    return file_list


def generate_folder(template):
   
    code, path_filename = template.strip().split("\n\nPath: ")
    path, filename = path_filename.split("\nFilename: ")
    path = path.replace("`","")
    filename = filename.replace("`","")
    print("Path **************",path)
    print("filename **************",filename)
   
    osDir = Path(path+filename)
    lines = code.splitlines()

    if lines[0].startswith("```") and lines[-1].startswith("```"):
        cleaned_code = "\n".join(lines[1:-1])  # Exclude the first and last lines
    else:
        cleaned_code = code  # No changes if backticks are not present

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(osDir, 'w') as file:
        file.write(cleaned_code)
    
    return path, filename,osDir


