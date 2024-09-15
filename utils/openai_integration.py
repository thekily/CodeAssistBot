import os
import json
import logging
import re
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)

def generate_plan(prompt, file_tree):
    """
    Generate a plan based on the user's prompt and the repository file tree.
    Returns a JSON response with the plan.
    """
    try:
        logger.info(f"Generating plan with prompt: {prompt}")
        logger.info(f"File tree: {json.dumps(file_tree, indent=2)}")

        context = f"Repository structure: {json.dumps(file_tree)}\n\nUser prompt: {prompt}\n\n"
        request = context + "Based on the repository structure and the user's prompt, generate a detailed plan of steps to implement the requested functionality. Each step should specify which files need to be created or modified and provide a high-level description of the changes. Return the response as a JSON object with a 'steps' key containing an array of step objects. Each step object should have 'description' and 'files' keys."
        
        logger.info(f"Constructed context: {context}")
        logger.info(f"Constructed request: {request}")

        logger.info("Calling OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request}],
            max_tokens=500
        )
        
        logger.info(f"Raw OpenAI API response: {response}")

        # Extract JSON from the response using regex
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response.choices[0].message.content)
        if json_match:
            plan_json_str = json_match.group(1)
        else:
            plan_json_str = response.choices[0].message.content

        logger.info(f"Extracted plan JSON string: {plan_json_str}")

        # Parse the extracted JSON
        plan_json = json.loads(plan_json_str)
        logger.info(f"Parsed plan JSON: {plan_json}")

        return json.dumps(plan_json)
    except Exception as e:
        logger.error(f"Error generating plan: {str(e)}", exc_info=True)
        raise Exception(f"Error generating plan: {str(e)}")

def execute_plan(plan, repo_path):
    """
    Execute the plan by generating code modifications for each step.
    Returns a JSON response with the execution results.
    """
    try:
        plan_obj = json.loads(plan)
        context = f"Repository path: {repo_path}\n\nPlan: {json.dumps(plan_obj)}\n\n"
        request = context + "For each step in the plan, provide the exact code modifications or new file contents. Return the response as a JSON object with a 'steps' key containing an array of step objects. Each step object should have 'description', 'file_path', and 'content' keys."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request}],
            max_tokens=1000
        )
        
        # Parse the response content as JSON
        execution_json = json.loads(response.choices[0].message.content)
        return json.dumps(execution_json)
    except Exception as e:
        logger.error(f"Error executing plan: {str(e)}", exc_info=True)
        raise Exception(f"Error executing plan: {str(e)}")
