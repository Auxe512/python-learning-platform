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
