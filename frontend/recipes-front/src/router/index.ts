import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import VerifyView from '../views/VerifyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/log-in',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/verify-code',
      name: 'verify',
      component: VerifyView,
    }
  ],
})

export default router
