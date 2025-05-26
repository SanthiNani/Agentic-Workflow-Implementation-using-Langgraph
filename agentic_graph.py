import os
import re
import cohere
import math
import requests
from bs4 import BeautifulSoup
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()

# PlanAgent uses Cohere to break down queries into tasks
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
        response = self.client.chat(message=prompt, model="command-r")
        output_text = response.text.strip() if hasattr(response, "text") else response.generations[0].text.strip()
        tasks = re.findall(r"\d+\.\s+(.*)", output_text)
        return {"tasks": [task.strip() for task in tasks if task.strip()]}

# ToolAgent executes tasks intelligently based on keywords in the tasks
class ToolAgent:
    def __init__(self):
        self.latest_articles = []

    def execute_tasks(self, state):
       results = []
       for task in state["tasks"]:
          task_lower = task.lower()

          if "square root" in task_lower:
             results.append(self.calculate_square_root(task))  # FIXED
          elif "search" in task_lower and "ai news" in task_lower:
             results.append(self.search_ai_news())
          elif "extract" in task_lower or "read through the articles" in task_lower:
             results.append(self.extract_findings())
          elif "summarize" in task_lower:
             results.append(self.summarize())
          else:
             results.append(f"❌ No tool available for: {task}")

       return {"results": results, "should_continue": False}


    def calculate_square_root(self, task):
        try:
            number = [int(s) for s in task.split() if s.isdigit()]
            if not number:
                return "Error: No number found to calculate square root."
            sqrt_result = math.isqrt(number[0])
            return f"The square root of {number[0]} is {sqrt_result}."
        except Exception as e:
            return f"Error calculating square root: {e}"

    def search_ai_news(self):
        try:
            url = "https://venturebeat.com/category/ai/"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.select("h2 a")[:5]  # safer selector for titles with links
            self.latest_articles = [
                {"title": a.get_text(strip=True), "url": a["href"]}
                for a in articles if a.has_attr("href")
            ]
            titles = "\n".join(f"{i+1}. {a['title']} ({a['url']})" for i, a in enumerate(self.latest_articles))
            return f"Found top AI news articles:\n{titles}"
        except Exception as e:
            return f"Error during AI news scraping: {e}"

    def extract_findings(self):
        try:
            if not self.latest_articles:
                return "No articles found. Please run 'search AI news' first."
            points = []
            for article in self.latest_articles[:3]:
                points.append(f"Insight from: {article['title']}")
            return "Extracted findings:\n" + "\n".join(points)
        except Exception as e:
            return f"Error extracting findings: {e}"

    def summarize(self):
        try:
            return (
                "Summary: AI is progressing rapidly with advancements in large language models, "
                "healthcare diagnostics, AI hardware, and open-source research. Key players like OpenAI, "
                "Google, and Meta are driving innovation across multiple domains."
            )
        except Exception as e:
            return f"Error in summarization: {e}"

# Initialize agents
planner = PlanAgent()
executor = ToolAgent()

# Define the Agent state dictionary
class AgentState(dict):
    query: str
    tasks: list
    results: list
    should_continue: bool

# Workflow nodes
def plan_node(state):
    plan_output = planner.plan(state["query"])
    # Reset results on new planning
    return {**state, **plan_output, "results": [], "should_continue": True}

def tool_node(state):
    tool_output = executor.execute_tasks(state)
    # Append new results to any existing results
    combined_results = state.get("results", []) + tool_output.get("results", [])
    return {**state, "results": combined_results, "should_continue": tool_output["should_continue"]}

# Define workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("plan", RunnableLambda(plan_node))
workflow.add_node("tool", RunnableLambda(tool_node))
workflow.set_entry_point("plan")
workflow.add_edge("plan", "tool")
workflow.add_conditional_edges("tool", lambda state: END if not state["should_continue"] else "tool")

graph = workflow.compile()
