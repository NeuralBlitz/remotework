<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">M</div>
          <span class="logo-text">Mito</span>
        </div>
      </div>

      <nav class="nav-menu">
        <div class="nav-section">
          <div class="nav-section-title">Main</div>
          <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
            <span class="nav-icon">📊</span>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/commands" class="nav-item" :class="{ active: $route.path === '/commands' }">
            <span class="nav-icon">⚡</span>
            <span>Commands</span>
          </router-link>
          <router-link to="/terminal" class="nav-item" :class="{ active: $route.path === '/terminal' }">
            <span class="nav-icon">💻</span>
            <span>Terminal</span>
          </router-link>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Extensions</div>
          <router-link to="/plugins" class="nav-item" :class="{ active: $route.path === '/plugins' }">
            <span class="nav-icon">🧩</span>
            <span>Plugins</span>
          </router-link>
          <router-link to="/os" class="nav-item" :class="{ active: $route.path === '/os' }">
            <span class="nav-icon">🔄</span>
            <span>OS Swap</span>
          </router-link>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">System</div>
          <router-link to="/settings" class="nav-item" :class="{ active: $route.path === '/settings' }">
            <span class="nav-icon">⚙️</span>
            <span>Settings</span>
          </router-link>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="nav-item" style="cursor: default;">
          <span class="nav-icon">💜</span>
          <span>v{{ appInfo?.version || '1.0.0' }}</span>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div>
          <div class="top-bar-title">Command Center</div>
          <div class="top-bar-subtitle">Search routes, launch commands, and monitor activity in one place.</div>
        </div>

        <div class="top-bar-controls">
          <button class="search-box palette-trigger" @click="openPalette()">
            <span>⌘K</span>
            <span class="palette-placeholder">Search commands, routes, or plugins</span>
          </button>

          <div class="top-bar-metrics">
            <span class="badge badge-success">{{ successfulRunsToday }} runs today</span>
            <span class="badge badge-warning">{{ favoriteCount }} favorites</span>
          </div>
        </div>
      </header>

      <router-view />
    </main>

    <div v-if="showPalette" class="modal-overlay" @click.self="closePalette">
      <div class="modal palette-modal">
        <div class="palette-header">
          <input
            ref="paletteInput"
            v-model="paletteQuery"
            class="palette-input"
            type="text"
            placeholder="Type a command name, description, or route"
          />
          <button class="modal-close" @click="closePalette">&times;</button>
        </div>

        <div class="palette-section">
          <div class="palette-section-title">Navigation</div>
          <button
            v-for="item in filteredRoutes"
            :key="item.path"
            class="palette-item"
            @click="navigateTo(item.path)"
          >
            <div>
              <div class="palette-item-title">{{ item.label }}</div>
              <div class="palette-item-subtitle">{{ item.description }}</div>
            </div>
            <span class="badge">Route</span>
          </button>
        </div>

        <div class="palette-section">
          <div class="palette-section-title">Commands</div>
          <button
            v-for="command in filteredCommands"
            :key="command.name"
            class="palette-item"
            @click="launchCommand(command.name)"
          >
            <div>
              <div class="palette-item-title">{{ command.name }}</div>
              <div class="palette-item-subtitle">{{ command.description }}</div>
            </div>
            <span class="badge" :class="isFavorite(command.name) ? 'badge-success' : ''">
              {{ isFavorite(command.name) ? 'Favorite' : command.category }}
            </span>
          </button>
          <div v-if="filteredCommands.length === 0 && filteredRoutes.length === 0" class="empty-state compact-empty-state">
            <p>No matches found.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore, type Command } from '@/stores/app'

const router = useRouter()
const store = useAppStore()

const showPalette = ref(false)
const paletteQuery = ref('')
const paletteInput = ref<HTMLInputElement | null>(null)

const routes = [
  { path: '/', label: 'Dashboard', description: 'System overview, analytics, and recent activity.' },
  { path: '/commands', label: 'Commands', description: 'Explore, favorite, and execute command workflows.' },
  { path: '/terminal', label: 'Terminal', description: 'Run ad hoc commands and inspect output.' },
  { path: '/plugins', label: 'Plugins', description: 'Manage integrations, permissions, and plugin health.' },
  { path: '/os', label: 'OS Swap', description: 'Operate virtual machines, containers, and snapshots.' },
  { path: '/settings', label: 'Settings', description: 'Adjust defaults, server behavior, and storage.' }
]

const appInfo = computed(() => store.appInfo)
const successfulRunsToday = computed(() => store.successfulRunsToday)
const favoriteCount = computed(() => store.favoriteCommands.length)

const filteredRoutes = computed(() => {
  const query = paletteQuery.value.trim().toLowerCase()
  if (!query) return routes

  return routes.filter((item) => {
    const haystack = `${item.label} ${item.description}`.toLowerCase()
    return haystack.includes(query)
  })
})

const filteredCommands = computed(() => {
  const query = paletteQuery.value.trim().toLowerCase()
  const commands = store.commands.slice()

  const sorted = commands.sort((left, right) => {
    const leftFav = store.favoriteCommands.includes(left.name) ? 1 : 0
    const rightFav = store.favoriteCommands.includes(right.name) ? 1 : 0
    if (leftFav !== rightFav) return rightFav - leftFav
    return left.name.localeCompare(right.name)
  })

  if (!query) return sorted.slice(0, 8)

  return sorted.filter((command) => {
    const haystack = `${command.name} ${command.description} ${command.category}`.toLowerCase()
    return haystack.includes(query)
  }).slice(0, 8)
})

function isFavorite(name: string) {
  return store.favoriteCommands.includes(name)
}

function openPalette(query = '') {
  paletteQuery.value = query
  showPalette.value = true

  nextTick(() => {
    paletteInput.value?.focus()
  })
}

function closePalette() {
  showPalette.value = false
  paletteQuery.value = ''
}

function navigateTo(path: string) {
  closePalette()
  router.push(path)
}

async function launchCommand(name: string) {
  const command = store.commands.find((item) => item.name === name)
  if (!command) return

  closePalette()

  if (command.args.some((arg) => arg.required)) {
    router.push({ path: '/commands', query: { command: command.name } })
    return
  }

  await store.runCommand(command.name, [])
  router.push('/terminal')
}

function handleGlobalKeydown(event: KeyboardEvent) {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    openPalette()
    return
  }

  if (event.key === 'Escape' && showPalette.value) {
    closePalette()
  }
}

onMounted(async () => {
  store.loadPersistedState()
  await store.loadAppInfo()
  await store.loadCommands()
  await store.loadPlugins()
  window.addEventListener('keydown', handleGlobalKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<style scoped>
.sidebar-footer {
  border-top: 1px solid var(--border);
  padding-top: 1rem;
  margin-top: auto;
}
</style>
