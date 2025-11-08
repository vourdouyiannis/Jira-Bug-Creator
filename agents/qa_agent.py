from services.gemini_service import generate_content
from services.utils import load_prompt
from services.image_utils import compress_image  # ensure this exists


def generate_bug_report(title, description, analyst_findings, master_img_b64=None, branch_img_b64=None):
    """
    QA Agent combines text + analyst findings + screenshots.
    It automatically includes both screenshots if provided, or one if not.
    """
    # Load and format prompt
    prompt = load_prompt("qa_agent").format(
        title=title,
        description=description,
        analyst_findings=analyst_findings
    )
    # prompt += "\n\nNote: If two screenshots exist, treat the first as PRODUCTION and the second as DEVELOPMENT. Focus on visual regressions or discrepancies."
    prompt += "\nDo not include or describe base64 data in your response. Only describe the differences or analysis."

    inputs = [
        {"role": "user", "parts": [
            {"text": prompt},
        ]}
    ]
    #
    # if master_img_b64:
    #     inputs[0]["parts"].append({
    #         "mime_type": "image/jpeg",
    #         "data": compress_image(master_img_b64)
    #     })
    # if branch_img_b64:
    #     inputs[0]["parts"].append({
    #         "mime_type": "image/jpeg",
    #         "data": compress_image(branch_img_b64)
    #     })

    print("🧾 QA Agent → Sending to Gemini...")
    result = generate_content(inputs)

    # # Fallback: try sequential if first attempt fails
    # if not result and master_img_b64 and branch_img_b64:
    #     print("⚠️ Combined bug generation failed, retrying sequentially...")
    #     results = []
    #     for img_b64 in [master_img_b64, branch_img_b64]:
    #         img_inputs = [prompt, {
    #             "mime_type": "image/png",
    #             "data": compress_image(img_b64)
    #         }]
    #         partial = generate_content(img_inputs)
    #         if partial:
    #             results.append(partial)
    #     result = "\n\n".join(results)
    #
    # print("✅ QA Agent → Gemini response received.")
    return result
