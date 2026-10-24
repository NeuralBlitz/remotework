<template>
  <div class="content-area">
    <h1 class="page-title">Dashboard</h1>

    <div class="grid grid-4" style="margin-bottom: 1.5rem;">
      <div class="stat-card">
        <div class="stat-value">{{ commands.length }}</div>
        <div class="stat-label">Commands</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ enabledPlugins }}</div>
        <div class="stat-label">Active Plugins</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ successfulRunsToday }}</div>
        <div class="stat-label">Successful Runs Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ favoriteCommands.length }}</div>
        <div class="stat-label">Favorite Commands</div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Launchpad</h3>
          <button class="btn btn-secondary" @click="router.push('/commands')">Open Commands</button>
        </div>

        <div class="command-list compact-command-list">
          <div
            v-for="cmd in launchpadCommands"
            :key="cmd.name"
            class="command-item"
            @click="runQuickCommand(cmd.name)"
          >
            <div class="command-card-header">
              <div class="command-name">{{ cmd.name }}</div>
              <span v-if="isFavorite(cmd.name)" class="badge badge-success">Favorite</span>
            </div>
            <div class="command-desc">{{ cmd.description }}</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">System Status</h3>
          <span class="badge badge-success">Healthy</span>
        </div>

        <div class="list-stack">
          <div class="list-row">
            <span>Command Categories</span>
            <span class="badge">{{ categoryCount }}</span>
          </div>
          <div class="list-row">
            <span>Plugin Permissions</span>
            <span class="badge">{{ pluginPermissionCount }}</span>
          </div>
          <div class="list-row">
            <span>Recent Failures</span>
            <span class="badge" :class="recentFailures === 0 ? 'badge-success' : 'badge-error'">{{ recentFailures }}</span>
          </div>
          <div class="list-row">
            <span>Tracked History</span>
            <span class="badge">{{ recentCommandEntries.length }} recent</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Most Used Commands</h3>
        </div>

        <div v-if="topCommands.length" class="list-stack">
          <div v-for="item in topCommands" :key="item.command.name" class="list-row actionable-row" @click="runQuickCommand(item.command.name)">
            <div>
              <div class="plugin-name">{{ item.command.name }}</div>
              <div class="plugin-version">{{ item.command.description }}</div>
            </div>
            <span class="badge badge-success">{{ item.count }} runs</span>
          </div>
        </div>

        <div v-else class="empty-state compact-empty-state">
          <p>No usage data yet. Run commands to generate analytics.</p>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Recent Activity</h3>
          <button class="btn btn-secondary" @click="router.push('/terminal')">Open Terminal</button>
        </div>

        <div v-if="recentCommandEntries.length" class="list-stack">
          <div v-for="entry in recentCommandEntries" :key="entry.id" class="list-row">
            <div>
              <div class="plugin-name">{{ entry.command }} {{ formatArgs(entry.args) }}</div>
              <div class="plugin-version">{{ formatTimestamp(entry.timestamp) }}</div>
            </div>
            <span class="badge" :class="entry.status === 'success' ? 'badge-success' : 'badge-error'">
              {{ entry.status }}
            </span>
          </div>
        </div>

        <div v-else class="empty-state compact-empty-state">
          <p>No recent activity. Run a command to populate this feed.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

const store = useAppStore()
const router = useRouter()

const commands = computed(() => store.commands)
const favoriteCommands = computed(() => store.favoriteCommandDetails)
const enabledPlugins = computed(() => store.enabledPlugins.length)
const successfulRunsToday = computed(() => store.successfulRunsToday)
const recentCommandEntries = computed(() => store.recentCommandEntries)
const pluginPermissionCount = computed(() => store.pluginPermissionCount)
const categoryCount = computed(() => Object.keys(store.commandsByCategory).length)
const recentFailures = computed(() => store.commandHistory.filter((entry) => entry.status === 'error').slice(0, 10).length)

const launchpadCommands = computed(() => {
  if (favoriteCommands.value.length) return favoriteCommands.value.slice(0, 6)
  return store.commands.slice(0, 6)
})

const topCommands = computed(() => {
  return store.commands
    .map((command) => ({ command, count: store.commandUsageMap[command.name] || 0 }))
    .filter((item) => item.count > 0)
    .sort((left, right) => right.count - left.count)
    .slice(0, 6)
})

function isFavorite(name: string) {
  return store.favoriteCommands.includes(name)
}

async function runQuickCommand(name: string) {
  const command = store.commands.find((item) => item.name === name)
  if (!command) return

  if (command.args.some((arg) => arg.required)) {
    router.push({ path: '/commands', query: { command: command.name } })
    return
  }

  await store.runCommand(name, [])
  router.push('/terminal')
}

function formatArgs(args: string[]) {
  return args.length ? args.join(' ') : ''
}

function formatTimestamp(timestamp: string) {
  return new Date(timestamp).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}
</script>
