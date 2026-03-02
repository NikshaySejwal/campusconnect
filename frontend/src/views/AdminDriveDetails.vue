<template>
  <main class="container py-4">
    <div v-if="drive">
      <div class="page-header mb-4">
        <h1 class="fw-bold">{{ drive.title }}</h1>
        <p class="text-muted">Reviewing drive from {{ drive.company }}.</p>
      </div>

      <div class="card">
        <div class="card-header">
          Drive Details
        </div>
        <div class="card-body">
          <p><strong>Description:</strong> {{ drive.description }}</p>
          <p><strong>Salary:</strong> {{ drive.salary }}</p>
          <p><strong>Location:</strong> {{ drive.location }}</p>
          <p><strong>Eligible Branch:</strong> {{ drive.branch }}</p>
          <p><strong>Minimum CGPA:</strong> {{ drive.cgpa }}</p>
          <p><strong>Application Deadline:</strong> {{ new Date(drive.deadline).toLocaleDateString() }}</p>
           <p><strong>Status:</strong> <span :class="['badge', getStatusClass(drive.status)]">{{ drive.status }}</span></p>
        </div>
      </div>

    </div>
    <div v-else class="text-center">
      <p>Loading drive details...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const drive = ref(null);
const route = useRoute();

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const getStatusClass = (status) => {
    switch (status) {
        case 'APPROVED': return 'bg-success-soft text-success';
        case 'REJECTED': return 'bg-danger-soft text-danger';
        case 'PENDING': return 'bg-warning-soft text-warning';
        default: return 'bg-light text-muted';
    }
};

onMounted(async () => {
  const driveId = route.params.id;
  try {
    const response = await fetch(`/api/admin/drive/${driveId}`, { headers: getAuthHeader() });
    if (response.ok) {
      const data = await response.json();
      drive.value = data;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch drive details');
    }
  } catch (error) {
    console.error('Error fetching drive details:', error);
  }
});
</script>

<style scoped>
/* Scoped styles from AdminDashboard to ensure consistency for status badges */
.badge.bg-success-soft {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
}

.badge.bg-danger-soft {
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
}

.badge.bg-warning-soft {
    background-color: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
}

.page-header {
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}
</style>
