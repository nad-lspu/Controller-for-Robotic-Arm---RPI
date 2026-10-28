
import ast
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
