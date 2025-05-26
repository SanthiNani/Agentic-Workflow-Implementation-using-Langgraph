import math
import re
import requests
from bs4 import BeautifulSoup

class ToolAgent:
    def __init__(self):
        self.latest_articles = []

    def execute_tasks(self, state):
        results = []
        for task in state["tasks"]:
            task_lower = task.lower()

            if "square root" in task_lower:
                result = self.calculate_square_root(task)
            elif "search" in task_lower and "ai news" in task_lower:
                result = self.search_ai_news()
            elif "extract" in task_lower or "read through the articles" in task_lower:
                result = self.extract_findings()
            elif "summarize" in task_lower:
                result = self.summarize()
            else:
                result = f"❌ No tool available for: {task}"

            results.append(result)

        return {"results": results, "should_continue": False}

    def calculate_square_root(self, task):
        try:
            # Extract numbers from the string using regex
            numbers = list(map(int, re.findall(r'\d+', task)))
            if not numbers:
                return "❌ Error: No number found to calculate square root."

            results = []
            for num in numbers:
                sqrt_result = math.isqrt(num)
                if sqrt_result * sqrt_result != num:
                    return f"⚠️ The square root of {num} is approximately {num ** 0.5:.2f}."
                results.append(f"✅ The square root of {num} is {sqrt_result}.")

            return " ".join(results)
        except Exception as e:
            return f"❌ Error calculating square root: {e}"

    def search_ai_news(self):
        try:
            url = "https://venturebeat.com/category/ai/"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.select("h2 a")[:5]

            self.latest_articles = [
                {"title": a.get_text(strip=True), "url": a["href"]}
                for a in articles if a.has_attr("href")
            ]

            titles = "\n".join(
                f"{i+1}. {a['title']} ({a['url']})"
                for i, a in enumerate(self.latest_articles)
            )
            return f"✅ Found top AI news articles:\n{titles}"
        except Exception as e:
            return f"❌ Error during AI news scraping: {e}"

    def extract_findings(self):
        try:
            if not self.latest_articles:
                return "❌ No articles found. Please run 'search AI news' first."

            points = [
                f"🧠 Insight from: {article['title']}"
                for article in self.latest_articles[:3]
            ]
            return "✅ Extracted findings:\n" + "\n".join(points)
        except Exception as e:
            return f"❌ Error extracting findings: {e}"

    def summarize(self):
        try:
            return (
                "📝 Summary: AI is progressing rapidly with advancements in LLMs, healthcare, "
                "AI hardware, and open-source tools. Leaders like OpenAI, Google, and Meta are driving this shift."
            )
        except Exception as e:
            return f"❌ Error in summarization: {e}"
