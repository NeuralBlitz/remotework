<template>
  <div class="content-area">
    <h1 class="page-title">OS Swap - Next Generation Virtualization</h1>
    
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">🔥 OS Swap Engine</h3>
        <span class="badge badge-success">{{ status }}</span>
      </div>
      
      <p style="color: var(--text-secondary); margin-bottom: 1rem;">
        Revolutionary operating system virtualization that allows seamless OS switching, 
        containerized environments, and instant OS provisioning.
      </p>
      
      <div class="grid grid-3" style="margin-top: 1.5rem;">
        <div class="stat-card" style="text-align: center;">
          <div class="stat-value">{{ virtualMachines.length }}</div>
          <div class="stat-label">Virtual Machines</div>
        </div>
        <div class="stat-card" style="text-align: center;">
          <div class="stat-value">{{ containers.length }}</div>
          <div class="stat-label">Containers</div>
        </div>
        <div class="stat-card" style="text-align: center;">
          <div class="stat-value">{{ snapshots.length }}</div>
          <div class="stat-label">Snapshots</div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-2" style="margin-top: 1rem;">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">🖥️ Virtual Machines</h3>
          <button class="btn btn-primary" @click="showVMModal = true">+ New VM</button>
        </div>
        
        <div v-if="virtualMachines.length === 0" class="empty-state" style="padding: 1rem;">
          <p>No virtual machines</p>
        </div>
        
        <div v-else>
          <div v-for="vm in virtualMachines" :key="vm.id" class="plugin-item">
            <div class="plugin-info">
              <div class="plugin-icon" style="background: linear-gradient(135deg, #10b981, #06b6d4);">🖥️</div>
              <div>
                <div class="plugin-name">{{ vm.name }}</div>
                <div class="plugin-version">{{ vm.os }} - {{ vm.memory }} RAM - {{ vm.vcpu }} vCPU</div>
              </div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
              <button 
                class="btn btn-secondary" 
                @click="toggleVM(vm.id)"
                :style="{ background: vm.running ? '#ef4444' : '' }"
              >
                {{ vm.running ? 'Stop' : 'Start' }}
              </button>
              <button class="btn btn-secondary" @click="snapshotVM(vm.id)">📸</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">📦 Containers</h3>
          <button class="btn btn-primary" @click="showContainerModal = true">+ New Container</button>
        </div>
        
        <div v-if="containers.length === 0" class="empty-state" style="padding: 1rem;">
          <p>No containers</p>
        </div>
        
        <div v-else>
          <div v-for="container in containers" :key="container.id" class="plugin-item">
            <div class="plugin-info">
              <div class="plugin-icon" style="background: linear-gradient(135deg, #6366f1, #8b5cf6);">📦</div>
              <div>
                <div class="plugin-name">{{ container.name }}</div>
                <div class="plugin-version">{{ container.image }} - {{ container.status }}</div>
              </div>
            </div>
            <button class="btn btn-secondary" @click="removeContainer(container.id)">🗑️</button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card" style="margin-top: 1rem;">
      <div class="card-header">
        <h3 class="card-title">📸 Snapshots</h3>
      </div>
      
      <div v-if="snapshots.length === 0" class="empty-state">
        <div class="empty-icon">📸</div>
        <p>No snapshots available</p>
      </div>
      
      <div v-else class="command-list">
        <div v-for="snap in snapshots" :key="snap.id" class="command-item">
          <div class="command-name">{{ snap.name }}</div>
          <div class="command-desc">{{ snap.vm }} - {{ snap.date }}</div>
        </div>
      </div>
    </div>
    
    <div class="card" style="margin-top: 1rem;">
      <div class="card-header">
        <h3 class="card-title">🚀 Quick Actions</h3>
      </div>
      
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <button class="btn btn-primary" @click="startAllVMs">Start All VMs</button>
        <button class="btn btn-secondary" @click="stopAllVMs">Stop All VMs</button>
        <button class="btn btn-secondary" @click="cleanupContainers">Cleanup Containers</button>
        <button class="btn btn-secondary" @click="optimizeStorage">Optimize Storage</button>
      </div>
    </div>
    
    <div v-if="showVMModal" class="modal-overlay" @click.self="showVMModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">Create Virtual Machine</h3>
          <button class="modal-close" @click="showVMModal = false">&times;</button>
        </div>
        
        <div class="form-group">
          <label class="form-label">Name</label>
          <input type="text" class="form-input" v-model="newVM.name" />
        </div>
        
        <div class="form-group">
          <label class="form-label">Operating System</label>
          <select class="form-input" v-model="newVM.os">
            <option value="Ubuntu 22.04">Ubuntu 22.04</option>
            <option value="Ubuntu 20.04">Ubuntu 20.04</option>
            <option value="Debian 11">Debian 11</option>
            <option value="CentOS 8">CentOS 8</option>
            <option value="Windows 11">Windows 11</option>
            <option value="Arch Linux">Arch Linux</option>
          </select>
        </div>
        
        <div class="grid grid-2">
          <div class="form-group">
            <label class="form-label">Memory (GB)</label>
            <input type="number" class="form-input" v-model="newVM.memory" />
          </div>
          <div class="form-group">
            <label class="form-label">vCPUs</label>
            <input type="number" class="form-input" v-model="newVM.vcpu" />
          </div>
        </div>
        
        <button class="btn btn-primary" style="width: 100%;" @click="createVM">
          Create VM
        </button>
      </div>
    </div>
    
    <div v-if="showContainerModal" class="modal-overlay" @click.self="showContainerModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">Create Container</h3>
          <button class="modal-close" @click="showContainerModal = false">&times;</button>
        </div>
        
        <div class="form-group">
          <label class="form-label">Name</label>
          <input type="text" class="form-input" v-model="newContainer.name" />
        </div>
        
        <div class="form-group">
          <label class="form-label">Image</label>
          <input type="text" class="form-input" v-model="newContainer.image" placeholder="ubuntu:22.04" />
        </div>
        
        <button class="btn btn-primary" style="width: 100%;" @click="createContainer">
          Create Container
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const status = ref('Ready')

