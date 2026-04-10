# Python 學習平台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一個 Python 學習網站，讓大一學生提交程式碼後，系統執行程式碼、比對 18 組測試案例，並用 Groq Cloud AI 分析錯誤 pattern 給予引導式提示。

**Architecture:** FastAPI 後端以 asyncio subprocess 執行學生程式碼（全跑 18 組），比對結果後呼叫 Groq Cloud API，依 error_type 選擇三種 prompt 分支。Vue.js 前端使用 Monaco Editor，收到完整 results 後只渲染到第一個失敗為止，讓學生聚焦解決一個問題。

**Tech Stack:** Python 3.11+, FastAPI, uvicorn, openai SDK (Groq Cloud API), python-dotenv, pytest, pytest-asyncio, httpx, Vue 3, Vite, @guolao/vue-monaco-editor, axios

---

## 檔案結構

```
畢業專題/
├── backend/
│   ├── main.py            # FastAPI app，POST /submit
│   ├── executor.py        # asyncio subprocess 執行 + blacklist + timeout
│   ├── judge.py           # 18 組 test case 比對
│   ├── ai.py              # Groq Cloud API + 3 種 prompt 分支
│   ├── problem.py         # 題目定義 + 18 組 TEST_CASES
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env               # GROQ_API_KEY（不 commit）
│   ├── .env.example
│   └── tests/
│       ├── test_executor.py
│       ├── test_judge.py
│       ├── test_ai.py
│       └── test_main.py
└── frontend/
    ├── index.html
    └── src/
        ├── App.vue
        ├── api.js
        └── components/
            ├── ProblemStatement.vue
            ├── CodeEditor.vue
            └── ResultPanel.vue
```

---

### Task 1: 後端專案建立

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/pytest.ini`
- Create: `backend/.env.example`

- [ ] **Step 1: 建立目錄結構**

```bash
mkdir -p /home/auxe/Desktop/畢業專題/backend/tests
touch /home/auxe/Desktop/畢業專題/backend/__init__.py
touch /home/auxe/Desktop/畢業專題/backend/tests/__init__.py
```

- [ ] **Step 2: 建立 requirements.txt**

`backend/requirements.txt`:
```
fastapi==0.115.0
uvicorn==0.30.0
openai==1.51.0
python-dotenv==1.0.1
pytest==8.3.0
pytest-asyncio==0.24.0
httpx==0.27.0
```

- [ ] **Step 3: 建立 pytest.ini**

`backend/pytest.ini`:
```ini
[pytest]
asyncio_mode = auto
```

- [ ] **Step 4: 建立 .env.example**

`backend/.env.example`:
```
GROQ_API_KEY=your_api_key_here
```

- [ ] **Step 5: 安裝依賴並建立 .env**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pip install -r requirements.txt
cp .env.example .env
# 編輯 .env，填入實際的 GROQ_API_KEY
```

- [ ] **Step 6: 建立 .gitignore 並 commit**

`/home/auxe/Desktop/畢業專題/.gitignore`:
```
.env
__pycache__/
.pytest_cache/
node_modules/
.superpowers/
```

```bash
cd /home/auxe/Desktop/畢業專題
git init
git add backend/requirements.txt backend/pytest.ini backend/.env.example .gitignore
git commit -m "feat: backend project setup"
```

---

### Task 2: problem.py — 題目定義與 18 組測試案例

**Files:**
- Create: `backend/problem.py`

- [ ] **Step 1: 建立 problem.py**

