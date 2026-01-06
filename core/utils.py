
import time
import json
import os

def calculate_wpm(chars, seconds):
    return (chars / 5) / (seconds / 60) if seconds > 0 else 0.0
def calculate_accuracy(total, errors):
    return ((total - errors) / total * 100) if total > 0 else 100.0
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False
