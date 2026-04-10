import ast
import asyncio
import os
import signal
import sys

FORBIDDEN_MODULES = {"os", "sys", "subprocess", "socket", "multiprocessing", "threading", "ctypes", "importlib"}


def check_forbidden(code: str) -> str | None:
    """Check for forbidden module imports using AST parsing.

    Known limitation (classroom MVP): dynamic imports such as
    __import__("os") or importlib.import_module("os") are NOT caught here.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None  # SyntaxError is caught later in the subprocess
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in FORBIDDEN_MODULES:
                    return f"不允許使用 {root} 模組"
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in FORBIDDEN_MODULES:
                return f"不允許使用 {root} 模組"
    return None


async def run_code(code: str, input_val: str, timeout: float = 5.0) -> dict:
    """
    以 asyncio subprocess 執行學生程式碼，傳入一組測試輸入。

    Returns:
        dict: { actual: str|None, error_type: str|None, stderr: str }
        error_type 可能值: "syntax_error" | "runtime_error" | "no_return" | None
    """
    forbidden_error = check_forbidden(code)
    if forbidden_error:
        return {"actual": None, "error_type": "runtime_error", "stderr": forbidden_error}

    try:
        compile(code, "<student>", "exec")
    except SyntaxError as e:
        return {"actual": None, "error_type": "syntax_error", "stderr": f"SyntaxError: {e}"}

    runner_script = f"""{code}

_sol = Solution()
_result = _sol.lengthOfLongestSubstring({repr(input_val)})
print(_result)
"""

    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            runner_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        stderr_str = stderr.decode().strip()
        stdout_str = stdout.decode().strip()

        if proc.returncode != 0:
            if "SyntaxError" in stderr_str:
                return {"actual": None, "error_type": "syntax_error", "stderr": stderr_str}
            return {"actual": None, "error_type": "runtime_error", "stderr": stderr_str}

        if stdout_str in ("None", ""):
            return {"actual": None, "error_type": "no_return", "stderr": ""}

        return {"actual": stdout_str, "error_type": None, "stderr": ""}

    except asyncio.TimeoutError:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        await proc.wait()
        return {"actual": None, "error_type": "runtime_error", "stderr": "執行超時（超過時間限制）"}
