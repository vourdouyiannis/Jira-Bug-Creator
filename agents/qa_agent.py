import json
from services.gemini_service import generate_content
from services.utils import load_prompt, format_prompt


def generate_bug_report(title, description, analyst_findings):
    """
    Generate a structured Markdown bug report using Gemini based on analyst findings.

    @param title: str, the bug title.
    @param description: str, the bug description.
    @param analyst_findings: dict or str, structured findings from Analyst Agent.

    @return: str, cleaned Markdown bug report or fallback error message.
    """

    # Normalize input to JSON string
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
    prompt = format_prompt(template, title=title, description=description,
                           analyst_findings=analyst_json)

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
