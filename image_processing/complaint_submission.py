from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://aaryashdevane312:MfipouSVCU19dySu@cluster0.jw9bg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["complaints_db"]  # Database name
collection = db["complaints"]  # Collection name

def submit_complaint(description, category, image_path):
    """Stores the complaint in MongoDB."""
    complaint_data = {
        "description": description,
        "category": category,
        "image_path": image_path
    }
    
    # Insert into MongoDB
    collection.insert_one(complaint_data)
    
    print("✅ Complaint successfully stored in MongoDB.")
