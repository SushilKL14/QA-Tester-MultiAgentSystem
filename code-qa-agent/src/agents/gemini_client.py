# src/agents/gemini_client.py

"""
Gemini client adapter.

Modes:
- ADC (preferred): If GCP_PROJECT env var is set, use Application Default Credentials
  to obtain short-lived bearer tokens and call the Vertex AI REST predict endpoint.

- API key fallback: If GEMINI_API_KEY is set, call the Google Generative API via
  the "https://us-central1-aiplatform.googleapis.com/v1" model predict endpoint with
  the API key in the header as a Bearer token (or adapt to your organization's pattern).

IMPORTANT: This module will raise a RuntimeError if neither GCP_PROJECT nor GEMINI_API_KEY
is present so the application fails loudly and with a clear message (no silent stubs).
"""

import os
import json
import requests

# Try to import google auth for ADC; if not available, ADC won't be used.
try:
    import google.auth
    from google.auth.transport.requests import Request
    _HAS_GOOGLE_AUTH = True
except Exception:
    _HAS_GOOGLE_AUTH = False

PROJECT = os.getenv("GCP_PROJECT")
REGION = os.getenv("GCP_REGION", "us-central1")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY")  # optional fallback

def _get_adc_access_token():
    if not _HAS_GOOGLE_AUTH:
        raise RuntimeError("google.auth library not available for ADC token generation.")
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(Request())
    return credentials.token

def _call_vertex_predict_with_token(prompt: str, access_token: str, max_output_tokens: int = 512, temperature: float = 0.2):
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
    return resp.json()

def _call_vertex_predict_with_api_key(prompt: str, api_key: str, max_output_tokens: int = 512, temperature: float = 0.2):
    endpoint = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/publishers/google/models/{MODEL}:predict"
    body = {
        "instances": [{"content": prompt}],
        "parameters": {"maxOutputTokens": max_output_tokens, "temperature": temperature}
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(endpoint, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()

def generate_text(prompt: str, max_output_tokens: int = 512, temperature: float = 0.2) -> str:
    if PROJECT:
        if not _HAS_GOOGLE_AUTH:
            raise RuntimeError("GCP_PROJECT set but google.auth library is not installed.")
        token = _get_adc_access_token()
        resp = _call_vertex_predict_with_token(prompt, token, max_output_tokens, temperature)
    elif API_KEY:
        resp = _call_vertex_predict_with_api_key(prompt, API_KEY, max_output_tokens, temperature)
    else:
        raise RuntimeError(
            "Gemini integration requires either GCP_PROJECT (ADC mode) or GEMINI_API_KEY environment variable. "
            "Set one of them and try again."
        )

    text = ""
    if isinstance(resp.get("predictions"), list) and resp["predictions"]:
        first = resp["predictions"][0]
        if isinstance(first, dict):
            text = first.get("content", "") or first.get("output", "") or json.dumps(first)
        else:
            text = str(first)
    elif "outputs" in resp:
        if resp["outputs"]:
            out0 = resp["outputs"][0]
            if isinstance(out0, dict):
                text = out0.get("content", "") or out0.get("text", "") or json.dumps(out0)
            else:
                text = str(out0)
    else:
        text = json.dumps(resp)

    return json.dumps({"text": text, "raw": resp})
