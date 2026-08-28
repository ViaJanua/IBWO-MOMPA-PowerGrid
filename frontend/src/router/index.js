import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import TechStackView from '@/views/TechStackView.vue';
import DataView from '@/views/DataView.vue';
import AlgorithmView from '@/views/AlgorithmView.vue';
import LoginView from '@/views/LoginView.vue';
import ThreeView from '@/views/ThreeView.vue'; 

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/tech-stack', name: 'techStack', component: TechStackView },
  { path: '/data', name: 'data', component: DataView },
  { path: '/algorithm', name: 'algorithm', component: AlgorithmView },
  { path: '/login', name: 'login', component: LoginView },
   { path: '/three', name: 'three', component: ThreeView },
  { path: '/:pathMatch(.*)*', redirect: '/'},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;