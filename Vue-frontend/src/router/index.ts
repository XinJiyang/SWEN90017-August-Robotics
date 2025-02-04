import { createRouter, createWebHistory } from 'vue-router';
import { localCache } from '@/utils/cache';
import login from '../views/login/login.vue';
import register from '@/views/register/register.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/:pathMatch(.*)',
      component: () => import('../views/not-found/not-found.vue')
    }
  ]
});

//router gurad
router.beforeEach((to) => {
  if (!localCache.getCache('token')) {

    if (to.path !== '/login' && to.path !== '/register') {
      return '/login';
    }
  } else {
    if (to.path === '/login') {
      return '/';
    }
  }
});

export default router;
