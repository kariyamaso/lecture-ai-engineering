# frontend/app.py
import streamlit as st
import requests
import json

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/generate" # URL of your FastAPI backend

# --- Page Setup ---
st.set_page_config(
    page_title="AI Code Assistant (FastAPI)",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🤖 AI Code Generation Assistant (FastAPI Backend)")
st.write("Enter a natural language description, and the AI will generate code.")
st.markdown("---")

# --- Custom CSS for Dark Theme ---
st.markdown("""
<style>
body {
    color: #E0E0E0;
    background-color: #1E1E1E;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}
input, textarea, select {
    background-color: #2A2A2A !important;
    color: #E0E0E0 !important;
    border: 1px solid #555 !important;
}
textarea {
     font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
}
button {
    background-color: #3C3C3C !important;
    color: #E0E0E0 !important;
    border: 1px solid #555 !important;
    transition: background-color 0.2s ease;
}
button:hover {
    background-color: #555555 !important;
}
pre, code {
    background-color: #282C34 !important;
    color: #ABB2BF !important;
    border-radius: 4px;
    padding: 0.5em !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #00AACC;
}
</style>
""", unsafe_allow_html=True)

# --- Main Application Area ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter your code description:")
    prompt_input = st.text_area(
        "Prompt",
        height=300,
        placeholder="e.g., 'Create a Python function that sums two numbers'",
        label_visibility="collapsed"
    )
    generate_button = st.button("✨ Generate Code")

with col2:
    st.subheader("Generated Code:")
    code_display_area = st.empty() # Placeholder for the code output

# --- Button Click Logic ---
if generate_button and prompt_input:
    with st.spinner("Generating code via FastAPI backend..."):
        try:
            payload = {"prompt": prompt_input}
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            generated_code = result.get("generated_code", "Error: Could not parse response.")
            code_display_area.code(generated_code, language="python") # Assume python for now

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
            code_display_area.error(f"Could not connect to the FastAPI backend at {BACKEND_URL}. Is it running?")
        except json.JSONDecodeError:
            st.error("Error decoding response from backend.")
            code_display_area.error("Received an invalid response from the backend.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            code_display_area.error(f"An error occurred: {e}")
elif generate_button and not prompt_input:
    st.warning("Please enter a description first.")
    code_display_area.info("Waiting for prompt...")
else:
     # Initial state or after clearing
     code_display_area.info("Enter a prompt and click 'Generate Code'.")
