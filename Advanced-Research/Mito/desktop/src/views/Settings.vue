<template>
  <div class="content-area">
    <h1 class="page-title">Settings</h1>
    
    <div class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">General</h3>
        </div>
        
        <div class="form-group">
          <label class="form-label">Theme</label>
          <select class="form-input" v-model="settings.theme">
            <option value="dark">Dark</option>
            <option value="light">Light</option>
            <option value="auto">Auto</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Language</label>
          <select class="form-input" v-model="settings.language">
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Default Model</label>
          <input type="text" class="form-input" v-model="settings.defaultModel" />
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">API Server</h3>
        </div>
        
        <div class="form-group">
          <label class="form-label">Host</label>
          <input type="text" class="form-input" v-model="settings.apiHost" />
        </div>
        
        <div class="form-group">
          <label class="form-label">Port</label>
          <input type="number" class="form-input" v-model="settings.apiPort" />
        </div>
        
        <div class="form-group">
          <label class="form-label">Rate Limit (requests/min)</label>
          <input type="number" class="form-input" v-model="settings.rateLimit" />
        </div>
      </div>
    </div>
    
    <div class="card" style="margin-top: 1rem;">
      <div class="card-header">
        <h3 class="card-title">Storage</h3>
      </div>
      
      <div class="grid grid-2">
        <div class="form-group">
          <label class="form-label">Models Directory</label>
          <input type="text" class="form-input" v-model="settings.modelsDir" />
        </div>
        
        <div class="form-group">
          <label class="form-label">Data Directory</label>
          <input type="text" class="form-input" v-model="settings.dataDir" />
        </div>
      </div>
      
      <button class="btn btn-primary" @click="saveSettings">Save Settings</button>
    </div>
    
    <div class="card" style="margin-top: 1rem;">
      <div class="card-header">
        <h3 class="card-title">About</h3>
      </div>
      
      <div style="color: var(--text-secondary);">
        <p><strong>Mito AI Toolkit</strong></p>
        <p>Version: {{ appInfo?.version || '1.0.0' }}</p>
        <p style="margin-top: 0.5rem;">The Powerhouse AI Toolkit - A comprehensive AI solution for LLMs, transformers, vision, speech, and more.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const appInfo = computed(() => store.appInfo)

const settings = reactive({
  theme: 'dark',
  language: 'en',
  defaultModel: 'gpt2',
  apiHost: '0.0.0.0',
  apiPort: 8000,
  rateLimit: 100,
  modelsDir: './models',
  dataDir: './data'
})

function saveSettings() {
  console.log('Saving settings:', settings)
}
</script>
