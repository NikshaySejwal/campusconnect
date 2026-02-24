<template>
  <div class="container my-5">
    <div v-if="drive">
      <h1 class="mb-2">Applicants for {{ drive.title }}</h1>
      <p class="text-muted mb-4">Review and manage applications for this drive.</p>

      <div class="card">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="bg-light">
              <tr>
                <th class="px-4 py-3">Student Name</th>
                <th class="px-4 py-3">Application Date</th>
                <th class="px-4 py-3">Status</th>
                <th class="px-4 py-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.id">
                <td class="px-4 py-3">{{ app.student_name }}</td>
                <td class="px-4 py-3">{{ new Date(app.application_date).toLocaleDateString() }}</td>
                <td class="px-4 py-3">
                  <span :class="['badge', getStatusClass(app.status)]">{{ app.status }}</span>
                </td>
                <td class="px-4 py-3 text-end">
                  <div class="d-flex gap-2 justify-content-end">
                    <router-link :to="{ name: 'StudentProfileView', params: { id: app.student_id } }" class="btn btn-sm btn-outline-primary">View Profile</router-link>
                    <button @click="updateStatus(app, 'HIRED')" class="btn btn-sm btn-success">Hired</button>
                    <button @click="updateStatus(app, 'SHORTLISTED')" class="btn btn-sm btn-info">Shortlist</button>
                    <button @click="updateStatus(app, 'REJECTED')" class="btn btn-sm btn-danger">Reject</button>
                  </div>
                </td>
              </tr>
              <tr v-if="!applications.length">
                <td colspan="4" class="text-center text-muted fst-italic py-5">
                  No applications received for this drive yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const drive = ref(null);
const applications = ref([]);

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const fetchDriveDetails = async () => {
  try {
    const response = await fetch(`/api/drive/${route.params.id}`, { headers: getAuthHeader() });
    if (!response.ok) throw new Error('Failed to fetch drive details.');
    drive.value = await response.json();
  } catch (error) {
    console.error('Error fetching drive details:', error);
  }
};

const fetchApplications = async () => {
  try {
    const response = await fetch(`/api/company/drive/${route.params.id}/applications`, { headers: getAuthHeader() });
    if (!response.ok) throw new Error('Failed to fetch applications.');
    const data = await response.json();
    applications.value = data.applications;
  } catch (error) {
    console.error('Error fetching applications:', error);
    if (error.response && error.response.status === 401) {
      router.push({ name: 'Login' });
    }
  }
};

const updateStatus = async (application, status) => {
  try {
    const response = await fetch(`/api/company/application/${application.id}/status`, {
      method: 'POST',
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    if (!response.ok) throw new Error('Failed to update status.');
    await fetchApplications(); // Refresh the list
  } catch (error) {
    console.error('Error updating status:', error);
  }
};

const getStatusClass = (status) => {
  const statusMap = {
    APPLIED: 'bg-primary-soft',
    SHORTLISTED: 'bg-warning-soft text-dark',
    HIRED: 'bg-success-soft',
    REJECTED: 'bg-danger-soft'
  };
  return statusMap[status] || 'bg-light';
};

onMounted(() => {
  fetchDriveDetails();
  fetchApplications();
});
</script>

<style scoped>
.container {
  max-width: 1000px;
}
.table-hover tbody tr:hover {
    background-color: #f8fafc;
}
.badge {
  font-size: .85rem;
  padding: .5em .9em;
  border-radius: .25rem;
  font-weight: 600;
}
.badge.bg-warning-soft { background-color: #fffbeb; border: 1px solid #fde68a; color: #92400e; }
.badge.bg-success-soft { background-color: #e6f9f0; color: #00875a; }
.badge.bg-danger-soft { background-color: #fbeae5; color: #c53030; }
.badge.bg-primary-soft { background-color: #e7e9fd; color: #3f51b5; }
</style>
