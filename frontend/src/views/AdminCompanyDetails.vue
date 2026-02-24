<template>
  <div class="container my-5">
    <div v-if="company">
      <h1 class="mb-4">{{ company.company_name }}</h1>
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Company Details</h5>
          <p><strong>Email:</strong> {{ company.email }}</p>
          <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>
          <p><strong>Approval Status:</strong> {{ company.approval_status }}</p>
          <p><strong>Description:</strong> {{ company.description }}</p>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Drives</h5>
          <table class="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Deadline</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in company.drives" :key="drive.id">
                <td>{{ drive.title }}</td>
                <td>{{ drive.status }}</td>
                <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
                <td>
                  <router-link :to="{ name: 'AdminDriveDetails', params: { id: drive.id } }" class="btn btn-sm btn-outline-info">View Drive</router-link>
                </td>
              </tr>
            </tbody>
          </table>
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

const company = ref(null);
const route = useRoute();

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

onMounted(async () => {
  const companyId = route.params.id;
  try {
    const response = await fetch(`/api/admin/company/${companyId}`, { headers: getAuthHeader() });
    const data = await response.json();
    if (response.ok) {
      company.value = data;
    } else {
      throw new Error(data.message || 'Failed to fetch company details');
    }
  } catch (error) {
    console.error('Error fetching company details:', error);
  }
});
</script>
