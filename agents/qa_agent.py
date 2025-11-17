import json
from services.gemini_service import generate_content
from services.utils import load_prompt, format_prompt



def generate_bug_report(title, description, analyst_findings, master_img_b64=None, branch_img_b64=None):
    """
    QA Agent:
    - Consumes structured JSON from the Analyst Agent
    - Produces a clean Markdown bug report
    - Screenshots are NOT sent to Gemini anymore
    """

    # Ensure analyst_findings is always JSON-serializable
    if isinstance(analyst_findings, dict):
        analyst_json = json.dumps(analyst_findings, indent=2)
    else:
        # In case fallback returned a string
        analyst_json = json.dumps(
            {
                "differences": analyst_findings,
                "root_cause": "",
                "severity": "",
                "notes": ""
            }, indent=2
        )

    # Build the prompt
    template = load_prompt("qa_agent")
    prompt = format_prompt(template, title=title, description=description, analyst_findings=analyst_json)

    inputs = [
        {
            "role": "user",
            "parts": [
                {"text": prompt}
            ]
        }
    ]

    print("🧾 QA Agent → Sending to Gemini...")
    result = generate_content(inputs)

    if not result:
        print("⚠️ No bug report returned by QA Agent.")
        return "⚠️ QA Agent failed to generate a report."

    return result.strip()
