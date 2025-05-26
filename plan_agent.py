import cohere
import re
from dotenv import load_dotenv
import os

load_dotenv()

class PlanAgent:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set in environment variables")
        self.client = cohere.Client(api_key)

    def plan(self, user_input):
        prompt = f"""
Decompose the following query into a numbered list of detailed, actionable tasks.

Query: {user_input}
Tasks:
1."""
        try:
            # Use cohere chat endpoint with the prompt
            response = self.client.chat(message=prompt, model="command-r")
            # Extract text from response
            output_text = getattr(response, "text", None) or response.generations[0].text
            output_text = output_text.strip()
        except Exception as e:
            return {
                "query": user_input,
                "tasks": [],
                "results": [f"Error calling Cohere API: {str(e)}"],
                "should_continue": False,
            }

        # Extract numbered tasks with regex
        tasks = re.findall(r"\d+\.\s+(.*)", output_text)
        tasks = [task.strip() for task in tasks if task.strip()]

        # Mark all tasks as executed placeholder
        results = [f"Executed: {task}" for task in tasks]

        return {
            "query": user_input,
            "tasks": tasks,
            "results": results,
            "should_continue": False,
        }
