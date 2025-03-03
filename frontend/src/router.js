// router.js

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import CasesView from './views/CasesView.vue';
import JudicialInterfaceView from './views/JudicialInterfaceView.vue';
import PoliticalInterfaceView from './views/PoliticalInterfaceView.vue';
import StatisticsDashboardView from './views/StatisticsDashboardView.vue';
import ViewNormsView from './views/NormsView.vue';
import AboutView from './views/AboutView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/cases', component: CasesView },
  { path: '/judicial', component: JudicialInterfaceView },
  { path: '/political', component: PoliticalInterfaceView },
  { path: '/statistics', component: StatisticsDashboardView },
  { path: '/norms', component: ViewNormsView },
  { path: '/about', component: AboutView },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
