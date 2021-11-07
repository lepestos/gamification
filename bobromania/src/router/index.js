import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/BlackBox',
    name: 'BlackBox',
    component: () => import('../views/BlackBox.vue')
  },
  {
    path: '/Lottery',
    name: 'Lottery',
    component: () => import('../views/Lottery.vue')
  },
  {
    path: '/Bingo',
    name: 'Bingo',
    component: () => import('../views/Bingo.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
