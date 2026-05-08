import streamlit as st
import json
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("AI Application Compiler")

user_input = st.text_input("Enter your app idea")

if st.button("Generate"):

    prompt = f"""
    Return ONLY valid JSON.

    {{
      "ui": {{"pages": []}},
      "api": {{"routes": []}},
      "db": {{"tables": []}},
      "auth": {{"roles": []}}
    }}

    USER INPUT:
    {user_input}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    start = content.find("{")
    end = content.rfind("}") + 1

    clean_json = content[start:end]

    result = json.loads(clean_json)

    st.json(result)
