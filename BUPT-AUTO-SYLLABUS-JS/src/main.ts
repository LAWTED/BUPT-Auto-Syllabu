import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import Notifications from '@kyvg/vue3-notification'

createApp(App).use(Notifications).mount('#app')
