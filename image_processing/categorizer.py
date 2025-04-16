# categorizer.py
def categorize(description):
    description = description.lower()
    
    if "garbage" in description or "trash" in description:
        return "Garbage Issue"
    elif "water" in description or "leak" in description or "pipeline" in description:
        return "Water Leakage"
    elif "sewage" in description or "drain" in description:
        return "Sewage Blockage"
    else:
        return "Uncategorized"
