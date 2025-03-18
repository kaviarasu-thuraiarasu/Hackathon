import openai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_openai import ChatOpenAI
# OpenAI API Key (Replace with your key)
OPENAI_API_KEY = "" # os.getenv("OPENAI_API_KEY")

# Function to generate documentation using LLM
def generate_documentation(app_name):
    prompt = f"Generate a detailed software documentation for an application named '{app_name}'. It should include Overview, Features, User Stories, API Documentation, Database Schema, Installation Guide, Usage Guide, FAQs, and Troubleshooting."
    
    response = ChatOpenAI(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a technical writer."},
                  {"role": "user", "content": prompt}],openai_api_key=OPENAI_API_KEY,stream=True)
    #  response = openai.ChatCompletion.create(
    #    model="gpt-4",
    #     messages=[{"role": "system", "content": "You are a technical writer."},
    #               {"role": "user", "content": prompt}],
    #     api_key=OPENAI_API_KEY
    # )
    print(response[-1].content)
    
    return response[-1].content

# Function to save documentation to PDF
def save_to_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    
    y_position = height - 40
    for line in content.split("\n"):
        c.drawString(50, y_position, line)
        y_position -= 20  # Move down for the next line

    c.save()
    print(f"PDF '{filename}' generated successfully!")

# Example Usage
app_name = "ProjectX"
doc_content = generate_documentation(app_name)
save_to_pdf("ProjectX_Documentation.pdf", doc_content)
