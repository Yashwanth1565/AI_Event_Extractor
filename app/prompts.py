EXTRACTION_PROMPT = """
Extract event information from the given text.

Rules:
1. Return ONLY valid JSON.
2. Do not include explanations.
3. Do not use markdown.
4. Do not hallucinate missing fields.
5. Missing fields must be "not_available".

Output Schema:
{{
  "event_name": "",
  "event_date": "",
  "event_time": "",
  "event_location": "",
  "organizer": ""
}}

Text:
{text}
"""