`backend/problem.py`:
```python
PROBLEM = {
    "title": "Longest Substring Without Repeating Characters",
    "description": "給定一個字串 s，請找出不含重複字元的最長子字串的長度。",
    "examples": [
        {
            "input": "abcabcbb",
            "output": 3,
            "explanation": '最長不重複子字串為 "abc"，長度為 3',
        },
        {
            "input": "bbbbb",
            "output": 1,
            "explanation": '最長子字串為 "b"，長度為 1',
        },
        {
            "input": "pwwkew",
            "output": 3,
            "explanation": '最長不重複子字串為 "wke"，長度為 3',
        },
    ],
    "starter_code": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 在此撰寫你的解法
        pass
""",
}

TEST_CASES = [
    # 基本測試
    {"index": 1,  "input": "abcabcbb",                   "expected": 3,  "is_stress": False},
    {"index": 2,  "input": "bbbbb",                      "expected": 1,  "is_stress": False},
    {"index": 3,  "input": "pwwkew",                     "expected": 3,  "is_stress": False},
    # 邊界條件
    {"index": 4,  "input": "",                           "expected": 0,  "is_stress": False},
    {"index": 5,  "input": "a",                          "expected": 1,  "is_stress": False},
    {"index": 6,  "input": "au",                         "expected": 2,  "is_stress": False},
    {"index": 7,  "input": "aa",                         "expected": 1,  "is_stress": False},
    # 進階測試
    {"index": 8,  "input": "abcdefg",                    "expected": 7,  "is_stress": False},
    {"index": 9,  "input": "dvdf",                       "expected": 3,  "is_stress": False},
    {"index": 10, "input": "anviaj",                     "expected": 5,  "is_stress": False},
    {"index": 11, "input": "tmmzuxt",                    "expected": 5,  "is_stress": False},
    {"index": 12, "input": "abba",                       "expected": 2,  "is_stress": False},
    {"index": 13, "input": "aab",                        "expected": 2,  "is_stress": False},
    # 特殊字元
    {"index": 14, "input": "a b",                        "expected": 3,  "is_stress": False},
    {"index": 15, "input": "!@#$%",                      "expected": 5,  "is_stress": False},
    {"index": 16, "input": " ",                          "expected": 1,  "is_stress": False},
    # 壓力測試
    {"index": 17, "input": "a" * 50000,                  "expected": 1,  "is_stress": True},
    {"index": 18, "input": "abcdefghijklmnopqrstuvwxyz", "expected": 26, "is_stress": False},
]
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add backend/problem.py
git commit -m "feat: add problem definition and 18 test cases"
```

---

### Task 3: executor.py — 非同步程式碼執行

**Files:**
- Create: `backend/executor.py`
- Create: `backend/tests/test_executor.py`

- [ ] **Step 1: 撰寫失敗測試**

`backend/tests/test_executor.py`:
```python
import pytest
from executor import run_code


@pytest.mark.asyncio
async def test_correct_code_returns_output():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(set(s))
"""
    result = await run_code(code, "abc")
    assert result["error_type"] is None
    assert result["actual"] == "3"
    assert result["stderr"] == ""


@pytest.mark.asyncio
async def test_syntax_error():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(s  # missing paren
"""
    result = await run_code(code, "abc")
    assert result["error_type"] == "syntax_error"
    assert result["actual"] is None
    assert "SyntaxError" in result["stderr"]


@pytest.mark.asyncio
async def test_runtime_error():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return s[999]
"""
    result = await run_code(code, "abc")
    assert result["error_type"] == "runtime_error"
    assert result["actual"] is None


@pytest.mark.asyncio
async def test_no_return():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass
"""
    result = await run_code(code, "abc")
    assert result["error_type"] == "no_return"
    assert result["actual"] is None


@pytest.mark.asyncio
async def test_forbidden_import_os():
    code = """
import os
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return 1
"""
    result = await run_code(code, "abc")
    assert result["error_type"] == "runtime_error"
    assert "os" in result["stderr"]


@pytest.mark.asyncio
async def test_timeout():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        while True:
            pass
"""
    result = await run_code(code, "abc", timeout=1.0)
    assert result["error_type"] == "runtime_error"
    assert "超時" in result["stderr"]
```

- [ ] **Step 2: 執行測試確認失敗**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_executor.py -v
```
Expected: `ModuleNotFoundError: No module named 'executor'`

- [ ] **Step 3: 實作 executor.py**

`backend/executor.py`:
```python
import asyncio
import sys

FORBIDDEN_MODULES = ["os", "sys", "subprocess", "socket"]


def check_forbidden(code: str) -> str | None:
    for module in FORBIDDEN_MODULES:
        if f"import {module}" in code:
            return f"不允許使用 {module} 模組"
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

    runner_script = f"""{code}

_sol = Solution()
_result = _sol.lengthOfLongestSubstring({repr(input_val)})
print(_result)
"""

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            runner_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
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
        proc.kill()
        await proc.wait()
        return {"actual": None, "error_type": "runtime_error", "stderr": "執行超時（超過時間限制）"}
