import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()   # loads .env for local development

def get_secret(key):
    try:
        return st.secrets[key]     # works when deployed on Streamlit Cloud
    except Exception:
        return os.getenv(key)      # works locally, reading from .env

st.title("Nepal Travel Assistant")

api_key = get_secret("GEMINI_API_KEY")

model = "gemini-3.6-flash"

user_text = st.text_input(
    "Text to extract from:",
    "Ram Thapa runs a trekking shop in Pokhara."
)

if st.button("Run"):
    if not api_key:
        st.error("No API key found. Check your .env file (local) or Secrets (deployed).")
        st.stop()

    client = genai.Client(api_key=api_key)

    messages = [
        {"role": "system", "content": "You are a terse travel assistant for Nepal."},
        {"role": "user",   "content": f'Extract the name and city. Respond with JSON only.\nText: "{user_text}"'},
    ]

    system_prompt = next(m["content"] for m in messages if m["role"] == "system")
    user_prompt = next(m["content"] for m in messages if m["role"] == "user")

    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
    )

    st.write("**User prompt sent:**")
    st.code(user_prompt)

    st.write("**Model response:**")
    st.write(response.text)