const showVMModal = ref(false)
const showContainerModal = ref(false)

const virtualMachines = ref([
  { id: '1', name: 'mito-ubuntu-1', os: 'Ubuntu 22.04', memory: '4GB', vcpu: 2, running: false },
  { id: '2', name: 'mito-dev-env', os: 'Arch Linux', memory: '8GB', vcpu: 4, running: true }
])

const containers = ref([
  { id: '1', name: 'mito-api-server', image: 'mito:latest', status: 'Running' },
  { id: '2', name: 'mito-worker-1', image: 'python:3.11', status: 'Running' }
])

const snapshots = ref([
  { id: '1', name: 'mito-ubuntu-clean', vm: 'mito-ubuntu-1', date: '2024-01-15' }
])

const newVM = reactive({
  name: '',
  os: 'Ubuntu 22.04',
  memory: 4,
  vcpu: 2
})

const newContainer = reactive({
  name: '',
  image: ''
})

function toggleVM(id: string) {
  const vm = virtualMachines.value.find(v => v.id === id)
  if (vm) {
    vm.running = !vm.running
  }
}

function snapshotVM(id: string) {
  const vm = virtualMachines.value.find(v => v.id === id)
  if (vm) {
    snapshots.value.unshift({
      id: Date.now().toString(),
      name: `${vm.name}-snap-${Date.now()}`,
      vm: vm.name,
      date: new Date().toISOString().split('T')[0]
    })
  }
}

function createVM() {
  if (newVM.name) {
    virtualMachines.value.push({
      id: Date.now().toString(),
      name: newVM.name,
      os: newVM.os,
      memory: `${newVM.memory}GB`,
      vcpu: newVM.vcpu,
      running: false
    })
    newVM.name = ''
    showVMModal.value = false
  }
}

function createContainer() {
  if (newContainer.name && newContainer.image) {
    containers.value.push({
      id: Date.now().toString(),
      name: newContainer.name,
      image: newContainer.image,
      status: 'Running'
    })
    newContainer.name = ''
    newContainer.image = ''
    showContainerModal.value = false
  }
}

function removeContainer(id: string) {
  containers.value = containers.value.filter(c => c.id !== id)
}

function startAllVMs() {
  virtualMachines.value.forEach(vm => vm.running = true)
}

function stopAllVMs() {
  virtualMachines.value.forEach(vm => vm.running = false)
}

function cleanupContainers() {
  containers.value = []
}

function optimizeStorage() {
  console.log('Optimizing storage...')
}
</script>