```

- [ ] **Step 4: 執行測試確認通過**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_executor.py -v
```
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add backend/executor.py backend/tests/test_executor.py
git commit -m "feat: add async code executor with blacklist and timeout"
```

---

### Task 4: judge.py — 18 組測試案例比對

**Files:**
- Create: `backend/judge.py`
- Create: `backend/tests/test_judge.py`

- [ ] **Step 1: 撰寫失敗測試**

`backend/tests/test_judge.py`:
```python
import pytest
from judge import judge

CORRECT_CODE = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        left = 0
        result = 0
        for right, char in enumerate(s):
            if char in char_map and char_map[char] >= left:
                left = char_map[char] + 1
            char_map[char] = right
            result = max(result, right - left + 1)
        return result
"""

WRONG_CODE = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(s)
"""


@pytest.mark.asyncio
async def test_correct_code_all_pass():
    results = await judge(CORRECT_CODE)
    assert len(results) == 18
    assert all(r["passed"] for r in results)


@pytest.mark.asyncio
async def test_wrong_code_test2_fails():
    results = await judge(WRONG_CODE)
    assert len(results) == 18
    test2 = next(r for r in results if r["index"] == 2)
    assert not test2["passed"]
    assert test2["actual"] == "5"
    assert test2["expected"] == 1


@pytest.mark.asyncio
async def test_result_has_required_fields():
    results = await judge(WRONG_CODE)
    first = results[0]
    for field in ("index", "input", "expected", "actual", "passed", "error_type", "stderr"):
        assert field in first
```

- [ ] **Step 2: 執行測試確認失敗**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_judge.py -v
```
Expected: `ModuleNotFoundError: No module named 'judge'`

- [ ] **Step 3: 實作 judge.py**

`backend/judge.py`:
```python
from executor import run_code
from problem import TEST_CASES

_DISPLAY_MAX_LEN = 50


async def judge(code: str) -> list[dict]:
    """
    對全部 18 組 test case 執行學生程式碼並比對結果。
    永遠跑完全部，不中途停止（停在第一個失敗是前端的責任）。

    Returns:
        list[dict]: 18 筆結果，每筆包含
            index, input（截斷顯示）, expected, actual, passed, error_type, stderr
    """
    results = []
    for tc in TEST_CASES:
        timeout = 10.0 if tc["is_stress"] else 5.0
        exec_result = await run_code(code, tc["input"], timeout=timeout)

        actual = exec_result["actual"]
        passed = (actual == str(tc["expected"])) and exec_result["error_type"] is None

        display_input = (
            tc["input"]
            if len(tc["input"]) <= _DISPLAY_MAX_LEN
            else tc["input"][:_DISPLAY_MAX_LEN] + "..."
        )

        results.append(
            {
                "index": tc["index"],
                "input": display_input,
                "expected": tc["expected"],
                "actual": actual,
                "passed": passed,
                "error_type": exec_result["error_type"],
                "stderr": exec_result["stderr"],
            }
        )

    return results
```

- [ ] **Step 4: 執行測試確認通過**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_judge.py -v
```
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add backend/judge.py backend/tests/test_judge.py
git commit -m "feat: add judge running all 18 test cases"
```

---

### Task 5: ai.py — Groq Cloud API 整合（三種 prompt 分支）

**Files:**
- Create: `backend/ai.py`
- Create: `backend/tests/test_ai.py`

- [ ] **Step 1: 撰寫失敗測試**

