import streamlit as st
from agentic_graph import graph, AgentState
import json  # import json to use json.dumps

st.title("🧠 Agentic Workflow Demo")

user_query = st.text_input("Enter your query")

if st.button("Run Workflow") and user_query:
    initial_state = AgentState(query=user_query)
    final_state = graph.invoke(initial_state)

    st.subheader("Final Output")
    # Use json.dumps to convert dict to JSON string, then display it as text or st.json for dict directly
    st.json({
        "query": final_state["query"],
        "tasks": final_state["tasks"],
        "results": final_state["results"],
        "should_continue": final_state["should_continue"]
    })
