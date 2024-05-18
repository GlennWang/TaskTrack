// src/main.js
import { createApp } from 'vue'
import router from './router'
import './assets/defaultstyle.css'
import './assets/scrollbar.css'
import './assets/checkbox.css'
import App from './App.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')
