<template>
  <div class="content-area">
    <div class="page-header-row">
      <h1 class="page-title" style="margin-bottom: 0;">Plugins</h1>
      <div class="page-header-actions">
        <input v-model="searchTerm" type="text" class="form-input page-search" placeholder="Search plugins, authors, or permissions" />
        <button class="btn btn-primary" @click="showModal = true">+ Add Plugin</button>
      </div>
    </div>

    <div class="grid grid-4" style="margin-bottom: 1rem;">
      <div class="stat-card">
        <div class="stat-value">{{ plugins.length }}</div>
        <div class="stat-label">Installed Plugins</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ enabledPlugins.length }}</div>
        <div class="stat-label">Enabled</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ permissionCount }}</div>
        <div class="stat-label">Unique Permissions</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ authorCount }}</div>
        <div class="stat-label">Maintainers</div>
      </div>
    </div>

    <div class="tabs wrap-tabs">
      <div class="tab" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">
        All ({{ plugins.length }})
      </div>
      <div class="tab" :class="{ active: activeTab === 'enabled' }" @click="activeTab = 'enabled'">
        Enabled ({{ enabledPlugins.length }})
      </div>
      <div class="tab" :class="{ active: activeTab === 'disabled' }" @click="activeTab = 'disabled'">
        Disabled ({{ disabledPlugins.length }})
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Plugin Inventory</h3>
          <span class="badge">{{ displayedPlugins.length }} visible</span>
        </div>

        <div v-if="displayedPlugins.length">
          <div v-for="plugin in displayedPlugins" :key="plugin.id" class="plugin-item plugin-item-detailed">
            <div class="plugin-info align-start">
              <div class="plugin-icon">🔌</div>
              <div>
                <div class="plugin-name">{{ plugin.name }}</div>
                <div class="plugin-version">v{{ plugin.version }} by {{ plugin.author || 'Unknown' }}</div>
                <div class="plugin-description">
                  {{ plugin.description || 'No description provided.' }}
                </div>
                <div class="command-meta" style="margin-top: 0.75rem;">
                  <span v-if="plugin.permissions.length === 0" class="badge">No declared permissions</span>
                  <span v-for="permission in plugin.permissions" :key="permission" class="badge">
                    {{ permission }}
                  </span>
                </div>
              </div>
            </div>
            <label class="plugin-toggle">
              <input
                type="checkbox"
                :checked="plugin.enabled"
                @change="togglePlugin(plugin.id, ($event.target as HTMLInputElement).checked)"
              />
              <span class="slider"></span>
            </label>
          </div>
        </div>

        <div v-else class="empty-state compact-empty-state">
          <p>No plugins match the current filters.</p>
        </div>
      </div>

      <div class="section-stack">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Permission Coverage</h3>
          </div>

          <div v-if="permissionSummary.length" class="list-stack">
            <div v-for="item in permissionSummary" :key="item.permission" class="list-row">
              <div>
                <div class="plugin-name">{{ item.permission }}</div>
                <div class="plugin-version">Used across plugin integrations</div>
              </div>
              <span class="badge badge-success">{{ item.count }}</span>
            </div>
          </div>

          <div v-else class="empty-state compact-empty-state">
            <p>No plugin permissions declared yet.</p>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Operational Summary</h3>
          </div>

          <div class="list-stack">
            <div class="list-row">
              <span>Enabled Share</span>
              <span class="badge badge-success">{{ enabledShare }}</span>
            </div>
            <div class="list-row">
              <span>Disabled Plugins</span>
              <span class="badge badge-warning">{{ disabledPlugins.length }}</span>
            </div>
            <div class="list-row">
              <span>Search Matches</span>
              <span class="badge">{{ displayedPlugins.length }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">Add Plugin</h3>
          <button class="modal-close" @click="showModal = false">&times;</button>
        </div>

        <div class="form-group">
          <label class="form-label">Plugin Name</label>
          <input type="text" class="form-input" v-model="newPlugin.name" />
        </div>

        <div class="form-group">
          <label class="form-label">Version</label>
          <input type="text" class="form-input" v-model="newPlugin.version" placeholder="1.0.0" />
        </div>

        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea class="form-input" v-model="newPlugin.description"></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Author</label>
          <input type="text" class="form-input" v-model="newPlugin.author" />
        </div>

        <button class="btn btn-primary" style="width: 100%;" @click="registerPlugin">
          Install Plugin
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const activeTab = ref('all')
const searchTerm = ref('')
const showModal = ref(false)
const newPlugin = reactive({
  name: '',
  version: '1.0.0',
  description: '',
  author: ''
})

const plugins = computed(() => store.plugins)
const enabledPlugins = computed(() => store.enabledPlugins)
const disabledPlugins = computed(() => store.disabledPlugins)
const permissionCount = computed(() => store.pluginPermissionCount)
const authorCount = computed(() => new Set(store.plugins.map((plugin) => plugin.author).filter(Boolean)).size)

const displayedPlugins = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  const source = activeTab.value === 'enabled'
    ? enabledPlugins.value
    : activeTab.value === 'disabled'
      ? disabledPlugins.value
      : plugins.value

  return source.filter((plugin) => {
    if (!query) return true
    const haystack = [
      plugin.name,
      plugin.author,
      plugin.description,
      plugin.permissions.join(' ')
    ].join(' ').toLowerCase()

    return haystack.includes(query)
  })
})

const permissionSummary = computed(() => {
  const counts = new Map<string, number>()

  store.plugins.forEach((plugin) => {
    plugin.permissions.forEach((permission) => {
      counts.set(permission, (counts.get(permission) || 0) + 1)
    })
  })

  return Array.from(counts.entries())
    .map(([permission, count]) => ({ permission, count }))
    .sort((left, right) => right.count - left.count)
    .slice(0, 8)
})

const enabledShare = computed(() => {
  if (plugins.value.length === 0) return '0%'
  return `${Math.round((enabledPlugins.value.length / plugins.value.length) * 100)}%`
})

async function togglePlugin(id: string, enabled: boolean) {
  if (enabled) {
    await store.enablePlugin(id)
  } else {
    await store.disablePlugin(id)
  }
}

async function registerPlugin() {
  if (!newPlugin.name || !newPlugin.version) return

  await store.registerPlugin(
    newPlugin.name,
    newPlugin.version,
    newPlugin.description,
    newPlugin.author,
    []
  )

  newPlugin.name = ''
  newPlugin.version = '1.0.0'
  newPlugin.description = ''
  newPlugin.author = ''
  showModal.value = false
}
</script>
