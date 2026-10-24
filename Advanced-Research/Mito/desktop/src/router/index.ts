import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Commands from '@/views/Commands.vue'
import Plugins from '@/views/Plugins.vue'
import Terminal from '@/views/Terminal.vue'
import Settings from '@/views/Settings.vue'
import OS from '@/views/OS.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/commands', name: 'Commands', component: Commands },
  { path: '/plugins', name: 'Plugins', component: Plugins },
  { path: '/terminal', name: 'Terminal', component: Terminal },
  { path: '/settings', name: 'Settings', component: Settings },
  { path: '/os', name: 'OS', component: OS },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
