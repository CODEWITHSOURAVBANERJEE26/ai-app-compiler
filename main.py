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

    print("\nRAW RESPONSE:\n")
    print(content)

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

    print("\nRAW RESPONSE:\n")
    print(content)

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
# MAIN PIPELINE
# -------------------------
def run():

    print("\n==============================")
    print(" AI APPLICATION COMPILER ")
    print("==============================\n")

    user_input = input("Enter app idea: ")

    # STEP 1
    print("\n[1] Extracting Intent...")
    intent = extract_intent(user_input)

    # STEP 2
    print("\n[2] Generating System...")
    system = generate_system(intent)

    # STEP 3
    print("\n[3] Validating...")
    errors = validate(system)

    # STEP 4
    if errors:
        print("\n[4] Repairing...")
        system = repair(system, errors)

    # FINAL OUTPUT
    print("\n==============================")
    print(" FINAL OUTPUT ")
    print("==============================\n")

    print(json.dumps(system, indent=2))

# -------------------------
# START
# -------------------------
if __name__ == "__main__":
    run()