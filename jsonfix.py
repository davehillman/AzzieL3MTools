## AzzieL3M
## jsonfix.py
## Hillman
## March 2026

## following code initially created by ChatGPT (3/25) to solidify json formatting
## from output by the LLM sources

import json
import re
from typing import Any


def extract_json_block(text: str) -> str:
    """
    Extract JSON from LLM output.
    Handles ```json fences and embedded JSON.
    """
    # Remove code fences
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    # Try to find first JSON object or array
    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if match:
        return match.group(1)

    return text  # fallback


def clean_json_string(s: str) -> str:
    """
    Attempt to fix common JSON issues from LLMs.
    """
    # Replace single quotes with double quotes (careful heuristic)
    s = re.sub(r"'", '"', s)

    # Remove trailing commas before closing braces/brackets
    s = re.sub(r",\s*([\]}])", r"\1", s)

    return s


def normalize_json(data: Any) -> dict:
    """
    Normalize parsed JSON into consistent dict structure.
    """
    if isinstance(data, dict):
        return data

    if isinstance(data, list):
        if len(data) == 1 and data[0] == "no data":
            return {"status": "no data"}
        return {"items": data}

    if isinstance(data, str):
        return {"value": data}

    if isinstance(data, (int, float, bool)) or data is None:
        return {"value": data}

    return {"value": str(data)}


def parse_llm_json(text: str) -> dict:
    """
    Full pipeline:
    extract → clean → parse → normalize
    """
    extracted = extract_json_block(text)

    try:
        parsed = json.loads(extracted)
        # return {
        #     "ok": True,
        #     "stage": "direct",
        #     "normalized": normalize_json(parsed),
        #     "raw_parsed": parsed,
        # }
        return parsed
    except json.JSONDecodeError:
        pass

    # Try cleaning
    cleaned = clean_json_string(extracted)

    try:
        parsed = json.loads(cleaned)
        # return {
        #     "ok": True,
        #     "stage": "cleaned",
        #     "normalized": normalize_json(parsed),
        #     "raw_parsed": parsed,
        # }
        return parsed
    except json.JSONDecodeError as e:
        # return {
        #     "ok": False,
        #     "error": str(e),
        #     "extracted": extracted,
        #     "cleaned": cleaned,
        # }
        return cleaned
    
## above could be modified for different outputs.
