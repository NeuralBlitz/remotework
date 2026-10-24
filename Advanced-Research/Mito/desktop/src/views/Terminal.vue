<template>
  <div class="content-area">
    <h1 class="page-title">Terminal</h1>
    
    <div class="card">
      <div class="terminal" ref="terminalRef">
        <div v-for="(line, i) in terminalOutput" :key="i" class="terminal-output">
          {{ line }}
        </div>
        <div v-if="loading" class="terminal-output" style="color: var(--accent);">
          Running...
        </div>
      </div>
      
      <div class="terminal-input" style="margin-top: 1rem;">
        <span style="color: var(--accent);">$</span>
        <input 
          type="text" 
          v-model="command" 
          @keyup.enter="executeCommand"
          placeholder="Enter mito command..."
          :disabled="loading"
        />
        <button class="btn btn-primary" @click="executeCommand" :disabled="loading">
          Run
        </button>
        <button class="btn btn-secondary" @click="clearTerminal" :disabled="loading">
          Clear
        </button>
      </div>
    </div>
    
    <div class="card" style="margin-top: 1rem;">
      <div class="card-header">
        <h3 class="card-title">Available Commands</h3>
      </div>
      <div class="command-list">
        <div 
          v-for="cmd in commands" 
          :key="cmd.name" 
          class="command-item"
          @click="fillCommand(cmd.name)"
        >
          <div class="command-name">{{ cmd.name }}</div>
          <div class="command-desc">{{ cmd.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const command = ref('')
const terminalRef = ref<HTMLElement | null>(null)

const terminalOutput = computed(() => store.terminalOutput)
const commands = computed(() => store.commands)
const loading = computed(() => store.loading)

async function executeCommand() {
  if (!command.value.trim() || loading.value) return
  
  const parts = command.value.trim().split(' ')
  const cmd = parts[0]
  const args = parts.slice(1)
  
  await store.runCommand(cmd, args)
  command.value = ''
  
  await nextTick()
  if (terminalRef.value) {
    terminalRef.value.scrollTop = terminalRef.value.scrollHeight
  }
}

function fillCommand(name: string) {
  command.value = name + ' '
}

function clearTerminal() {
  store.clearTerminal()
}
</script>
