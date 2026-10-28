
import ast
import subprocess
import sys
import threading
from collections import deque
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEST_SCRIPT = BASE_DIR / "test_execution.py"

_process = None

# Store the latest 200 lines of subprocess output.
_output_lines = deque(maxlen=200)

# Protect shared process and output state.
_output_lock = threading.Lock()

# Protect subprocess start and stop operations.
_process_lock = threading.Lock()

def _read_process_output(process, output_buffer):
    """
    Continuously drain subprocess output into the buffer
    belonging to that specific process.
    """
    if process.stdout is None:
        return

    try:
        for line in process.stdout:
            with _output_lock:
                output_buffer.append(line.rstrip("\r\n"))
    finally:
        process.stdout.close()

def start_test_program():
    with _process_lock:
        return _start_test_program_unlocked()

def _start_test_program_unlocked():
    global _process, _output_lines

    if _process is not None and _process.poll() is None:
        return {"status": "already_running", "pid": _process.pid}
    
    with _output_lock:
        _output_lines = deque(maxlen=200)
        current_output_buffer = _output_lines

    _process = subprocess.Popen(
        [sys.executable, "-u", str(TEST_SCRIPT)],
        cwd=str(BASE_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    threading.Thread(
        target=_read_process_output,
        args=(_process, current_output_buffer),
        daemon=True,
    ).start()

    return {"status": "started", "pid": _process.pid}

def stop_test_program():
    with _process_lock:
        return _stop_test_program_unlocked()

def _stop_test_program_unlocked():
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

def get_test_program_output():
    """
    Return a thread-safe snapshot of the current
    test program's captured output.
    """
    with _output_lock:
        lines = list(_output_lines)

    return {
        "output": "\n".join(lines),
        "lines": lines,
    }


def validate_demo_code(code: str):
    """
    Accept only simple print statements containing literal values.
    This is a restricted demonstration, not a Python sandbox.
    """
    if not isinstance(code, str) or len(code) > 2000:
        return {"valid": False, "message": "Invalid code length or type."}

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {"valid": False, "message": f"Syntax error: {error.msg}"}

    if len(tree.body) > 20:
        return {"valid": False, "message": "Too many statements."}

    for statement in tree.body:
        if not isinstance(statement, ast.Expr):
            return {
                "valid": False,
                "message": "Demo mode only supports print statements.",
            }

        call = statement.value

        if not (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "print"
            and not call.keywords
        ):
            return {
                "valid": False,
                "message": "Only print(...) is supported.",
            }

        if not all(
            isinstance(arg, ast.Constant)
            and type(arg.value) in (str, int, float, bool, type(None))
            for arg in call.args
        ):
            return {
                "valid": False,
                "message": "Only literal values are allowed inside print().",
            }

    return {"valid": True, "message": "Demo code accepted."}

def execute_demo_code(code: str):
    """
    Interpret validated literal print statements without
    executing the submitted Python source code.
    """
    validation = validate_demo_code(code)

    if not validation["valid"]:
        return {
            "success": False,
            "message": validation["message"],
            "output": "",
        }

    tree = ast.parse(code)
    output_lines = []

    for statement in tree.body:
        call = statement.value

        values = [str(arg.value) for arg in call.args]
        output_lines.append(" ".join(values))

    return {
        "success": True,
        "message": "Demo code executed successfully.",
        "output": "\n".join(output_lines),
    }