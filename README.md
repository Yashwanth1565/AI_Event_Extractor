# AI Event Information Extractor

A Generative AI application that extracts structured event details from:
- Event descriptions
- Posters
- Flyers
- Conference banners

## Features
- Text Extraction
- Image Extraction
- Structured JSON Output
- LangFuse Tracing
- Streamlit UI
- Multimodal AI

## Tech Stack
- Streamlit
- Groq
- LangFuse
- Prompt Engineering
- Llama 4 Vision

## Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/b901b388-baee-442a-91f6-4faa479f2bbb" />


## Output Schema

```json
{
  "event_name": "",
  "event_date": "",
  "event_time": "",
  "event_location": "",
  "organizer": ""
}
