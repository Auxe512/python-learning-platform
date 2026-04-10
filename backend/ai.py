import os
import inspect
import openai
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
    - 依 first_fail 的 error_type 選擇三種 prompt 分支：
      * syntax_error / runtime_error → 簡化版，傳 stderr
      * no_return → 簡化版，提醒 return
      * None (wrong answer) → 完整版，傳所有失敗 cases 做 pattern 推斷
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

    # wrong_answer (error_type is None): use full pattern-analysis prompt
    # Guard: if error_type is unknown (not None), treat as runtime_error
    if error_type is not None:
        return f"""你是一個程式學習助教，目標是幫助大一學生學習 Python。

學生程式碼：
{code}

執行時發生錯誤，錯誤訊息如下：
{first_fail.get('stderr', '（錯誤訊息不可用）')}

請解釋這個錯誤訊息的意思，並引導學生找到並修正問題。

規則：
1. 不要直接給出修正後的程式碼
2. 用繁體中文回答，語氣友善鼓勵
3. 回答控制在 150 字以內"""

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
    """呼叫 Grok API 取得 AI 提示。全部通過時回傳 None。API 失敗時回傳 None。"""
    prompt = build_prompt(code, results)
    if prompt is None:
        return None

    try:
        result = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        response = await result if inspect.isawaitable(result) else result
        content = response.choices[0].message.content
        if content is None:
            return None
        return content
    except openai.OpenAIError:
        return None
