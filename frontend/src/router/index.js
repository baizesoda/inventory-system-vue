import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/login', component: () => import('../views/Login.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'products', component: () => import('../views/Products.vue') },
      { path: 'inventory', component: () => import('../views/Inventory.vue') },
      { path: 'scan', component: () => import('../views/Scan.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useUserStore()
  if (!to.meta.guest && !store.token) {
    next('/login')
  } else {
    next()
  }
})

export default router
