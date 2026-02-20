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
import DriveApplicants from '../views/DriveApplicants.vue';

const routes = [
  { path: '/', name: 'Landing', component: Landing },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { 
    path: '/admin/dashboard', 
    name: 'AdminDashboard', 
    component: AdminDashboard, 
    meta: { requiresAuth: true, role: 'ADMIN' } 
  },
  { 
    path: '/company/dashboard', 
    name: 'CompanyDashboard', 
    component: CompanyDashboard, 
    meta: { requiresAuth: true, role: 'COMPANY' } 
  },
  { 
    path: '/company/drive/create', 
    name: 'CreateDrive', 
    component: CreateDrive, 
    meta: { requiresAuth: true, role: 'COMPANY' } 
  },
  { 
    path: '/company/drive/:id/applicants', 
    name: 'DriveApplicants', 
    component: DriveApplicants, 
    meta: { requiresAuth: true, role: 'COMPANY' } 
  },
  { 
    path: '/student/dashboard', 
    name: 'StudentDashboard', 
    component: StudentDashboard, 
    meta: { requiresAuth: true, role: 'STUDENT' } 
  },
  { 
    path: '/student/applications', 
    name: 'ApplicationHistory', 
    component: ApplicationHistory, 
    meta: { requiresAuth: true, role: 'STUDENT' } 
  },
  {
    path: '/student/profile',
    name: 'StudentProfile',
    component: StudentProfile,
    meta: { requiresAuth: true, role: 'STUDENT' }
  },
  {
    path: '/drive/:id',
    name: 'DriveDetails',
    component: DriveDetails,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user'));

  // If the user is logged in, redirect them away from public pages to their dashboard
  if (loggedIn && ['Landing', 'Login', 'Register'].includes(to.name)) {
    if (user && user.role) {
      switch (user.role) {
        case 'ADMIN':
          return next({ name: 'AdminDashboard' });
        case 'COMPANY':
          return next({ name: 'CompanyDashboard' });
        case 'STUDENT':
          return next({ name: 'StudentDashboard' });
        default:
          // Fallback in case of an unknown role
          return next({ name: 'Landing' });
      }
    }
  }

  // If the route requires authentication
  if (to.meta.requiresAuth) {
    // If the user is not logged in, redirect to the login page
    if (!loggedIn) {
      return next({ name: 'Login' });
    }

    // If the route requires a specific role and the user's role doesn't match,
    // redirect them to their respective dashboard.
    if (to.meta.role && user && to.meta.role !== user.role) {
      switch (user.role) {
        case 'ADMIN':
          return next({ name: 'AdminDashboard' });
        case 'COMPANY':
          return next({ name: 'CompanyDashboard' });
        case 'STUDENT':
          return next({ name: 'StudentDashboard' });
        default:
          return next({ name: 'Landing' });
      }
    }
  }

  // Otherwise, allow the navigation to proceed
  next();
});

export default router;
