import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Add from '../views/Headings/Add.vue'
import Heading from '../views/Headings/Heading.vue'

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
    component: Add
  },
  {
    path: '/heading/:head_uuid/',
    name: 'concrete_heading',
    component: Heading
  }
]

const router = new VueRouter({
  routes
})

export default router
