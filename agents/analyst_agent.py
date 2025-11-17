import json
import re
from services.gemini_service import generate_content
from services.utils import load_prompt, format_prompt
from services.image_utils import compress_image


def extract_json_block(text: str) -> str:
    """
    Extract JSON between <json> ... </json>.
    Returns the inner content or the raw text if not found.
    """
    match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def analyze_bug(title, description, master_img_b64=None, branch_img_b64=None):
    """
    Analyst Agent:
    - Compares screenshots visually
    - Considers title + description for context
    - Returns ONLY structured JSON (differences, root_cause, severity, notes)
    """

    if not (master_img_b64 or branch_img_b64):
        return {
            "differences": "",
            "root_cause": "",
            "severity": "",
            "notes": ""
        }

    # Load the strict JSON prompt
    template = load_prompt("analyst_agent")
    prompt = format_prompt(template, title=title, description=description)

    # Build request
    inputs = [
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ]

    # Add images
    if master_img_b64:
        inputs[0]["parts"].append({
            "mime_type": "image/jpeg",
            "data": compress_image(master_img_b64)
        })

    if branch_img_b64:
        inputs[0]["parts"].append({
            "mime_type": "image/jpeg",
            "data": compress_image(branch_img_b64)
        })

    print("🔍 Analyst Agent → Sending to Gemini...")
    raw = generate_content(inputs)

    if not raw:
        print("⚠️ Analyst returned empty response.")
        return {
            "differences": "",
            "root_cause": "",
            "severity": "",
            "notes": ""
        }

    # Extract JSON cleanly
    cleaned = extract_json_block(raw)

    # Validate JSON output
    try:
        parsed = json.loads(cleaned)

        # Enforce schema
        if not isinstance(parsed, dict):
            raise ValueError("JSON is not an object")

        # Ensure required fields exist
        for key in ["differences", "root_cause", "severity", "notes"]:
            if key not in parsed:
                parsed[key] = ""

        return parsed

    except Exception as e:
        print(f"⚠️ Invalid JSON from analyst: {e}")
        return {
            "differences": cleaned or "",
            "root_cause": "",
            "severity": "",
            "notes": ""
        }
