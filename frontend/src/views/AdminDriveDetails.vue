<template>
  <div class="container my-5">
    <div v-if="drive">
      <h1 class="mb-4">{{ drive.title }}</h1>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Drive Details</h5>
          <p><strong>Company:</strong> {{ drive.company }}</p>
          <p><strong>Description:</strong> {{ drive.description }}</p>
          <p><strong>Salary:</strong> {{ drive.salary }}</p>
          <p><strong>Location:</strong> {{ drive.location }}</p>
          <p><strong>Eligible Branch:</strong> {{ drive.branch }}</p>
          <p><strong>Minimum CGPA:</strong> {{ drive.cgpa }}</p>
          <p><strong>Application Deadline:</strong> {{ new Date(drive.deadline).toLocaleDateString() }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const drive = ref(null);
const route = useRoute();

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

onMounted(async () => {
  const driveId = route.params.id;
  try {
    const response = await fetch(`/api/admin/drive/${driveId}`, { headers: getAuthHeader() });
    const data = await response.json();
    if (response.ok) {
      drive.value = data;
    } else {
      throw new Error(data.message || 'Failed to fetch drive details');
    }
  } catch (error) {
    console.error('Error fetching drive details:', error);
  }
});
</script>
