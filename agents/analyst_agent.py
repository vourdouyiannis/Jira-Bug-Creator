import json
import re
from services.gemini_service import generate_content
from services.utils import load_prompt, format_prompt
from services.image_utils import compress_image


def extract_json_block(text):
    """
    Extract JSON block from Gemini response.

    Looks for <json>...</json> tags and returns the inner text.
    Falls back to returning raw text if tags are not found.

    @param text: str, raw response text.

    @return: str, potential JSON content.
    """
    match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def analyze_bug(title, description, master_img_b64=None, branch_img_b64=None):
    """
    Analyze visual and contextual differences using Gemini.

    @param title: str, the bug title.
    @param description: str, the bug description.
    @param master_img_b64: str|None, base64 image of reference (master).
    @param branch_img_b64: str|None, base64 image of comparison (branch).

    @return: dict, structured analysis with keys: differences, root_cause, severity, notes.
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

    inputs = [
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ]

    # Attach screenshots
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