`backend/tests/test_ai.py`:
```python
import pytest
from unittest.mock import AsyncMock, patch
from ai import build_prompt, get_hint


def make_result(index, input_val, expected, actual, passed, error_type=None, stderr=""):
    if passed:
        error_type = None
    return {
        "index": index,
        "input": input_val,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "error_type": error_type,
        "stderr": stderr,
    }


# --- build_prompt tests (no API call) ---

def test_build_prompt_all_passed_returns_none():
    results = [make_result(1, "abc", 3, "3", True)]
    assert build_prompt("code", results) is None


def test_build_prompt_syntax_error_uses_stderr():
    results = [
        make_result(1, "abc", 3, None, False, "syntax_error", "SyntaxError: invalid syntax (line 3)")
    ]
    prompt = build_prompt("code", results)
    assert "SyntaxError: invalid syntax (line 3)" in prompt
    assert "步驟一" not in prompt


def test_build_prompt_runtime_error_uses_stderr():
    results = [
        make_result(1, "abc", 3, None, False, "runtime_error", "IndexError: list index out of range")
    ]
    prompt = build_prompt("code", results)
    assert "IndexError: list index out of range" in prompt
    assert "步驟一" not in prompt


def test_build_prompt_no_return_mentions_return():
    results = [make_result(1, "abc", 3, None, False, "no_return")]
    prompt = build_prompt("code", results)
    assert "return" in prompt
    assert "步驟一" not in prompt


def test_build_prompt_wrong_answer_has_two_steps():
    # error_type=None means: ran successfully but returned wrong value
    results = [
        make_result(1, "abcabcbb", 3, "8", False, None),
        make_result(2, "bbbbb", 1, "5", False, None),
    ]
    prompt = build_prompt("code", results)
    assert "步驟一" in prompt
    assert "步驟二" in prompt


def test_build_prompt_wrong_answer_includes_all_failures():
    results = [
        make_result(1, "abcabcbb", 3, "3", True),       # passed
        make_result(2, "bbbbb", 1, "5", False, None),    # first fail (ran, wrong answer)
        make_result(3, "pwwkew", 3, "6", False, None),   # second fail
    ]
    prompt = build_prompt("code", results)
    # all failures should appear in the pattern section
    assert "bbbbb" in prompt
    assert "pwwkew" in prompt
    # first_fail is highlighted
    assert "5" in prompt  # actual of first fail


# --- get_hint tests (mock API) ---

@pytest.mark.asyncio
async def test_get_hint_returns_none_when_all_pass():
    results = [make_result(1, "abc", 3, "3", True)]
    hint = await get_hint("code", results)
    assert hint is None


@pytest.mark.asyncio
async def test_get_hint_calls_api_and_returns_content():
    results = [make_result(1, "abc", 3, "5", False, None)]  # ran fine, wrong answer

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "這是 AI 提示"

    with patch("ai.client.chat.completions.create", return_value=mock_response) as mock_create:
        hint = await get_hint("code", results)

    assert hint == "這是 AI 提示"
    mock_create.assert_called_once()
```

- [ ] **Step 2: 執行測試確認失敗**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_ai.py -v
```
Expected: `ModuleNotFoundError: No module named 'ai'`

- [ ] **Step 3: 實作 ai.py**

`backend/ai.py`:
```python
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1",
)


def build_prompt(code: str, results: list[dict]) -> str | None:
    """
    組裝 AI prompt。
    - 全部通過 → 回傳 None
    - 依 first_fail 的 error_type 選擇三種 prompt 分支
    """
    failed = [r for r in results if not r["passed"]]
    if not failed:
        return None

    first_fail = failed[0]
    error_type = first_fail["error_type"]

    if error_type in ("syntax_error", "runtime_error"):
        return f"""你是一個程式學習助教，目標是幫助大一學生學習 Python。

學生程式碼：
{code}

執行時發生錯誤，錯誤訊息如下：
{first_fail['stderr']}

請解釋這個錯誤訊息的意思，並引導學生找到並修正問題。

規則：
1. 不要直接給出修正後的程式碼
2. 用繁體中文回答，語氣友善鼓勵
3. 回答控制在 150 字以內"""

    if error_type == "no_return":
        return f"""你是一個程式學習助教，目標是幫助大一學生學習 Python。

學生程式碼：
{code}

問題：函式執行後回傳了 None，代表函式內沒有 return 語句或 return 沒有帶值。

請提醒學生函式需要回傳值，並說明 return 的用法。

規則：
1. 不要直接給出答案
2. 用繁體中文回答，語氣友善鼓勵
3. 回答控制在 100 字以內"""

    # wrong_answer：傳入所有失敗 cases 做 pattern 推斷
    failed_summary = "\n".join(
        f"- Input: {r['input']!r} / Expected: {r['expected']} / Actual: {r['actual']}"
        for r in failed
    )

    return f"""你是一個程式學習助教，目標是幫助大一學生學習 Python。

題目：Longest Substring Without Repeating Characters
學生程式碼：
{code}

所有失敗的測試案例（用來推斷錯誤 pattern）：
{failed_summary}

第一個失敗的測試案例（學生目前看到的）：
- Input：{first_fail['input']!r}
- 預期輸出：{first_fail['expected']}
- 實際輸出：{first_fail['actual']}

請依照以下兩個步驟回答：

【步驟一：推斷錯誤原因】
根據所有失敗案例的輸出 pattern，推斷學生的程式碼在邏輯上犯了什麼錯誤。
請說明你的推斷依據（例如：「'bbbbb' 回傳 5 而非 1，代表...」）。

【步驟二：給予引導提示】
根據步驟一的推斷，針對第一個失敗的測試案例給學生一個引導式提示。

規則：
1. 不要直接給出正確程式碼或答案
2. 提示要基於推斷出的錯誤原因，不是泛泛而談
3. 用繁體中文回答，語氣友善鼓勵
4. 整體回答控制在 200 字以內"""


