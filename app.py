import streamlit as st
import os
import json
from dotenv import load_dotenv
from groq import Groq

# -------------------------
# LOAD ENV
# -------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------
# INTENT EXTRACTION
# -------------------------
def extract_intent(user_input):

    prompt = f"""
    Return ONLY valid JSON.

    {{
      "app_name": "",
      "features": []
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

    return json.loads(clean_json)

# -------------------------
# SYSTEM GENERATION
# -------------------------
def generate_system(intent):

    prompt = f"""
    Return ONLY valid JSON.

    {{
      "ui": {{
        "pages": []
      }},
      "api": {{
        "routes": []
      }},
      "db": {{
        "tables": []
      }},
      "auth": {{
        "roles": []
      }}
    }}

    INTENT:
    {intent}
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

    return json.loads(clean_json)

# -------------------------
# VALIDATION
# -------------------------
def validate(system):

    errors = []

    required = ["ui", "api", "db", "auth"]

    for item in required:
        if item not in system:
            errors.append(f"Missing {item}")

    return errors

# -------------------------
# REPAIR
# -------------------------
def repair(system, errors):

    for error in errors:

        if "Missing ui" in error:
            system["ui"] = {"pages": []}

        if "Missing api" in error:
            system["api"] = {"routes": []}

        if "Missing db" in error:
            system["db"] = {"tables": []}

        if "Missing auth" in error:
            system["auth"] = {"roles": []}

    return system

# -------------------------
# STREAMLIT UI
# -------------------------
st.title("AI Application Compiler")

st.write(
    "Convert natural language ideas into structured application architecture."
)

user_input = st.text_input("Enter your app idea")

if st.button("Generate"):

    # STEP 1
    st.subheader("1. Intent Extraction")
    intent = extract_intent(user_input)
    st.json(intent)

    # STEP 2
    st.subheader("2. System Generation")
    system = generate_system(intent)
    st.json(system)

    # STEP 3
    st.subheader("3. Validation")
    errors = validate(system)

    if errors:
        st.error(errors)

        # STEP 4
        st.subheader("4. Repair")
        system = repair(system, errors)

        st.success("System repaired successfully.")

    else:
        st.success("No validation errors found.")

    # FINAL OUTPUT
    st.subheader("Final Output")
    st.json(system)
