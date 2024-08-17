import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Products from '../components/Products.vue';
import ClientsRegister from '../components/client/ClientsRegister.vue';
import ClientsList from '../components/client/ClientsList.vue';
import ClientsEdit from '../components/client/ClientsEdit.vue';
import CreateSale from '../components/sale/CreateSale.vue';
import SalesList from '../components/sale/SalesList.vue';
import Reports from '../components/Reports.vue';
import Home from '../components/Home.vue';

const routes = [
  { path: '/', component: Home, meta: { hideHeader: true } },
  { path: '/login', component: Login, meta: { hideHeader: true } },
  { path: '/products', component: Products }, 
  { path: '/clients', component: ClientsList }, 
  { path: '/clients/register', component: ClientsRegister }, 
  { path: '/clients/:id/edit', component: ClientsEdit }, 
  { path: '/sale/create', component: CreateSale }, 
  { path: '/sales/list', component: SalesList}, 
  { path: '/reports', component: Reports}, 
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); 
  if (to.path !== '/login' && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;