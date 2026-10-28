
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEST_SCRIPT = BASE_DIR / "test_execution.py"

_process = None


def start_test_program():
    global _process

    if _process is not None and _process.poll() is None:
        return {"status": "already_running", "pid": _process.pid}

    _process = subprocess.Popen(
        [sys.executable, str(TEST_SCRIPT)],
        cwd=str(BASE_DIR),
    )

    return {"status": "started", "pid": _process.pid}


def stop_test_program():
    global _process

    if _process is None or _process.poll() is not None:
        _process = None
        return {"status": "not_running"}

    _process.terminate()

    try:
        _process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _process.kill()
        _process.wait()

    _process = None
    return {"status": "stopped"}
