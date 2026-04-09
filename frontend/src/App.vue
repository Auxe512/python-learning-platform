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
