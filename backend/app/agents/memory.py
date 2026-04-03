from typing import Dict, Any

# Simple In-Memory State for mock/dev
_session_storage = {}

def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in _session_storage:
        _session_storage[session_id] = {"history": [], "context": {}}
    return _session_storage[session_id]

def update_session(session_id: str, key: str, value: Any):
    session = get_session(session_id)
    session["context"][key] = value

def append_history(session_id: str, message: dict):
    session = get_session(session_id)
    session["history"].append(message)
