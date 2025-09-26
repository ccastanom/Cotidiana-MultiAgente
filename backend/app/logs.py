# backend/app/logs.py
from typing import List, Dict
from threading import Lock
import time

_LOCK = Lock()
_LOGS: List[Dict] = []

def append_log(entry: Dict):
    entry['timestamp'] = int(time.time() * 1000)
    with _LOCK:
        _LOGS.append(entry)

def get_logs(limit: int = 100):
    with _LOCK:
        return list(_LOGS[-limit:])
