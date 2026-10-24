<template>
  <div class="content-area">
    <div class="page-header-row">
      <h1 class="page-title" style="margin-bottom: 0;">Commands</h1>
      <div class="page-header-actions">
        <input v-model="searchTerm" type="text" class="form-input page-search" placeholder="Search commands or descriptions" />
      </div>
    </div>

    <div class="tabs wrap-tabs">
      <div class="tab" :class="{ active: selectedCategory === 'all' }" @click="selectedCategory = 'all'">
        All ({{ commands.length }})
      </div>
      <div
        v-for="(cmds, category) in commandsByCategory"
        :key="category"
        class="tab"
        :class="{ active: selectedCategory === category }"
        @click="selectedCategory = category"
      >
        {{ category }} ({{ cmds.length }})
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Command Catalog</h3>
          <span class="badge">{{ displayedCommands.length }} visible</span>
        </div>

        <div v-if="displayedCommands.length" class="command-list command-list-wide">
          <div
            v-for="cmd in displayedCommands"
            :key="cmd.name"
            class="command-item"
            @click="openCommandModal(cmd)"
          >
            <div class="command-card-header">
              <div class="command-name">{{ cmd.name }}</div>
              <button class="icon-button" @click.stop="toggleFavorite(cmd.name)" :title="isFavorite(cmd.name) ? 'Remove favorite' : 'Add favorite'">
                {{ isFavorite(cmd.name) ? '★' : '☆' }}
              </button>
            </div>
            <div class="command-desc">{{ cmd.description }}</div>
            <div class="command-meta">
              <span class="badge">{{ cmd.category }}</span>
              <span class="badge">{{ cmd.args.length }} args</span>
              <span class="badge badge-success">{{ commandUsage(cmd.name) }} runs</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state compact-empty-state">
          <p>No commands match the current filters.</p>
        </div>
      </div>

      <div class="section-stack">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Favorites</h3>
            <span class="badge badge-warning">{{ favoriteCommands.length }}</span>
          </div>

          <div v-if="favoriteCommands.length" class="list-stack">
            <div v-for="cmd in favoriteCommands" :key="cmd.name" class="list-row actionable-row" @click="openCommandModal(cmd)">
              <div>
                <div class="plugin-name">{{ cmd.name }}</div>
                <div class="plugin-version">{{ cmd.description }}</div>
              </div>
              <span class="badge badge-success">{{ commandUsage(cmd.name) }} runs</span>
            </div>
          </div>

          <div v-else class="empty-state compact-empty-state">
            <p>Favorite commands to build a reusable operator toolkit.</p>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Recent Runs</h3>
            <button class="btn btn-secondary" @click="router.push('/terminal')">Terminal</button>
          </div>

          <div v-if="recentEntries.length" class="list-stack">
            <div v-for="entry in recentEntries" :key="entry.id" class="list-row actionable-row" @click="reopenCommand(entry.command)">
              <div>
                <div class="plugin-name">{{ entry.command }}</div>
                <div class="plugin-version">{{ formatTimestamp(entry.timestamp) }}</div>
              </div>
              <span class="badge" :class="entry.status === 'success' ? 'badge-success' : 'badge-error'">{{ entry.status }}</span>
            </div>
          </div>

          <div v-else class="empty-state compact-empty-state">
            <p>No command history yet.</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-header">
          <div>
            <h3 class="modal-title">{{ selectedCommand?.name }}</h3>
            <div class="plugin-version">{{ selectedCommand?.category }}</div>
          </div>
          <button class="modal-close" @click="showModal = false">&times;</button>
        </div>

        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
          {{ selectedCommand?.description }}
        </p>

        <div class="command-meta" style="margin-bottom: 1rem;">
          <span class="badge badge-success">{{ commandUsage(selectedCommand?.name || '') }} runs</span>
          <button class="btn btn-secondary" @click="toggleFavorite(selectedCommand?.name || '')">
            {{ isFavorite(selectedCommand?.name || '') ? 'Unfavorite' : 'Add to Favorites' }}
          </button>
        </div>

        <div class="form-group" v-for="arg in selectedCommand?.args" :key="arg.name">
          <label class="form-label">
            {{ arg.name }}
            <span v-if="!arg.required" style="color: var(--text-secondary);">(optional)</span>
          </label>
          <input
            type="text"
            class="form-input"
            v-model="argValues[arg.name]"
            :placeholder="arg.default || ''"
          />
        </div>

        <button class="btn btn-primary" style="width: 100%;" @click="executeSelectedCommand">
          Execute
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore, type Command } from '@/stores/app'

const store = useAppStore()
const router = useRouter()
const route = useRoute()

const selectedCategory = ref('all')
const searchTerm = ref('')
const showModal = ref(false)
const selectedCommand = ref<Command | null>(null)
const argValues = reactive<Record<string, string>>({})

const commands = computed(() => store.commands)
const commandsByCategory = computed(() => store.commandsByCategory)
const favoriteCommands = computed(() => store.favoriteCommandDetails)
const recentEntries = computed(() => store.recentCommandEntries)

const displayedCommands = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  const source = selectedCategory.value === 'all'
    ? commands.value
    : commandsByCategory.value[selectedCategory.value] || []

  return source
    .filter((command) => {
      if (!query) return true
      const haystack = `${command.name} ${command.description} ${command.category}`.toLowerCase()
      return haystack.includes(query)
    })
    .sort((left, right) => {
      const leftFav = isFavorite(left.name) ? 1 : 0
      const rightFav = isFavorite(right.name) ? 1 : 0
      if (leftFav !== rightFav) return rightFav - leftFav
      return commandUsage(right.name) - commandUsage(left.name)
    })
})

function commandUsage(name: string) {
  return store.commandUsageMap[name] || 0
}

function isFavorite(name: string) {
  return store.favoriteCommands.includes(name)
}

function toggleFavorite(name: string) {
  if (!name) return
  store.toggleFavoriteCommand(name)
}

function openCommandModal(command: Command) {
  selectedCommand.value = command
  Object.keys(argValues).forEach((key) => delete argValues[key])
  command.args.forEach((arg) => {
    argValues[arg.name] = arg.default || ''
  })
  showModal.value = true
}

function reopenCommand(name: string) {
  const command = commands.value.find((item) => item.name === name)
  if (command) openCommandModal(command)
}

async function executeSelectedCommand() {
  if (!selectedCommand.value) return

  const args = selectedCommand.value.args
    .map((arg) => argValues[arg.name]?.trim())
    .filter((value): value is string => Boolean(value))

  await store.runCommand(selectedCommand.value.name, args)
  showModal.value = false
  router.push('/terminal')
}

function formatTimestamp(timestamp: string) {
  return new Date(timestamp).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

watch(
  () => [commands.value.length, route.query.command],
  () => {
    const requested = typeof route.query.command === 'string' ? route.query.command : ''
    if (!requested) return

    const command = commands.value.find((item) => item.name === requested)
    if (command) {
      openCommandModal(command)
      router.replace({ path: route.path, query: {} })
    }
  },
  { immediate: true }
)
</script>
