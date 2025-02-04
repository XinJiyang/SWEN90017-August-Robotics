import type { RouteRecordRaw } from 'vue-router';

const asyncRoutes: RouteRecordRaw[] = [
  {
    path: '/dashboard',
    name: 'dashborad',
    component: () => import('../views/dashboard/dashboard.vue'),
    meta: {
      icon: 'Histogram',
      roles: ['viewer', 'operator', 'admin']
    }
  },
  {
    path: '/job',
    name: 'job',
    children: [
      {
        path: '',
        component: () => import('../views/job/job.vue'),
        meta: {
          roles: ['viewer', 'operator', 'admin']
        }
      },
      {
        path: 'edit/:id',
        component: () => import('../views/jobdetails/jobdetails.vue'),
        meta: {
          roles: ['operator', 'admin']
        }
      },
      {
        path: 'view/:id',
        component: () => import('../views/jobdetails/jobLayout.vue'),
        meta: {
          roles: ['viewer', 'operator', 'admin']
        }
      },
      {
        path: 'summary/:id',
        component: () => import('../views/jobdetails/jobSummary.vue'),
        meta: {
          roles: ['viewer', 'operator', 'admin']
        }
      }
    ],
    meta: {
      icon: 'Coin'
    }
  },
  {
    path: '/client',
    name: 'client',
    children: [
      {
        path: 'create',
        name: 'create',
        component: () => import('../views/client/create.vue'),
        meta: {
          roles: ['operator', 'admin']
        }
      },
      {
        path: '',
        component: () => import('../views/client/client.vue'),
        meta: {
          roles: ['viewer', 'operator', 'admin']
        }
      },
      {
        path: 'edit/:id',
        name: 'edit',
        component: () => import('../views/client/edit.vue'),
        meta: {
          roles: ['operator', 'admin']
        },
        props: true
      },
      {
        path: 'detail/:id',
        name: 'detail',
        component: () => import('../views/client/detail.vue'),
        meta: {
          roles: ['viewer', 'operator', 'admin']
        },
        props: true
      }
    ],
    meta: {
      icon: 'Avatar'
    }
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('../views/user/user.vue'),
    meta: {
      icon: 'User',
      roles: ['admin']
    }
  }
];

export default asyncRoutes;
