import re

def extract_days(text):
    match = re.search(r"(\d+)\s*(day|days|night|nights)", text.lower())
    return int(match.group(1)) if match else None

def extract_kid_age(text):
    match = re.search(r"(\d+)\s*(year|years)\s*old", text.lower())
    return int(match.group(1)) if match else None

