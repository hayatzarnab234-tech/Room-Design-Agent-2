import os

from google import genai
from google.genai import types

from prompts import ROOM_DESIGN_SYSTEM_PROMPT
from rag import retrieve_knowledge


def get_api_key():

    # Try Streamlit secrets first
    try:

        import streamlit as st

        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]

    except Exception:
        pass

    # Fall back to environment variable
    return os.getenv("GEMINI_API_KEY")


def generate_room_design(room_data):

    api_key = get_api_key()

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to .streamlit/secrets.toml locally "
            "or add it through Streamlit Cloud Secrets."
        )

    # Create Gemini client
    client = genai.Client(
        api_key=api_key
    )

    # Retrieve relevant design knowledge
    knowledge = retrieve_knowledge(room_data)

    # Build user prompt
    user_prompt = f"""
Create a practical residential interior design using the information below.

USER REQUIREMENTS

Room type:
{room_data.get("room_type", "")}

Room dimensions:
{room_data.get("dimensions", "")}

Budget:
{room_data.get("budget", "")}

Preferred design style:
{room_data.get("style", "")}

Preferred colors:
{room_data.get("colors", "")}

Required furniture:
{room_data.get("furniture", "")}

Functional requirements:
{room_data.get("functional_requirements", "")}

Additional preferences:
{room_data.get("additional_preferences", "")}


RETRIEVED DESIGN KNOWLEDGE

{knowledge}


INSTRUCTIONS

Use the retrieved knowledge only when relevant.

Do not invent room dimensions.

Do not claim that furniture definitely fits unless the
provided dimensions support that conclusion.

Do not invent confirmed product prices.

Clearly distinguish estimates from confirmed prices.

If important information is missing, state what is missing.

Follow the required output structure exactly.
"""

    # Generate response
    response = client.models.generate_content(

        model="model="gemini-3.8-flash",

        config=types.GenerateContentConfig(
            system_instruction=ROOM_DESIGN_SYSTEM_PROMPT,
            temperature=0.4
        ),

        contents=user_prompt
    )

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text
