# Python 學習平台 — 專題說明

## 專案概述

給大一學生的 Python 程式學習平台（LeetCode 風格）。學生提交程式碼後，系統執行程式碼、比對 18 組測試案例，Groq AI 分析錯誤 pattern 並給予引導式提示（不直接給答案）。

目前只有一題：**Longest Substring Without Repeating Characters（LeetCode #3）**

## 啟動方式

**後端（Terminal 1）：**
```bash
cd /home/auxe/Desktop/畢業專題/backend
uvicorn main:app --reload --port 8000
```

**前端（Terminal 2）：**
```bash
cd /home/auxe/Desktop/畢業專題/frontend
npm run dev
# 通常在 http://localhost:5173 或 5174（若 5173 被占用）
```

## 目錄結構

```
畢業專題/
├── backend/
│   ├── main.py          # FastAPI app，POST /submit（唯一 endpoint）
│   ├── executor.py      # asyncio subprocess 執行學生程式碼 + AST 安全過濾
│   ├── judge.py         # 18 組 test case 比對，回傳完整 results 陣列
│   ├── ai.py            # Groq Cloud API（llama-3.1-8b-instant），3 種 prompt 分支
│   ├── problem.py       # 題目定義 + 18 組 TEST_CASES
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env             # GROQ_API_KEY=gsk_... （不 commit）
│   └── tests/
│       ├── test_executor.py
│       ├── test_judge.py
│       ├── test_ai.py
│       └── test_main.py
└── frontend/
    ├── index.html
    └── src/
        ├── App.vue          # 左右兩欄佈局，handleSubmit，全域樣式
        ├── api.js           # axios POST /submit
        └── components/
            ├── ProblemStatement.vue  # 題目 + 3 個範例卡片
            ├── CodeEditor.vue        # Monaco Editor（Python，vs-dark）
            └── ResultPanel.vue       # 測試結果（到第一個失敗為止）+ AI 提示
```

## 執行測試

```bash
cd /home/auxe/Desktop/畢業專題/backend
pytest -v        # 19 tests，約 3-4 秒
```

## 關鍵架構決策

- **後端跑全部 18 筆 test case**，前端只渲染到第一個失敗（含）為止
- AI prompt 有 3 個分支：`syntax_error/runtime_error` → stderr 說明；`no_return` → 提醒 return；`wrong_answer`（error_type=None）→ 傳所有失敗 cases 做 pattern 推斷 + 2 步驟回答
- executor 用 AST 過濾禁止模組（os, sys, subprocess, socket 等），用 `start_new_session=True` + `os.killpg` 確保 timeout 時整個 process group 都被 kill

## 環境設定

```bash
# backend/.env（必填）
GROQ_API_KEY=gsk_...  # 從 console.groq.com/keys 取得

# Python venv（若需要）
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

## AI / Groq 設定

- **Provider：** Groq Cloud（`https://api.groq.com/openai/v1`）
- **Model：** `llama-3.1-8b-instant`（免費額度最多：500k tokens/day）
- **SDK：** openai Python SDK（OpenAI 相容格式）
- **注意：** openai SDK 的 `@required_args` decorator 會影響 mock，`ai.py` 用 `inspect.isawaitable` workaround

## CORS

後端允許所有 `localhost:*` port（regex），Vite 換 port 不需要改設定：
```python
allow_origin_regex=r"http://localhost:\d+"
```

## 前端樣式

- **設計：** Warm Terminal 美學，IBM Plex Mono 統一全站字型
- **配色：** CSS 變數定義在 App.vue `<style>`，amber accent（`--amber: #dfa050`）
- **佈局：** 左欄（題目+編輯器+提交），右欄 sticky 500px（結果+AI 提示）

## 設計規格與計畫

- Spec：`docs/superpowers/specs/2026-04-08-leetcode-learning-platform-design.md`
- Plan：`docs/superpowers/plans/2026-04-09-learning-platform.md`
