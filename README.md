# LLM Chat App

This is a local LLM-powered chat application built with Streamlit and Ollama. It supports both conversational interaction and document summarization.

## Features

-   **Conversational Chat:** Chat with a local LLM (e.g., Mistral, LLaMA).
-   **Document Summarization:** Upload PDF, Word, or text files to get a concise summary.
-   **Follow-up Questions:** Ask follow-up questions based on the summarized document.

## Prerequisites

-   Python 3.7+
-   Ollama installed and running. You can download it from [https://ollama.ai/](https://ollama.ai/).
-   A running Ollama model (e.g., `ollama run mistral`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/llm-chat-app.git
    cd llm-chat-app
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  **Open your browser:**
    The app will open in your default web browser.

3.  **Choose the app mode:**
    -   **Conversational Chat:** Start chatting with the LLM.
    -   **Document Summarization:** Upload a document to get a summary and ask follow-up questions.
