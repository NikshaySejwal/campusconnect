<template>
  <div class="company-dashboard-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-10">

          <!-- Header -->
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-5">
            <div v-if="company">
              <h1 class="fw-bold">Company Dashboard</h1>
              <p class="text-muted">Welcome, {{ company.company_name }}!</p>
            </div>
             <div v-else>
              <h1 class="fw-bold">Company Dashboard</h1>
              <p class="text-muted">Loading...</p>
            </div>
            <router-link to="/create-drive" class="btn btn-primary btn-lg">
                <i class="bi bi-plus-lg me-2"></i>Create Drive
            </router-link>
          </div>

          <!-- Active Drives -->
          <div v-if="drives.length">
            <h4 class="fw-semibold mb-4">Your Drives</h4>
            <div class="vstack gap-3">
              <div v-for="drive in drives" :key="drive.id" class="card shadow-sm">
                <div class="card-body p-4 d-flex justify-content-between align-items-center">
                  <div>
                    <h5 class="fw-bold mb-1">{{ drive.title }}</h5>
                    <span class="badge" :class="drive.status === 'APPROVED' ? 'bg-success-soft text-success' : 'bg-warning-soft text-warning'">{{ drive.status }}</span>
                  </div>
                  <div class="d-flex align-items-center gap-4">
                     <div class="text-center">
                         <div class="fs-4 fw-bold">{{ drive.applications_count }}</div>
                         <div class="text-xs text-muted">Applicants</div>
                     </div>
                    <router-link :to="{ name: 'DriveApplicants', params: { id: drive.id } }" class="btn btn-outline-primary" :class="{ 'disabled': drive.status !== 'APPROVED' }">
                        View Applicants
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
           <div v-else class="text-center py-5 text-muted fst-italic">
                You have not created any drives yet.
           </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const company = ref(null);
const drives = ref([]);

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const fetchData = async (url) => {
    const response = await fetch(url, { headers: getAuthHeader() });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.message || data.msg || `Failed to fetch from ${url}`);
    }
    return data;
};

const fetchCompanyProfile = async () => {
    try {
        const data = await fetchData('/api/company/profile');
        company.value = data;
    } catch (error) {
        console.error('Error fetching company profile:', error);
    }
};

const fetchDrives = async () => {
    try {
        const data = await fetchData('/api/company/drives');
        drives.value = data.drives;
    } catch (error) {
        console.error('Error fetching drives:', error);
    }
};

onMounted(async () => {
    await fetchCompanyProfile();
    await fetchDrives();
});
</script>

<style scoped>
.company-dashboard-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.fw-semibold { font-weight: 600; }
.fw-bold { font-weight: 700; }
.text-muted { color: #64748b !important; }
.text-xs { font-size: 0.8rem; }

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
    font-weight: 600;
}

.badge.bg-warning-soft {
    background-color: #fffbeb !important;
    border: 1px solid #fde68a;
    color: #b45309 !important;
    font-weight: 600;
}

.badge.bg-danger-soft {
    background-color: #fef2f2 !important;
    border: 1px solid #fecaca;
    color: #991b1b !important;
    font-weight: 600;
}
</style>