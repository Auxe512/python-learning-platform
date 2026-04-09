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
