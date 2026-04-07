#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path
from shutil import which


STATE_DIR = Path.home() / ".codex" / "tmp"
STATE_FILE = STATE_DIR / "model_notice_state.json"
DEFAULT_SOUND = Path("/System/Library/Sounds/Funk.aiff")


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


def run_quietly(command: list[str]) -> None:
    subprocess.run(
        command,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def notify_mac(title: str, subtitle: str, message: str) -> None:
    if sys.platform != "darwin":
        return
    safe_title = title.replace('"', "'")
    safe_subtitle = subtitle.replace('"', "'")
    safe_message = message.replace('"', "'")
    script = (
        f'display notification "{safe_message}" '
        f'with title "{safe_title}" subtitle "{safe_subtitle}"'
    )
    run_quietly(["/usr/bin/osascript", "-e", script])


def notify_windows(title: str, subtitle: str, message: str) -> None:
    if sys.platform != "win32":
        return

    powershell = which("powershell") or which("powershell.exe") or which("pwsh")
    if not powershell:
        return

    lines = [title.strip()]
    if subtitle.strip():
        lines.append(subtitle.strip())
    if message.strip():
        lines.append(message.strip())
    body = "\n".join(lines)

    # Best effort toast: if the Windows notification API is unavailable, the
    # hook still falls back to the in-app systemMessage and optional beep.
    script = rf"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime -ErrorAction SilentlyContinue
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null
$xml = @"
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>{escape(title)}</text>
      <text>{escape(subtitle)}</text>
      <text>{escape(message)}</text>
    </binding>
  </visual>
</toast>
"@
$doc = New-Object Windows.Data.Xml.Dom.XmlDocument
$doc.LoadXml($xml)
$toast = [Windows.UI.Notifications.ToastNotification]::new($doc)
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Codex")
$notifier.Show($toast)
"""
    run_quietly([powershell, "-NoProfile", "-Command", script])


def play_sound() -> None:
    if sys.platform == "darwin":
        if DEFAULT_SOUND.exists():
            for _ in range(2):
                run_quietly(["/usr/bin/afplay", "-v", "2", str(DEFAULT_SOUND)])
            return
        run_quietly(["/usr/bin/osascript", "-e", "beep 2"])
        return

    if sys.platform == "win32":
        try:
            import winsound

            for _ in range(2):
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            pass
        return


def notify_user(title: str, subtitle: str, message: str) -> None:
    if sys.platform == "darwin":
        notify_mac(title, subtitle, message)
        return

    if sys.platform == "win32":
        notify_windows(title, subtitle, message)


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
                play_sound()
                notify_user("Codex", "模型已切换", f"{previous} -> {model}")
                emit(f"模型已切换：{previous} -> {model}")
            else:
                emit(f"当前模型：{model}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
