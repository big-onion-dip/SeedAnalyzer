import re

def extract_weight(raw):
    match = re.search(r"[-+]?\s*([\d.]+)", raw or "")
    return float(match.group(1)) if match else 0
