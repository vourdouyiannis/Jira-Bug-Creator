import time
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose the model — 2.5 Pro
MODEL_NAME = "gemini-2.5-pro"
MODEL = genai.GenerativeModel(MODEL_NAME)

def generate_content(inputs, max_retries=2, timeout=30):
    """
    Sends a multimodal request (text + optional images) to Gemini.
    Handles timeouts, retries, and empty responses safely.
    """

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            print(f"🚀 Sending to Gemini (attempt {attempt})...")

            start = time.time()
            response = MODEL.generate_content(
                inputs,
                request_options={"timeout": timeout}
            )
            elapsed = round(time.time() - start, 2)

            print(f"✅ Gemini response received in {elapsed}s.")

            # Validate the response
            if not response or not getattr(response, "text", None):
                print("⚠️ Empty response from Gemini.")
                continue

            return response.text.strip()

        except google_exceptions.DeadlineExceeded:
            print("⏰ Gemini API timeout reached. Retrying...")
        except google_exceptions.ResourceExhausted:
            print("💥 Gemini quota or rate limit exceeded.")
            break
        except google_exceptions.InvalidArgument as e:
            print(f"❌ Invalid request to Gemini: {e}")
            break
        except Exception as e:
            print(f"⚠️ Unexpected Gemini error: {e}")

        time.sleep(2)  # short backoff between retries

    # If we’re here, all attempts failed
    print("❌ Gemini service timeout or error. No output generated.")
    return "⚠️ Gemini service timeout or error. No output generated."
