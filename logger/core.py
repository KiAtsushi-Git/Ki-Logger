import os
import datetime
import inspect

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(CORE_DIR, "..", "logs"))
BASE_DIR = os.path.abspath(os.path.join(CORE_DIR, ".."))

def _get_caller_info():
    for frame_info in inspect.stack():
        filepath = os.path.abspath(frame_info.filename)
        if "logger/core.py" not in filepath.replace("\\", "/"):
            relative_path = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
            lineno = frame_info.lineno
            return f"{relative_path}:{lineno}"
    return "unknown:0"

def _write_log(level: str, message: str, name: str = "default"):
    now = datetime.datetime.now()
    folder = os.path.join(LOG_DIR, name)
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, f"{now.date()}.log")
    location = _get_caller_info()

    line = f"[{level.upper()}][{now.strftime('%Y-%m-%d %H:%M:%S')}][{name}][{location}] {message}\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(line)

def info(message: str, name: str = "default"):
    _write_log("info", message, name)

def warning(message: str, name: str = "default"):
    _write_log("warning", message, name)

def error(message: str, name: str = "default"):
    _write_log("error", message, name)
