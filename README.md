# 🤖 Agentic Workflow with LangGraph, Cohere & Streamlit

This project implements an **agentic workflow system** that uses LangGraph to coordinate a PlanAgent and a ToolAgent. The system can break down a user query, plan executable tasks using a Cohere LLM, execute those tasks (e.g., math computations, AI news scraping), and present results through a **Streamlit-based interactive UI**.

---

## 🚀 Features

- **Agentic Reasoning**: Uses Cohere to plan step-by-step tasks from any complex query.
- **Task Execution Engine**: Executes real-world tasks such as:
  - 📐 Square root calculation
  - 📰 AI news scraping from VentureBeat
  - 🧠 Insight extraction
  - 📝 Summary generation
- **Feedback Loop**: Determines whether the agent should continue based on execution results.
- **Streamlit UI**: Interactive frontend to input queries and view results in real time.

---

## 🧠 Workflow Architecture

```text
[User Query] ➝ [PlanAgent (Cohere)] ➝ [ToolAgent (Executes Tasks)] ➝ [Returns Results]
                                       ↳ Optional Feedback Loop
````

---

## 📦 Requirements

Install the required packages using:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```txt
cohere
langchain
langgraph
python-dotenv
streamlit
requests
beautifulsoup4
```

---

## 🗂️ Project Structure

```
.
├── agentic_graph.py       # LangGraph agentic workflow logic
├── tool_agent.py          # Executes real-world tasks
├── main.py                # Entry point to run the agent
├── streamlit_app.py       # Streamlit UI to interact with the agent
├── .env                   # Your API keys (e.g., COHERE_API_KEY)
└── requirements.txt       # Python dependencies
```

---

## 🛠️ Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/SanthiNani/agentic-workflow-langgraph.git
   cd agentic-workflow-langgraph
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file with your Cohere API Key:**

   ```
   COHERE_API_KEY=your-cohere-api-key
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run streamlit_app.py
   ```

---

## 💡 Example Query

> **Query:** Calculate the square root of 169
> ✅ Output: The square root of 169 is 13.

> **Query:** Search AI news and summarize findings
> ✅ Output: Scrapes VentureBeat, extracts top headlines, insights, and generates a summary.

---

## 📸 Demo Screenshot

![Screenshot 2025-05-26 163837](https://github.com/user-attachments/assets/0d2c89f9-6635-4ec4-943f-2e95d20a4c05)


---

## ✨ Future Enhancements

* Integrate tools like WolframAlpha, OpenAI Functions, or SerpAPI.
* Add memory to store past plans and results.
* Voice input and speech synthesis output.

---

## 📄 License

MIT License.
Feel free to fork, contribute, or extend this project.

---

## 🙌 Acknowledgements

* [LangGraph by LangChain](https://github.com/langchain-ai/langgraph)
* [Cohere AI](https://cohere.com/)
* [Streamlit](https://streamlit.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---
