# src/agents/gemini_client.py
"""
Adapter to use Gemini 1.5 Flash for code reasoning without embedding API keys.
Requires environment variables:
- GCP_PROJECT
- GCP_REGION
- GEMINI_MODEL (e.g., 'gemini-1.5-flash')
"""

import os
import json
import google.auth
from google.auth.transport.requests import Request
import requests

PROJECT = os.getenv("GCP_PROJECT")
REGION = os.getenv("GCP_REGION", "us-central1")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not PROJECT:
    raise RuntimeError("GCP_PROJECT environment variable is required for Gemini integration.")

def _get_access_token():
    """Generate short-lived access token from service account."""
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(Request())
    return credentials.token

def generate_text(prompt: str, max_output_tokens: int = 512, temperature: float = 0.2) -> dict:
    """
    Call Gemini 1.5 Flash and return the response as a dict.
    Returns:
      {
        "text": "main generated text",
        "raw": {... full API response ...}
      }
    """
    access_token = _get_access_token()
    endpoint = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models/{MODEL}:predict"

    body = {
        "instances": [{"content": prompt}],
        "parameters": {"maxOutputTokens": max_output_tokens, "temperature": temperature}
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(endpoint, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    text = ""
    if isinstance(data.get("predictions"), list) and data["predictions"]:
        first = data["predictions"][0]
        if isinstance(first, dict):
            text = first.get("content", "") or first.get("output", "") or json.dumps(first)
        else:
            text = str(first)
    elif "outputs" in data:
        text = data["outputs"][0].get("content", "") if data["outputs"] else ""
    else:
        text = json.dumps(data)

    return {"text": text, "raw": data}
