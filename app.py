
import streamlit as st
from document_processor import get_text_from_file
from llm import get_conversational_response, summarize_text
import os
import time
import json
import re

# --- Constants ---
CHAT_HISTORY_FILE = "chat_history.json"

# --- UI Configuration ---
st.set_page_config(page_title="LLM Chat App", page_icon=":robot_face:", layout="wide")



# --- Helper Functions ---
def load_chat_history():
    """Loads chat history from a JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_chat_history(messages):
    """Saves chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=4)

def clear_chat_history():
    """Clears the chat history from session state and deletes the history file."""
    st.session_state.messages = []
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)

def format_response_to_sentences(response_text):
    """Formats a block of text into separate sentences, each on a new line."""
    sentences = re.split(r'(?<=[.!?])\s+', response_text)
    return "\n".join(sentence.strip() for sentence in sentences if sentence.strip())

# --- Temp Directory ---
if not os.path.exists("temp"):
    os.makedirs("temp")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()
if "document_summary" not in st.session_state:
    st.session_state.document_summary = ""

# --- Sidebar ---
st.sidebar.title("LLM Chat App")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Conversational Chat", "Document Summarization"])

if st.sidebar.button("New Chat"):
    clear_chat_history()
    st.rerun()

# --- Main App ---
if app_mode == "Conversational Chat":
    st.header("Conversational Chat")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_chat_history(st.session_state.messages)
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            # Get response from LLM
            assistant_response = get_conversational_response(prompt)
            
            # Format the response
            formatted_response = format_response_to_sentences(assistant_response)

            # Simulate stream of response (we'll stream the whole formatted block)
            full_response_display = ""
            for chunk in formatted_response.split():
                full_response_display += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response_display + "▌")
            message_placeholder.markdown(formatted_response)

        # Add the formatted assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        save_chat_history(st.session_state.messages)

elif app_mode == "Document Summarization":
    st.header("Document Summarization")

    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        file_path = os.path.join("temp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text from the document
        text = get_text_from_file(file_path)

        if "Error" not in text:
            st.text_area("Extracted Text", text, height=300)

            if st.button("Summarize"):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(text)
                    # Format the summary
                    formatted_summary = format_response_to_sentences(summary)
                    st.session_state.document_summary = formatted_summary
                    st.success("Summarization complete!")
                    st.text_area("Summary", formatted_summary, height=200, key="summary_output")
        else:
            st.error(text)

        # Clean up the temporary file
        os.remove(file_path)

    if st.session_state.document_summary:
        st.text_area("Summary", st.session_state.document_summary, height=200, key="summary_display")
        if prompt := st.chat_input("Ask a follow-up question about the document"):
            context = f"Based on the following document summary:\n{st.session_state.document_summary}\n\n{prompt}"
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = get_conversational_response(context)
                formatted_response = format_response_to_sentences(response)
                st.markdown(formatted_response)
