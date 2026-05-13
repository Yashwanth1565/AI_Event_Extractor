import os
import json
import base64

from groq import Groq
from dotenv import load_dotenv

from app.langfuse_config import langfuse

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print(os.getenv("GROQ_API_KEY"))

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

    trace = langfuse.trace(
        name="event_extraction",
        user_id="streamlit_user"
    )

    generation = trace.generation(
        name="groq-generation",
        model="llama-3.3-70b-versatile",
        input="multimodal_input"
    )

    prompt = """
You are an intelligent event information extractor.

Extract event details strictly in JSON format.

RULES:
1. Return ONLY valid JSON.
2. Missing fields must be "not_available".

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

        # ---------- TEXT INPUT ---------- #

        if text and text.strip() != "":

            final_prompt = f"""
{prompt}

USER INPUT:
{text}
"""

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

        # ---------- IMAGE INPUT ---------- #

        elif image is not None:

            image_bytes = image.read()

            base64_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

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

        else:

            return default_response()

        raw_output = response.choices[0].message.content

        cleaned_output = clean_json(raw_output)

        parsed = json.loads(cleaned_output)

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

        generation.end(output=parsed)

        trace.update(output=parsed)

        return parsed

    except Exception as e:

        error_response = default_response()

        error_response["error"] = str(e)

        generation.end(output=error_response)

        trace.update(output=error_response)

        return error_response