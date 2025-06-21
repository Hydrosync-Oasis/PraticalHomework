// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analysis from '../views/Analysis.vue'
import Diabetes from '../views/Diabetes.vue'

const routes = [
  { path: '/', redirect: '/dashboard/age' },
  { 
    path: '/dashboard', 
    component: Dashboard,
    children: [
      { path: '', redirect: '/dashboard/age' },
      { path: 'age', name: 'AgeAnalysis' },
      { path: 'gender', name: 'GenderAnalysis' },
      { path: 'correlation', name: 'CorrelationAnalysis' },
      { path: 'smoking', name: 'SmokingAnalysis' },
    ]
  },
  { path: '/analysis', component: Analysis },
  { path: '/diabetes', component: Diabetes }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
