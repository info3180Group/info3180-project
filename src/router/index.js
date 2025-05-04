import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profiles from '../views/Profiles.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }  // Only for non-authenticated users
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }  // Only for non-authenticated users
    },
    {
      path: '/profiles',
      name: 'profiles',
      component: Profiles,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/:id',
      name: 'profile-detail',
      component: () => import('../views/ProfileDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/edit',
      name: 'edit-profile',
      component: () => import('../views/EditProfile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/edit/:id',
      name: 'edit-profile',
      component: () => import('../views/EditProfile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchProfiles.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/my-profile',
      name: 'my-profile',
      component: () => import('../views/MyProfile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/top-profiles',
      name: 'top-profiles',
      component: () => import('../views/TopProfiles.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/my-profiles',
      name: 'user-profiles',
      component: () => import('../views/UserProfiles.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profiles/new',
      name: 'new-profile',
      component: () => import('../views/NewProfile.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Updated navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  
  // Redirect to home if trying to access guest routes while logged in
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/');
    return;
  }

  // Redirect to login if trying to access protected routes while logged out
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
    return;
  }

  // If accessing root path when not authenticated, redirect to login
  if (to.path === '/' && !isAuthenticated) {
    next('/login');
    return;
  }

  next();
});

export default router
