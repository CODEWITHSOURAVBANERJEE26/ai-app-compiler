# AI Application Compiler

## Overview

AI Application Compiler is an AI-powered orchestration system that converts natural language prompts into structured application architectures.

The system uses a multi-stage AI pipeline to:
- extract application intent
- generate system architecture
- validate generated structure
- repair missing components automatically

The final output is returned as structured JSON.

---

## Features

- Intent Extraction
- System Architecture Generation
- Validation Engine
- Automatic Repair Engine
- Structured JSON Output
- Streamlit Web Interface
- Groq LLM Integration
- Multi-stage AI Orchestration Pipeline

---

## Tech Stack

- Python
- Streamlit
- Groq API
- JSON
- python-dotenv

---

## Architecture Pipeline

User Input
→ Intent Extraction
→ System Generation
→ Validation
→ Repair
→ Final Output

---

## Project Files

### main.py

Contains the original terminal-based orchestration pipeline.

### app.py

Contains the deployed Streamlit web application interface.

### requirements.txt

Contains all required Python dependencies.

### README.md

Project documentation and setup instructions.

---

## Example Prompt

Build CRM with login dashboard analytics payments

---

## Example Output

```json
{
  "ui": {
    "pages": [
      "login",
      "dashboard"
    ]
  },
  "api": {
    "routes": [
      "/login",
      "/dashboard"
    ]
  },
  "db": {
    "tables": [
      "users"
    ]
  },
  "auth": {
    "roles": [
      "admin",
      "user"
    ]
  }
}


## Live Demo

https://ai-app-compiler-jtfxtttfxcqknccagwystm.streamlit.app/

--Search it on web

