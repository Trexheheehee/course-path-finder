import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Available Gemini Models")

api_key = os.getenv("GEMINI_API_KEY")

# Allow manual entry if env var is missing
if not api_key or api_key == "your_api_key_here":
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

if api_key:
    genai.configure(api_key=api_key)
    st.write("Fetching models...")
    try:
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name)
                found_any = True
        
        if not found_any:
            st.warning("No models found that support generateContent.")
            
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please provide an API Key.")
