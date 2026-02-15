import { createRouter, createWebHistory } from 'vue-router';
import Landing from '../views/Landing.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import BatchJobs from '../views/BatchJobs.vue';
import CompanyDashboard from '../views/CompanyDashboard.vue';
import CreateDrive from '../views/CreateDrive.vue';
import ScreeningRoom from '../views/ScreeningRoom.vue';
import ApplicationHistory from '../views/ApplicationHistory.vue';
import StudentProfile from '../views/StudentProfile.vue';
import StudentDashboard from '../views/StudentDashboard.vue';

const routes = [
  { path: '/', component: Landing },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminDashboard },
  { path: '/batch-jobs', component: BatchJobs },
  { path: '/company', component: CompanyDashboard },
  { path: '/create-drive', component: CreateDrive },
  { path: '/screening', component: ScreeningRoom },
  { path: '/applications', component: ApplicationHistory },
  { path: '/profile/:id', component: StudentProfile, props: true },
  { path: '/student', component: StudentDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
