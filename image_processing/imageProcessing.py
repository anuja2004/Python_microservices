# imageProcessing.py
import google.generativeai as genai
import PIL.Image
from categorizer import categorize
from complaint_submission import submit_complaint
from configs.config import GEMINI_API_KEY
import logging

# Logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Configure Gemini API
genai.configure(api_key="AIzaSyBI170vlVKhHS7SGmngHi-neBAH2g3ccs4")

def describe_image(image_path):
    image = PIL.Image.open(image_path)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([image, "Describe this image in detail."])
    return response.text

def main():
    print("Starting image recognition process...\n")
    
    # You can dynamically input the image path or keep it static
    image_path = "assets/a.png"  # Replace this with your image path
    print(f"Processing Image: {image_path}\n")

    # Step 1: Describe the image
    description = describe_image(image_path)
    print("\n📝 Generated Description:\n", description)
    logging.info(f"Image Description: {description}")

    # Step 2: Categorize based on description
    category = categorize(description)
    print(f"✅ Categorized as: {category}")
    logging.info(f"Categorized as: {category}")

    # Step 3: Submit complaint
    submit_complaint(description, category, image_path)
    print("🚀 Complaint submitted successfully!")

if __name__ == "__main__":
    main()
