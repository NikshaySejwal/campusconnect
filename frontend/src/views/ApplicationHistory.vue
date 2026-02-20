<template>
  <div class="application-history-page">
    <!-- Navbar can be added here if needed -->
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-9">

          <!-- Header -->
          <div class="text-center mb-5">
            <h1 class="fw-bold">Application History</h1>
            <p class="text-muted">Track the status and history of all your placement applications.</p>
          </div>

          <!-- Application List -->
          <div class="vstack gap-3">
            <div v-for="application in applications" :key="application.id" class="card shadow-sm">
              <div class="card-body p-4">
                <div class="d-flex flex-column flex-md-row justify-content-between">
                  <!-- Job Details -->
                  <div class="mb-3 mb-md-0">
                    <h5 class="fw-bold mb-1">{{ application.drive.title }}</h5>
                    <p class="text-muted fw-semibold mb-2">{{ application.drive.company.name }}</p>
                    <p class="text-xs text-muted mb-0">Applied on {{ new Date(application.applied_on).toLocaleDateString() }}</p>
                  </div>
                  <!-- Status -->
                  <div class="d-flex align-items-center justify-content-end">
                    <span :class="['badge', getStatusClass(application.status)]">{{ application.status }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="!applications.length && !isLoading" class="text-center py-5 text-muted fst-italic">
                You have not applied to any drives yet.
            </div>

            <div v-if="isLoading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const applications = ref([]);
const isLoading = ref(true);

const getAuthHeader = () => ({
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
});

const fetchApplications = async () => {
  isLoading.value = true;
  try {
    const response = await fetch('/api/student/applications', { headers: getAuthHeader() });
    if (!response.ok) throw new Error('Failed to fetch applications');
    const data = await response.json();
    applications.value = data.applications;
  } catch (error) {
    console.error('Error fetching applications:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchApplications);

const getStatusClass = (status) => {
  const map = {
    PENDING: 'bg-warning-soft text-warning',
    SHORTLISTED: 'bg-success-soft text-success',
    REJECTED: 'bg-danger-soft text-danger',
  };
  return map[status];
};
</script>

<style scoped>
.application-history-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.fw-bold { font-weight: 700; }
.fw-semibold { font-weight: 600; }
.text-muted { color: #64748b !important; }
.text-xs { font-size: 0.8rem; }

.badge {
  font-size: .8rem;
  padding: .5em .8em;
  font-weight: 600;
  letter-spacing: .5px;
  text-transform: capitalize;
}

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
}

.badge.bg-danger-soft {
    background-color: #fef2f2 !important;
    border: 1px solid #fecaca;
    color: #991b1b !important;
}

.badge.bg-warning-soft {
    background-color: #fffbeb !important;
    border: 1px solid #fde68a;
    color: #854d0e !important;
}
</style>
