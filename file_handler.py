##To ensure your data doesn't vanish when you close the program, you'll need robust JSON handling.


import json
import os
import shutil

def save_data(data, filename="data/expenses.json"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def load_data(filename="data/expenses.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
