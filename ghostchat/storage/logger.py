import os
import time
from config import LOG_FILE, LOG_TTL_SECONDS

os.makedirs("logs", exist_ok=True)

def log_message(sender, message, timestamp):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}|{sender}|{message}\n")

def prune_logs():
    if not os.path.exists(LOG_FILE):
        return

    cutoff = time.time() - LOG_TTL_SECONDS
    keep = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            ts, _, _ = line.strip().split("|", 2)
            if float(ts) >= cutoff:
                keep.append(line)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(keep)
