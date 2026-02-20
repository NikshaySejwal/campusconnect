<template>
  <div class="page-wrapper">
    <main class="container py-5">
      <div v-if="drive">
        <h1 class="page-title">Applicants for {{ drive.job_title }}</h1>
        <p class="page-subtitle">Review and manage applications for this drive.</p>
      </div>
      <div v-else class="text-center">
        <p>Loading drive details...</p>
      </div>

      <div v-if="applications.length" class="table-responsive mt-5">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th scope="col">Student Name</th>
              <th scope="col">Application Date</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>{{ app.student_name }}</td>
              <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
              <td>
                <span class="badge" :class="statusBadge(app.status)">{{ app.status }}</span>
              </td>
              <td>
                <div class="btn-group">
                  <button @click="updateStatus(app.id, 'SHORTLISTED')" class="btn btn-sm btn-outline-success" :disabled="app.status === 'SHORTLISTED'">Shortlist</button>
                  <button @click="updateStatus(app.id, 'REJECTED')" class="btn btn-sm btn-outline-danger" :disabled="app.status === 'REJECTED'">Reject</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
       <div v-else-if="!isLoading" class="text-center py-5 border-top mt-4">
        <p class="text-muted fst-italic">No applications have been submitted for this drive yet.</p>
      </div>

       <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger mt-4">{{ error }}</div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const drive = ref(null);
const applications = ref([]);
const isLoading = ref(true);
const error = ref(null);

const driveId = route.params.id;

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const statusBadge = (status) => ({
  'bg-success-soft text-success': status === 'SHORTLISTED',
  'bg-danger-soft text-danger': status === 'REJECTED',
  'bg-primary-soft text-primary': status === 'APPLIED',
});

const fetchDriveDetails = async () => {
  try {
    const res = await fetch(`/api/company/drive/${driveId}/applications`, { headers: getAuthHeader() });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to fetch drive details.');
    drive.value = { job_title: data.drive_title }; // Simplified for now
    applications.value = data.applications;
  } catch (err) {
    error.value = err.message;
  }
};

const updateStatus = async (applicationId, status) => {
  try {
    const res = await fetch(`/api/company/application/${applicationId}/status`, {
      method: 'POST',
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to update status.');
    
    // Update local state
    const index = applications.value.findIndex(app => app.id === applicationId);
    if(index !== -1) {
        applications.value[index].status = status;
    }

  } catch (err) {
    error.value = `Failed to update status: ${err.message}`;
  }
};

onMounted(async () => {
  isLoading.value = true;
  await fetchDriveDetails();
  isLoading.value = false;
});
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.page-title { font-size: 2.2rem; font-weight: 700; }
.page-subtitle { font-size: 1.1rem; color: #6c757d; }

.badge.bg-success-soft { background-color: #e6f9f0; color: #00875a; }
.badge.bg-danger-soft { background-color: #fbeae5; color: #c53030; }
.badge.bg-primary-soft { background-color: #e7e9fd; color: #3f51b5; }
</style>
