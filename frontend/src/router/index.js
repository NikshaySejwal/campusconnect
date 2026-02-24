import { createRouter, createWebHistory } from 'vue-router';
import Landing from '../views/Landing.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AdminCompanyDetails from '../views/AdminCompanyDetails.vue';
import AdminDriveDetails from '../views/AdminDriveDetails.vue';
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
    path: '/admin/company/:id',
    name: 'AdminCompanyDetails',
    component: AdminCompanyDetails,
    meta: { requiresAuth: true, role: 'ADMIN' }
  },
  {
    path: '/admin/drive/:id',
    name: 'AdminDriveDetails',
    component: AdminDriveDetails,
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
    path: '/student/:id/profile',
    name: 'StudentProfileView',
    component: StudentProfile,
    meta: { requiresAuth: true, role: ['COMPANY', 'ADMIN'] }
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
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user'));

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
          return next({ name: 'Landing' });
      }
    }
  }

  if (to.meta.requiresAuth) {
    if (!loggedIn) {
      return next({ name: 'Login' });
    }

    if (to.meta.role) {
      const requiredRoles = Array.isArray(to.meta.role) ? to.meta.role : [to.meta.role];
      if (!requiredRoles.includes(user.role)) {
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
  }

  next();
});

export default router;
