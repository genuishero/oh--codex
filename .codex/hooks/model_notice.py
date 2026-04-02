#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from pathlib import Path


STATE_DIR = Path.home() / ".codex" / "tmp"
STATE_FILE = STATE_DIR / "model_notice_state.json"


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=STATE_DIR, delete=False
    ) as tmp:
        json.dump(state, tmp, ensure_ascii=False)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    os.replace(temp_name, STATE_FILE)


def emit(message: str) -> None:
    print(json.dumps({"systemMessage": message}, ensure_ascii=False))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    session_id = payload.get("session_id")
    model = payload.get("model")
    event_name = payload.get("hook_event_name")

    if not session_id or not model or not event_name:
        return 0

    state = load_state()
    previous = state.get(session_id)

    if event_name == "SessionStart":
        state[session_id] = model
        save_state(state)
        emit(f"当前模型：{model}")
        return 0

    if event_name == "UserPromptSubmit":
        if previous != model:
            state[session_id] = model
            save_state(state)
            if previous:
                emit(f"模型已切换：{previous} -> {model}")
            else:
                emit(f"当前模型：{model}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
