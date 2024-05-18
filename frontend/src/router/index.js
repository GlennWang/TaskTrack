// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import TaskTrack from '../views/TaskTrack.vue'

const routes = [
  {
    path: '/',
    name: 'TaskTrack',
    component: TaskTrack
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