async def get_hint(code: str, results: list[dict]) -> str | None:
    """呼叫 Groq Cloud API 取得 AI 提示。全部通過時回傳 None。"""
    prompt = build_prompt(code, results)
    if prompt is None:
        return None

    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
```

- [ ] **Step 4: 執行測試確認通過**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_ai.py -v
```
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add backend/ai.py backend/tests/test_ai.py
git commit -m "feat: add Groq Cloud API with 3-branch prompt logic"
```

---

### Task 6: main.py — FastAPI /submit endpoint

**Files:**
- Create: `backend/main.py`
- Create: `backend/tests/test_main.py`

- [ ] **Step 1: 撰寫失敗測試**

`backend/tests/test_main.py`:
```python
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from main import app

CORRECT_CODE = """
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        left = 0
        result = 0
        for right, char in enumerate(s):
            if char in char_map and char_map[char] >= left:
                left = char_map[char] + 1
            char_map[char] = right
            result = max(result, right - left + 1)
        return result
"""


@pytest.mark.asyncio
async def test_submit_returns_18_results_and_hint():
    with patch("main.get_hint", new_callable=AsyncMock, return_value="測試提示"):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/submit", json={"code": CORRECT_CODE})

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "hint" in data
    assert len(data["results"]) == 18


@pytest.mark.asyncio
async def test_submit_hint_none_when_all_pass():
    with patch("main.get_hint", new_callable=AsyncMock, return_value=None):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/submit", json={"code": CORRECT_CODE})

    assert response.json()["hint"] is None
```

- [ ] **Step 2: 執行測試確認失敗**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest tests/test_main.py -v
```
Expected: `ModuleNotFoundError: No module named 'main'`

- [ ] **Step 3: 實作 main.py**

`backend/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from judge import judge
from ai import get_hint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class SubmitRequest(BaseModel):
    code: str


@app.post("/submit")
async def submit(req: SubmitRequest):
    results = await judge(req.code)
    hint = await get_hint(req.code, results)
    return {"results": results, "hint": hint}
```

- [ ] **Step 4: 執行所有後端測試**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest -v
```
Expected: 全部通過（約 17 tests）

- [ ] **Step 5: 手動啟動確認**

```bash
cd /home/auxe/Desktop/畢業專題/backend
uvicorn main:app --reload --port 8000
```

```bash
curl -s -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"code": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        return len(s)"}' \
  | python3 -m json.tool | head -30
```
Expected: JSON 包含 `results`（18 筆）和 `hint`（字串）

- [ ] **Step 6: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add backend/main.py backend/tests/test_main.py
git commit -m "feat: add FastAPI /submit endpoint with CORS"
```

---

### Task 7: 前端專案建立

**Files:**
- Create: `frontend/` (Vite + Vue 3)

- [ ] **Step 1: 建立 Vue 專案**

```bash
cd /home/auxe/Desktop/畢業專題
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```

- [ ] **Step 2: 安裝依賴**

```bash
cd /home/auxe/Desktop/畢業專題/frontend
npm install axios @guolao/vue-monaco-editor
```

