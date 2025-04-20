import './assets/main.css'

import { createApp, reactive } from 'vue'
import App from './App.vue'
import router from './router'
import { StateKey, type State } from './types/auth'

const app = createApp(App)

const state: State = reactive({
    userToken: null,
    user:null,
})

app.use(router)
app.provide(StateKey, state)

app.mount('#app')
