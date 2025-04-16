import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import re
# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("❌ GOOGLE_API_KEY is missing from environment variables.")
genai.configure(api_key=api_key)

# Use a supported model name; adjust if necessary
model = genai.GenerativeModel("gemini-1.5-flash")


def process_with_gemini(raw_item: dict, source: str) -> dict:
    prompt = f"""
Here's a water conservation technique from source '{source}':

{json.dumps(raw_item, indent=2)}

Task:
1. Elaborate the technique clearly.
2. Add any relevant extra information or context.
3. Provide 3–5 tags.
4. Detect and include media URL (if any).
5. Try to infer location if possible.

Return the result as a JSON object with keys:
- title
- detailed_description
- extra_info
- source
- tags
- media_url
- location
"""
    try:
        response = model.generate_content([prompt])
        response_text = response.text.strip()

        # ✅ Extract JSON from code block (if wrapped in ```json ... ```)
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?\n?", "", response_text)
            response_text = re.sub(r"\n?```$", "", response_text)

        print("🔍 Cleaned Gemini response:", repr(response_text))  # Optional debug
        return json.loads(response_text)
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return {}


# For testing purposes:
if __name__ == "__main__":
    sample_item = {
        "scheme_name": "Test Scheme",
        "description": "This is a test description of a water conservation technique."
    }
    result = process_with_gemini(sample_item, "test_source")
    print("Processed Result:")
    print(json.dumps(result, indent=2))

