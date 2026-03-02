<template>
  <main class="container py-4">
    <div class="page-header mb-4">
      <h1 class="fw-bold">Application History</h1>
      <p class="text-muted">Track the status and history of all your placement applications.</p>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="applications.length > 0" class="vstack gap-3">
      <div v-for="application in applications" :key="application.id" class="card list-item-card">
        <div class="card-body p-4">
          <div class="d-flex flex-column flex-md-row justify-content-between">
            <div class="mb-3 mb-md-0">
              <h5 class="card-title fw-bold mb-1">{{ application.drive_title }}</h5>
              <p class="card-subtitle text-muted fw-semibold mb-2">{{ application.company_name }}</p>
              <p class="text-xs text-muted mb-0">Applied on {{ new Date(application.application_date).toLocaleDateString() }}</p>
            </div>
            <div class="d-flex align-items-center justify-content-end">
              <span :class="['badge', getStatusClass(application.status)]">{{ application.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5 text-muted fst-italic border rounded-3">
      You have not applied to any drives yet.
    </div>
  </main>
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
    APPLIED: 'bg-warning-soft text-warning',
    SHORTLISTED: 'bg-success-soft text-success',
    HIRED: 'bg-primary-soft text-primary',
    REJECTED: 'bg-danger-soft text-danger',
  };
  return map[status] || 'bg-secondary-soft';
};
</script>

<style scoped>
.page-header {
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.list-item-card {
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}

.fw-bold { font-weight: 700 !important; }
.fw-semibold { font-weight: 600; }
.text-muted { color: #64748b !important; }
.text-xs { font-size: 0.8rem; }

.badge {
  font-size: .8rem;
  padding: .5em .8em;
  font-weight: 600;
  letter-spacing: .5px;
  text-transform: capitalize;
  border-radius: .375rem;
}
</style>
