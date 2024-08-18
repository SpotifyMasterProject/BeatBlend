import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingView from '@/views/LandingView.vue'
import {useAuthStore} from '@/stores/auth'
import WebsocketView from '@/views/WebsocketView.vue'
import AuthorizeSpotifyView from '@/views/AuthorizeSpotifyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
      beforeEnter: () => {
        // Redirect authenticated users to sessions page.
        const authStore = useAuthStore();
        if (authStore.token) {
          return {name: 'home'};
        }
      }
    },
    {
      path: '/spotify-callback',
      name: 'spotify-callback',
      component: AuthorizeSpotifyView
    },
    {
      path: '/sessions/join/:inviteToken',
      name: 'landing-view-guest',
      component: LandingView
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      /* meta: { requiresAuth: true } */
    },
    {
      path: '/session/:sessionId',
      name: 'guest-view',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/websockets',
      name: 'websockets',
      component: WebsocketView
    },
  ]
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return {name: 'landing'}
  }
})

export default router
