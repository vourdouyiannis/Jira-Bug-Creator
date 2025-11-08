from services.gemini_service import generate_content
from services.utils import load_prompt
from services.image_utils import compress_image  # ensure this exists


def analyze_bug(title, description, master_img_b64=None, branch_img_b64=None):
    """
    The Analyst agent now handles:
    - Title + description analysis
    - Screenshots (1 or 2) with automatic compression
    - Combined + sequential fallback for stability
    """
    if not (master_img_b64 or branch_img_b64):
        return ""

    # Load and format prompt
    prompt = load_prompt("analyst_agent").format(
        title=title,
        description=description
    )
    # Clarify runtime context (added dynamically, not in txt)
    prompt += "\n\nNote: If two screenshots are provided, they represent PRODUCTION (master) and DEVELOPMENT (branch). Compare them visually."

    # Prepare input
    inputs = [
        {"role": "user", "parts": [
            {"text": prompt},
        ]}
    ]

    # Add screenshots if available
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
    result = generate_content(inputs)

    # Fallback: if response fails or stalls, try analyzing images separately
    if not result and master_img_b64 and branch_img_b64:
        print("⚠️ Combined analysis failed, retrying sequentially...")
        results = []
        for img_b64 in [master_img_b64, branch_img_b64]:
            img_inputs = [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"mime_type": "image/jpeg", "data": compress_image(img_b64)}
                    ]
                }
            ]
            partial = generate_content(img_inputs)
            if partial:
                results.append(partial)
        result = "\n\n".join(results)

    print("✅ Analyst Agent → Gemini response received.")
    return result
