import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Course Roadmap Generator",
    page_icon="📚",
    layout="centered"
)

# --- Sidebar / Configuration ---
with st.sidebar:
    st.header("Configuration")
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check if the key is missing or is the default placeholder from the .env file
    if not api_key or api_key == "your_api_key_here":
        api_key = st.text_input("Enter Gemini API Key", type="password")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
    
    if not os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") == "your_api_key_here":
         st.warning("⚠️ Please enter your API key to proceed.")

    
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit & Gemini")

# --- Main Logic ---

def generate_roadmap(skill, level, duration):
    """
    Generates a learning roadmap using Google Gemini.
    """
    try:
        # Configure the API
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # Using gemini-1.5-pro as requested
        model = genai.GenerativeModel("gemini-2.5-flash")

        
        # Construct the prompt
        prompt = f"""
        You are an expert curriculum designer.
        Create a {duration} learning roadmap for {skill}
        for a {level} learner.

        For each week include:
        - Topics
        - Tools or resources
        - Practical outcome

        Format clearly by week using Markdown.
        Keep it concise and practical.
        """
        
        with st.spinner("Generating your personalized roadmap..."):
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI Layout ---

st.title("📚 Course Roadmap Generator")
st.markdown("Generate a structured learning path for any skill in seconds.")

# Input Section
col1, col2 = st.columns(2)

with col1:
    skill_input = st.text_input("Skill or Topic to Learn", placeholder="e.g. Python, Digital Marketing")

with col2:
    level_input = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])

duration_input = st.selectbox("Duration", ["4 weeks", "8 weeks", "12 weeks"])

generate_btn = st.button("Generate Roadmap", type="primary")

# Result Section
if generate_btn:
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please provide a Gemini API Key in the sidebar or environment variables.")
    elif not skill_input:
        st.warning("Please enter a skill or topic.")
    else:
        roadmap = generate_roadmap(skill_input, level_input, duration_input)
        if roadmap.startswith("Error"):
            st.error(roadmap)
        else:
            st.success("Roadmap generated successfully!")
            st.markdown("---")
            st.markdown(roadmap)
