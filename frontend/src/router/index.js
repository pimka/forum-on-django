import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Add from '../views/Headings/Add.vue'
import Heading from '../views/Headings/Heading.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Tags from '../views/Tags.vue'
import store from '@/store'
import SearchHeadings from '../views/Headings/SearchHeadings.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/new-heading/',
    name: 'new-heading',
    component: Add,
    meta: {
      Authorization: true
    }
  },
  {
    path: '/heading/:head_uuid/',
    name: 'concrete_heading',
    component: Heading
  },
  {
    path: '/login/',
    name: 'login',
    component: Login
  },
  {
    path: '/register/',
    name: 'register',
    component: Register
  },
  {
    path: '/tags/',
    name: 'tags',
    component: Tags,
    meta: {
      Administer: true
    }
  },
  {
    path: '/search/',
    name: 'search',
    component: SearchHeadings
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.Authorization)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login/')
  } else {
    next()
  }

  if (to.matched.some(record => record.meta.Authorization)) {
    if (store.getters.isStaff) {
      next()
      return
    }
    next('/')
  } else {
    next()
  }
})

export default router
