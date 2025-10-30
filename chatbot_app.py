# from dotenv import load_dotenv
# load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

import streamlit as st
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


# Sidebar UI (New chat, Search, Chat list)
with st.sidebar:
    st.header("📚 Menu")
    st.button("🆕 New Chat")
    st.button("📖 Library")
    st.button("🔍 Search Chats")

st.title("KoolGamer Chatbot App")

if "messsages" not in st.session_state:
    st.session_state.messages = []

check_pointer = InMemorySaver()

agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    checkpointer=check_pointer,
    prompt="You are a helpful assistant"
)

def stream_graph_updates(user_input : str):
    assistant_response = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
    for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": "def"}}):
        for value in event.values():
            new_text = value["messages"][-1].content
            assistant_response += new_text
            message_placeholder.markdown(assistant_response)
    
    st.session_state.messages.append(("assistant", assistant_response))

    # Display previous chat history
for role, message in st.session_state.messages:
   with st.chat_message(role):
       st.markdown(message)

prompt = st.chat_input("Ask Anything")
if prompt:

    # Display user input as a chat message
   with st.chat_message("user"):
       st.markdown(prompt)

 # Append user input to session state
   st.session_state.messages.append(("user", prompt))

#  Get response from the chatbot based on user input
   response = stream_graph_updates(prompt)


