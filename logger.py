import json
import os
from datetime import datetime

LOG_DIR = "logs"

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log file for this session
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"session_{timestamp}.json")

# Initialize empty log file
with open(LOG_FILE, "w") as f:
    json.dump([], f)


def log_interaction(data):

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)