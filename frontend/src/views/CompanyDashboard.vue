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
              <p class="text-muted">Loading company profile...</p>
            </div>
            <router-link v-if="isApproved" to="/company/drive/create" class="btn btn-primary btn-lg">
              <i class="bi bi-plus-lg me-2"></i>Create Drive
            </router-link>
          </div>

          <!-- Approval Status -->
          <div v-if="!isApproved" class="alert alert-warning" role="alert">
            <h4 class="alert-heading">Pending Approval</h4>
            <p>Your company profile is currently under review by the placement cell. You will be able to create drives and view applicants once your profile has been approved.</p>
          </div>

          <!-- Active Drives -->
          <div v-if="isApproved">
            <h4 class="fw-semibold mb-4">Your Drives</h4>
            <div v-if="drives.length" class="vstack gap-3">
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
            <div v-else class="text-center py-5 text-muted fst-italic">
                 You have not created any drives yet.
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const company = ref(null);
const drives = ref([]);
const approvalStatus = ref('PENDING'); // Assume pending until proven otherwise

const isApproved = computed(() => approvalStatus.value === 'APPROVED');

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const fetchData = async (url) => {
    const headers = getAuthHeader();
    headers['Cache-Control'] = 'no-cache'; // Prevent browser caching
    const response = await fetch(url, { headers });
    const data = await response.json();
    if (!response.ok) {
        // Capture status for non-approved companies
        if (response.status === 403) {
            approvalStatus.value = 'PENDING';
        }
        throw new Error(data.message || data.msg || `Failed to fetch from ${url}`);
    }
    return data;
};

const fetchCompanyProfile = async () => {
    try {
        const data = await fetchData('/api/company/profile');
        company.value = data;
        approvalStatus.value = data.approval_status; // Set status from successful fetch
    } catch (error) {
        console.error('Error fetching company profile:', error);
        // If fetching fails, isApproved will remain false
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
    if (isApproved.value) {
        await fetchDrives();
    }
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

.alert-warning {
    background-color: #fffbeb;
    border-color: #fde68a;
    color: #b45309;
}
</style>