- [ ] **Step 3: 確認開發伺服器可啟動**

```bash
npm run dev
```
Expected: 終端顯示 `Local: http://localhost:5173/`，瀏覽器可開啟

- [ ] **Step 4: 清空預設樣板**

清空 `frontend/src/style.css`（保留空檔案），刪除 `frontend/src/assets/` 目錄，刪除 `frontend/src/components/HelloWorld.vue`，並將 `frontend/src/App.vue` 改為：

```vue
<template>
  <div>OK</div>
</template>
```

- [ ] **Step 5: 建立 components 目錄**

```bash
mkdir -p /home/auxe/Desktop/畢業專題/frontend/src/components
```

- [ ] **Step 6: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/
git commit -m "feat: scaffold Vue 3 frontend with Monaco Editor dep"
```

---

### Task 8: api.js — axios 呼叫後端

**Files:**
- Create: `frontend/src/api.js`

- [ ] **Step 1: 建立 api.js**

`frontend/src/api.js`:
```javascript
import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

export async function submitCode(code) {
  const response = await axios.post(`${BASE_URL}/submit`, { code })
  return response.data  // { results: [...], hint: string|null }
}
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/src/api.js
git commit -m "feat: add API client for /submit"
```

---

### Task 9: ProblemStatement.vue — 題目說明

**Files:**
- Create: `frontend/src/components/ProblemStatement.vue`

- [ ] **Step 1: 建立 ProblemStatement.vue**

`frontend/src/components/ProblemStatement.vue`:
```vue
<template>
  <div class="problem">
    <h1 class="problem-title">📋 {{ problem.title }}</h1>
    <p class="problem-desc" v-html="problem.description"></p>
    <div class="examples">
      <div v-for="(ex, i) in problem.examples" :key="i" class="example-card">
        <div class="example-label">📌 範例 {{ i + 1 }}</div>
        <div class="example-input">Input:&nbsp; s = "{{ ex.input }}"</div>
        <div class="example-output">Output: {{ ex.output }}</div>
        <div class="example-note">{{ ex.explanation }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  problem: { type: Object, required: true },
})
</script>

