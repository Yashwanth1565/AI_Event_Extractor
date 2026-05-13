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

## Output Schema

```json
{
  "event_name": "",
  "event_date": "",
  "event_time": "",
  "event_location": "",
  "organizer": ""
}