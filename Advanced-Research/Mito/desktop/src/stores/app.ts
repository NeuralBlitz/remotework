import { defineStore } from 'pinia'
import { invoke } from '@tauri-apps/api/tauri'

export interface Command {
  name: string
  description: string
  category: string
  args: Array<{
    name: string
    required: boolean
    default: string | null
  }>
}

export interface Plugin {
  id: string
  name: string
  version: string
  description: string
  author: string
  enabled: boolean
  permissions: string[]
}

interface AppInfo {
  version: string
  name: string
  description: string
}

export interface CommandHistoryEntry {
  id: string
  command: string
  args: string[]
  status: 'success' | 'error'
  timestamp: string
  summary: string
}

const FAVORITES_KEY = 'mito.favoriteCommands'
const HISTORY_KEY = 'mito.commandHistory'

function isBrowser() {
  return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined'
}

function readPersistedList<T>(key: string, fallback: T): T {
  if (!isBrowser()) return fallback

  try {
    const raw = window.localStorage.getItem(key)
    return raw ? JSON.parse(raw) as T : fallback
  } catch {
    return fallback
  }
}

export const useAppStore = defineStore('app', {
  state: () => ({
    appInfo: null as AppInfo | null,
    commands: [] as Command[],
    plugins: [] as Plugin[],
    favoriteCommands: [] as string[],
    commandHistory: [] as CommandHistoryEntry[],
    loading: false,
    error: null as string | null,
    terminalOutput: [] as string[]
  }),

  actions: {
    loadPersistedState() {
      this.favoriteCommands = readPersistedList<string[]>(FAVORITES_KEY, [])
      this.commandHistory = readPersistedList<CommandHistoryEntry[]>(HISTORY_KEY, [])
    },

    persistState() {
      if (!isBrowser()) return

      window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(this.favoriteCommands))
      window.localStorage.setItem(HISTORY_KEY, JSON.stringify(this.commandHistory))
    },

    async loadAppInfo() {
      try {
        this.appInfo = await invoke('get_app_info')
      } catch (e) {
        console.error('Failed to load app info:', e)
        this.appInfo = { version: '1.0.0', name: 'Mito', description: 'AI Toolkit' }
      }
    },

    async loadCommands() {
      try {
        this.commands = await invoke('list_commands')
      } catch (e) {
        console.error('Failed to load commands:', e)
      }
    },

    async loadPlugins() {
      try {
        this.plugins = await invoke('list_plugins')
      } catch (e) {
        console.error('Failed to load plugins:', e)
      }
    },

    async executeCommand(command: string, args: Record<string, string>) {
      this.loading = true
      this.error = null
      const normalizedArgs = Object.values(args).filter(Boolean)

      try {
        const result = await invoke('execute_command', { command, args })
        this.terminalOutput.push(`$ mito ${command} ${normalizedArgs.join(' ')}`)
        this.terminalOutput.push(result as string)
        this.recordCommandExecution(command, normalizedArgs, 'success', result as string)
        return result
      } catch (e) {
        this.error = e as string
        this.terminalOutput.push(`Error: ${e}`)
        this.recordCommandExecution(command, normalizedArgs, 'error', String(e))
      } finally {
        this.loading = false
      }
    },

    async runCommand(command: string, args: string[]) {
      this.loading = true
      this.error = null

      try {
        const result = await invoke('run_mito_command', { command, args })
        this.terminalOutput.push(`$ mito ${command} ${args.join(' ')}`)
        this.terminalOutput.push(result as string)
        this.recordCommandExecution(command, args, 'success', result as string)
        return result
      } catch (e) {
        this.error = e as string
        this.terminalOutput.push(`Error: ${e}`)
        this.recordCommandExecution(command, args, 'error', String(e))
      } finally {
        this.loading = false
      }
    },

    async enablePlugin(id: string) {
      try {
        await invoke('enable_plugin', { id })
        const plugin = this.plugins.find((item) => item.id === id)
        if (plugin) plugin.enabled = true
      } catch (e) {
        console.error('Failed to enable plugin:', e)
      }
    },

    async disablePlugin(id: string) {
      try {
        await invoke('disable_plugin', { id })
        const plugin = this.plugins.find((item) => item.id === id)
        if (plugin) plugin.enabled = false
      } catch (e) {
        console.error('Failed to disable plugin:', e)
      }
    },

    async registerPlugin(name: string, version: string, description: string, author: string, permissions: string[]) {
      try {
        const plugin = await invoke('register_plugin', { name, version, description, author, permissions })
        this.plugins.push(plugin as Plugin)
      } catch (e) {
        console.error('Failed to register plugin:', e)
      }
    },

    toggleFavoriteCommand(name: string) {
      if (this.favoriteCommands.includes(name)) {
        this.favoriteCommands = this.favoriteCommands.filter((item) => item !== name)
      } else {
        this.favoriteCommands = [name, ...this.favoriteCommands]
      }

      this.persistState()
    },

    recordCommandExecution(command: string, args: string[], status: 'success' | 'error', summary: string) {
      const entry: CommandHistoryEntry = {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        command,
        args,
        status,
        timestamp: new Date().toISOString(),
        summary: summary.slice(0, 240)
      }

      this.commandHistory = [entry, ...this.commandHistory].slice(0, 50)
      this.persistState()
    },

    clearTerminal() {
      this.terminalOutput = []
    }
  },

  getters: {
    commandsByCategory: (state) => {
      const categories: Record<string, Command[]> = {}
      state.commands.forEach((command) => {
        if (!categories[command.category]) {
          categories[command.category] = []
        }
        categories[command.category].push(command)
      })
      return categories
    },

    favoriteCommandDetails: (state) =>
      state.favoriteCommands
        .map((name) => state.commands.find((command) => command.name === name))
        .filter((command): command is Command => Boolean(command)),

    commandUsageMap: (state) =>
      state.commandHistory.reduce<Record<string, number>>((acc, entry) => {
        acc[entry.command] = (acc[entry.command] || 0) + 1
        return acc
      }, {}),

    recentCommandEntries: (state) => state.commandHistory.slice(0, 8),

    successfulRunsToday: (state) => {
      const today = new Date().toISOString().slice(0, 10)
      return state.commandHistory.filter((entry) => entry.timestamp.startsWith(today) && entry.status === 'success').length
    },

    pluginPermissionCount: (state) => {
      const uniquePermissions = new Set<string>()
      state.plugins.forEach((plugin) => {
        plugin.permissions.forEach((permission) => uniquePermissions.add(permission))
      })
      return uniquePermissions.size
    },

    enabledPlugins: (state) => state.plugins.filter((plugin) => plugin.enabled),
    disabledPlugins: (state) => state.plugins.filter((plugin) => !plugin.enabled)
  }
})
