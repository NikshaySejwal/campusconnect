<template>
  <div class="student-dashboard-page">
    <div class="container py-5">
      
      <!-- Header -->
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-5">
            <div>
              <h1 class="fw-bold">Welcome, John!</h1>
              <p class="text-muted">Explore and apply to the latest placement drives from top companies.</p>
            </div>
            <div class="d-flex gap-2 mt-3 mt-md-0">
              <router-link to="/profile/1" class="btn btn-outline-primary">
                  <i class="bi bi-person-circle me-2"></i>My Profile
              </router-link>
              <router-link to="/applications" class="btn btn-outline-primary">
                  <i class="bi bi-file-earmark-text me-2"></i>My Applications
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Drives -->
      <div class="row justify-content-center">
        <div class="col-lg-10">
            <h4 class="fw-semibold mb-4">Available Drives</h4>
            <div class="vstack gap-3">
                <div v-for="drive in availableDrives" :key="drive.id" class="card shadow-sm drive-card">
                    <div class="card-body p-4">
                        <div class="d-flex align-items-center">
                            <img :src="drive.companyLogo" :alt="drive.company" class="company-logo me-4">
                            <div class="flex-grow-1">
                                <h5 class="fw-bold mb-1">{{ drive.jobTitle }}</h5>
                                <p class="text-muted fw-semibold mb-2">{{ drive.company }}</p>
                                <div class="d-flex flex-wrap gap-3 text-muted text-sm">
                                    <span><i class="bi bi-cash-stack me-1"></i> {{ drive.salary }}</span>
                                    <span><i class="bi bi-calendar-event me-1"></i> Deadline: {{ drive.deadline }}</span>
                                </div>
                            </div>
                            <button class="btn btn-primary ms-4">Apply Now</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const availableDrives = ref([
  {
    id: 1,
    jobTitle: 'Software Development Engineer',
    company: 'Amazon',
    companyLogo: 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
    salary: '15-20 LPA',
    deadline: '2024-08-15',
  },
  {
    id: 2,
    jobTitle: 'Frontend Engineer',
    company: 'Google',
    companyLogo: 'https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg',
    salary: '18-22 LPA',
    deadline: '2024-08-20',
  },
  {
    id: 3,
    jobTitle: 'Data Scientist',
    company: 'Microsoft',
    companyLogo: 'https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg',
    salary: '16-25 LPA',
    deadline: '2024-08-25',
  },
]);
</script>

<style scoped>
.student-dashboard-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.fw-bold { font-weight: 700; }
.fw-semibold { font-weight: 600; }
.text-muted { color: #64748b !important; }
.text-sm { font-size: 0.9rem; }

.drive-card {
    border: none;
    transition: all 0.2s ease-in-out;
}

.drive-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1) !important;
}

.company-logo {
    width: 50px;
    height: 50px;
    object-fit: contain;
}
</style>