<style scoped>
.problem { padding: 28px 40px; border-bottom: 1px solid #313244; }
.problem-title { font-size: 24px; font-weight: bold; color: #cba6f7; margin-bottom: 14px; }
.problem-desc { font-size: 16px; line-height: 1.9; color: #cdd6f4; margin-bottom: 20px; }
.examples { display: flex; gap: 20px; flex-wrap: wrap; }
.example-card {
  background: #1e1e2e; border: 1px solid #45475a; border-radius: 10px;
  padding: 20px 24px; font-size: 15px; flex: 1; min-width: 220px;
}
.example-label { color: #89b4fa; font-weight: bold; font-size: 14px; margin-bottom: 12px; }
.example-input { color: #a6e3a1; font-family: monospace; font-size: 15px; margin-bottom: 6px; }
.example-output { color: #f9e2af; font-family: monospace; font-size: 15px; margin-bottom: 6px; }
.example-note { color: #6c7086; font-size: 13px; margin-top: 10px; padding-top: 10px; border-top: 1px solid #313244; }
</style>
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/src/components/ProblemStatement.vue
git commit -m "feat: add ProblemStatement component"
```

---

### Task 10: CodeEditor.vue — Monaco Editor

**Files:**
- Create: `frontend/src/components/CodeEditor.vue`

- [ ] **Step 1: 建立 CodeEditor.vue**

`frontend/src/components/CodeEditor.vue`:
```vue
<template>
  <div class="editor-section">
    <div class="section-label">✏️ 程式碼編輯器</div>
    <VueMonacoEditor
      v-model:value="code"
      language="python"
      theme="vs-dark"
      :options="editorOptions"
      style="height: 280px; border-radius: 10px; overflow: hidden; border: 1px solid #3e3e42;"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'

const props = defineProps({
  modelValue: { type: String, required: true },
})
const emit = defineEmits(['update:modelValue'])

const code = ref(props.modelValue)
watch(code, (val) => emit('update:modelValue', val))

const editorOptions = {
  fontSize: 15,
  lineHeight: 24,
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  tabSize: 4,
  insertSpaces: true,
  quickSuggestions: true,
  wordBasedSuggestions: true,
}
</script>

<style scoped>
.editor-section { padding: 28px 40px; border-bottom: 1px solid #313244; }
.section-label { font-size: 14px; color: #6c7086; margin-bottom: 14px; }
</style>
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/src/components/CodeEditor.vue
git commit -m "feat: add CodeEditor with Monaco Editor and Python autocomplete"
```

---

### Task 11: ResultPanel.vue — 測試結果與 AI 提示

前端顯示邏輯：收到完整 18 筆 results，只渲染到第一個失敗（含）為止。

**Files:**
- Create: `frontend/src/components/ResultPanel.vue`

- [ ] **Step 1: 建立 ResultPanel.vue**

`frontend/src/components/ResultPanel.vue`:
```vue
<template>
  <div v-if="results.length > 0">
    <div class="section">
      <div class="section-label">🧪 測試結果</div>
      <div
        v-for="result in visibleResults"
        :key="result.index"
        :class="['test-result', result.passed ? 'pass' : 'fail']"
      >
        <span :class="result.passed ? 'status-pass' : 'status-fail'">
          {{ result.passed ? '✓ PASS' : '✗ FAIL' }}
        </span>
        <span class="test-label">Test {{ result.index }}</span>
        <span class="test-input">Input: "{{ result.input }}"</span>
        <span class="test-exp">
          Expected: <strong class="expected-val">{{ result.expected }}</strong>
        </span>
        <span v-if="!result.passed">
          Got: <strong class="got-fail">{{ result.actual ?? 'Error' }}</strong>
        </span>
      </div>
    </div>

    <div v-if="hint" class="section">
      <div class="section-label">🤖 AI 學習提示</div>
      <div class="ai-hint">
        <div class="ai-hint-body">{{ hint }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  results: { type: Array, default: () => [] },
  hint: { type: String, default: null },
})

// 只顯示到第一個失敗（含），後面的不顯示
const visibleResults = computed(() => {
  const firstFailIdx = props.results.findIndex((r) => !r.passed)
  if (firstFailIdx === -1) return props.results
  return props.results.slice(0, firstFailIdx + 1)
})
</script>

<style scoped>
.section { padding: 28px 40px; border-bottom: 1px solid #313244; }
.section-label { font-size: 14px; color: #6c7086; margin-bottom: 14px; }
.test-result {
  background: #1e1e2e; border: 1px solid #313244; border-radius: 8px;
  padding: 14px 20px; display: flex; align-items: center; gap: 24px;
  font-size: 15px; margin-bottom: 10px;
}
.test-result.pass { border-left: 5px solid #a6e3a1; }
.test-result.fail { border-left: 5px solid #f38ba8; }
.status-pass { color: #a6e3a1; font-weight: bold; min-width: 70px; }
.status-fail { color: #f38ba8; font-weight: bold; min-width: 70px; }
.test-label { color: #6c7086; min-width: 70px; }
.test-input { color: #cdd6f4; font-family: monospace; }
.test-exp { color: #6c7086; }
.expected-val { color: #f9e2af; }
.got-fail { color: #f38ba8; }
.ai-hint { border: 1.5px solid #cba6f7; border-radius: 10px; padding: 24px 28px; }
.ai-hint-body { color: #cdd6f4; font-size: 16px; line-height: 2; white-space: pre-wrap; }
</style>
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/src/components/ResultPanel.vue
git commit -m "feat: add ResultPanel with sequential display and AI hint"
```

---

### Task 12: App.vue — 組裝所有元件

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: 更新 App.vue**

`frontend/src/App.vue`:
```vue
<template>
  <div class="app">
    <div class="topbar">
      <span class="topbar-title">🧠 Python 學習平台</span>
    </div>

    <ProblemStatement :problem="problem" />
    <CodeEditor v-model="code" />

    <div class="submit-section">
      <button class="submit-btn" :disabled="loading" @click="handleSubmit">
        {{ loading ? '⏳ 執行中...' : '▶ 提交程式碼' }}
      </button>
      <span class="submit-note">提交後系統自動執行，並由 AI 分析結果給予提示</span>
    </div>

    <ResultPanel :results="results" :hint="hint" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProblemStatement from './components/ProblemStatement.vue'
import CodeEditor from './components/CodeEditor.vue'
import ResultPanel from './components/ResultPanel.vue'
import { submitCode } from './api.js'

const STARTER_CODE = `class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 在此撰寫你的解法
        pass
`

const problem = {
  title: 'Longest Substring Without Repeating Characters',
  description: '給定一個字串 <code>s</code>，請找出不含重複字元的<strong>最長子字串</strong>的長度。',
  examples: [
    { input: 'abcabcbb', output: 3, explanation: '最長不重複子字串為 "abc"，長度為 3' },
    { input: 'bbbbb',    output: 1, explanation: '最長子字串為 "b"，長度為 1' },
    { input: 'pwwkew',   output: 3, explanation: '最長不重複子字串為 "wke"，長度為 3' },
  ],
}

const code    = ref(STARTER_CODE)
const results = ref([])
const hint    = ref(null)
const loading = ref(false)

async function handleSubmit() {
  loading.value = true
  results.value = []
  hint.value    = null
  try {
    const data    = await submitCode(code.value)
    results.value = data.results
    hint.value    = data.hint
  } catch (err) {
    console.error('Submit error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #11111b; font-family: 'Segoe UI', sans-serif; color: #cdd6f4; }
code { background: #313244; color: #a6e3a1; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 15px; }

.app { max-width: 960px; margin: 0 auto; }
.topbar { background: #181825; padding: 16px 40px; border-bottom: 1px solid #313244; }
.topbar-title { font-size: 22px; font-weight: bold; color: #cdd6f4; }
.submit-section { padding: 20px 40px; display: flex; align-items: center; border-bottom: 1px solid #313244; }
.submit-btn {
  background: #a6e3a1; color: #1e1e2e; padding: 14px 36px;
  border-radius: 8px; font-size: 16px; font-weight: bold;
  cursor: pointer; border: none;
}
.submit-btn:disabled { background: #45475a; color: #6c7086; cursor: not-allowed; }
.submit-note { color: #6c7086; font-size: 14px; margin-left: 18px; }
</style>
```

- [ ] **Step 2: Commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add frontend/src/App.vue
git commit -m "feat: wire all components in App.vue"
```

---

### Task 13: 最終驗證

- [ ] **Step 1: 執行所有後端測試**

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest -v
```
Expected: 全部通過

- [ ] **Step 2: 啟動後端與前端**

Terminal 1：
```bash
cd /home/auxe/Desktop/畢業專題/backend
uvicorn main:app --reload --port 8000
```

Terminal 2：
```bash
cd /home/auxe/Desktop/畢業專題/frontend
npm run dev
```

- [ ] **Step 3: 驗證 wrong_answer（sequential 顯示）**

在 `http://localhost:5173` 輸入：
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(s)
```
Expected：
- 顯示 Test 1 FAIL（"abcabcbb"，Got: 8，Expected: 3）
- Test 2 以後不顯示
- AI 提示出現，包含【步驟一】推斷與【步驟二】提示

- [ ] **Step 4: 驗證 no_return**

輸入：
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass
```
Expected：AI 提示說明需要 return 語句，Test 1 顯示 FAIL（Got: Error）

- [ ] **Step 5: 驗證 syntax_error**

輸入：
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(s
```
Expected：AI 提示解釋 SyntaxError，Test 1 顯示 FAIL

- [ ] **Step 6: 驗證全部通過**

輸入正確解法：
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        left = 0
        result = 0
        for right, char in enumerate(s):
            if char in char_map and char_map[char] >= left:
                left = char_map[char] + 1
            char_map[char] = right
            result = max(result, right - left + 1)
        return result
```
Expected：全部 18 組 PASS 顯示，無 AI 提示區塊

- [ ] **Step 7: 多人並發測試**

同時開兩個瀏覽器分頁，各自提交不同程式碼，確認兩者都正常收到結果不互相干擾。

- [ ] **Step 8: 最終 commit**

```bash
cd /home/auxe/Desktop/畢業專題
git add .
git commit -m "feat: complete Python learning platform MVP"
```
