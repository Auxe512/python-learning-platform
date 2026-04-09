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
