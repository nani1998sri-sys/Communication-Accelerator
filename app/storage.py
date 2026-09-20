import json
from pathlib import Path
from datetime import datetime, timezone
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "state.json"
def load_state():
    if not STATE_FILE.exists(): return {"lessons": [], "messages": [], "updated_at": None}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))
def _save(state):
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
def save_lesson(content):
    state = load_state(); state["lessons"].append({"created_at": datetime.now(timezone.utc).isoformat(), "content": content}); state["lessons"] = state["lessons"][-30:]; _save(state)
def save_message(chat_id, role, content):
    state = load_state(); state["messages"].append({"chat_id": chat_id, "role": role, "content": content, "created_at": datetime.now(timezone.utc).isoformat()}); state["messages"] = state["messages"][-200:]; _save(state)
