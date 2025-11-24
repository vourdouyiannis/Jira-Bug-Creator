import time
import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

load_dotenv()

# Choose the model from environment
MODEL_NAME = os.getenv("MODEL_NAME")
MODEL = genai.GenerativeModel(MODEL_NAME)


def generate_content(inputs, max_retries=2, timeout=30):
    """
    Send a multimodal request to Gemini with retry and timeout handling.

    @param inputs: list, prompt in Gemini API format.
    @param max_retries: int, number of retry attempts.
    @param timeout: int, timeout in seconds per attempt.

    @return: str, response text or fallback error message.
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
