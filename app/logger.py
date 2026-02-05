import json
import sys
from datetime import datetime


def log(level: str, message: str, **fields):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **fields,
    }
    sys.stdout.write(json.dumps(entry) + "\n")
    sys.stdout.flush()
