import { createRouter, createWebHistory } from 'vue-router';
import Landing from '../views/Landing.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import CompanyDashboard from '../views/CompanyDashboard.vue';
import CreateDrive from '../views/CreateDrive.vue';
import ApplicationHistory from '../views/ApplicationHistory.vue';
import StudentProfile from '../views/StudentProfile.vue';
import StudentDashboard from '../views/StudentDashboard.vue';
import DriveDetails from '../views/DriveDetails.vue';

const routes = [
  { path: '/', name: 'Landing', component: Landing },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { 
    path: '/admin/dashboard', 
    name: 'AdminDashboard', 
    component: AdminDashboard, 
    meta: { requiresAuth: true, role: 'Admin' } 
  },
  { 
    path: '/company/dashboard', 
    name: 'CompanyDashboard', 
    component: CompanyDashboard, 
    meta: { requiresAuth: true, role: 'Company' } 
  },
  { 
    path: '/company/drive/create', 
    name: 'CreateDrive', 
    component: CreateDrive, 
    meta: { requiresAuth: true, role: 'Company' } 
  },
  { 
    path: '/student/dashboard', 
    name: 'StudentDashboard', 
    component: StudentDashboard, 
    meta: { requiresAuth: true, role: 'Student' } 
  },
  { 
    path: '/student/applications', 
    name: 'ApplicationHistory', 
    component: ApplicationHistory, 
    meta: { requiresAuth: true, role: 'Student' } 
  },
  { 
    path: '/student/profile', 
    name: 'StudentProfile', 
    component: StudentProfile, 
    meta: { requiresAuth: true, role: 'Student' } 
  },
  { 
    path: '/drive/:id', 
    name: 'DriveDetails', 
    component: DriveDetails, 
    props: true, 
    meta: { requiresAuth: true } 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user'));

  if (to.meta.requiresAuth) {
    if (!loggedIn) {
      return next({ name: 'Login' });
    }
    if (to.meta.role && to.meta.role !== user.role) {
      // Redirect based on role if there's a mismatch
      switch (user.role) {
        case 'Admin':
          return next({ name: 'AdminDashboard' });
        case 'Company':
          return next({ name: 'CompanyDashboard' });
        case 'Student':
          return next({ name: 'StudentDashboard' });
        default:
          return next({ name: 'Landing' });
      }
    }
  }

  next();
});

export default router;
