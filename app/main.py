import os
import json
import base64

from groq import Groq
from dotenv import load_dotenv
from app.langfuse_config import langfuse

# ---------- LOAD ENV ---------- #

load_dotenv()

# ---------- GROQ CLIENT ---------- #

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------- DEFAULT RESPONSE ---------- #

def default_response():

    return {
        "event_name": "not_available",
        "event_date": "not_available",
        "event_time": "not_available",
        "event_location": "not_available",
        "organizer": "not_available"
    }

# ---------- CLEAN JSON ---------- #

def clean_json(raw_output):

    return (
        raw_output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

# ---------- MAIN FUNCTION ---------- #

def process_event_input(text=None, image=None):

    # ---------- CREATE TRACE ---------- #

    trace = langfuse.trace(
        name="AI_Event_Extraction_System"
    )

    prompt = """
You are an intelligent AI Event Information Extractor.

Extract event details strictly in JSON format.

RULES:
1. Return ONLY valid JSON.
2. Missing fields must be "not_available".
3. No explanations.
4. No markdown.

Output Schema:
{
  "event_name": "",
  "event_date": "",
  "event_time": "",
  "event_location": "",
  "organizer": ""
}
"""

    try:

        # ====================================================
        # TEXT INPUT FLOW
        # ==================================================== #

        if text and text.strip() != "":

            final_prompt = f"""
{prompt}

USER INPUT:
{text}
"""

            generation = trace.generation(
                name="text_extraction",
                model="llama-3.3-70b-versatile",
                input=final_prompt
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content

        # ====================================================
        # IMAGE INPUT FLOW
        # ==================================================== #

        elif image is not None:

            image_bytes = image.read()

            base64_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            generation = trace.generation(
                name="image_extraction",
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                input="uploaded_event_poster"
            )

            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content

        else:

            return default_response()

        # ---------- CLEAN OUTPUT ---------- #

        cleaned_output = clean_json(
            raw_output
        )

        # ---------- PARSE JSON ---------- #

        parsed = json.loads(
            cleaned_output
        )

        # ---------- REQUIRED FIELDS ---------- #

        required_fields = [
            "event_name",
            "event_date",
            "event_time",
            "event_location",
            "organizer"
        ]

        for field in required_fields:

            if field not in parsed:

                parsed[field] = "not_available"

        # ---------- END GENERATION ---------- #

        generation.end(
            output=parsed
        )

        # ---------- UPDATE TRACE ---------- #

        trace.update(
            input={
                "text": text if text else None,
                "image_uploaded": True if image else False
            },
            output=parsed,
            metadata={
                "project": "AI Event Extractor",
                "framework": "Streamlit",
                "llm_provider": "Groq"
            }
        )

        # ---------- FLUSH ---------- #

        langfuse.flush()

        return parsed

    # ====================================================
    # ERROR HANDLING
    # ==================================================== #

    except Exception as e:

        error_response = default_response()

        error_response["error"] = str(e)

        trace.update(
            output=error_response
        )

        langfuse.flush()

        return error_response