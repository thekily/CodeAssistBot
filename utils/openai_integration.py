import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_plan(prompt, file_tree):
    """
    Generate a plan based on the user's prompt and the repository file tree.
    """
    try:
        context = f"Repository structure: {file_tree}\n\nUser prompt: {prompt}\n\n"
        request = context + "Based on the repository structure and the user's prompt, generate a detailed plan of steps to implement the requested functionality. Each step should specify which files need to be created or modified and provide a high-level description of the changes."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating plan: {str(e)}")

def execute_plan(plan, repo_path):
    """
    Execute the plan by generating code modifications for each step.
    """
    try:
        context = f"Repository path: {repo_path}\n\nPlan: {plan}\n\n"
        request = context + "For each step in the plan, provide the exact code modifications or new file contents. Specify the full file path for each modification."
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error executing plan: {str(e)}")
