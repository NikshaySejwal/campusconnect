<template>
  <div class="container p-4">
    <div v-if="loading" class="text-center">
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-else-if="profile" class="card shadow-sm mx-auto" style="max-width: 50rem;">
      <div class="card-header bg-white p-4 d-flex justify-content-between align-items-start">
        <div>
          <h1 class="h3 fw-bold mb-0">{{ profile.company_name }}</h1>
          <p class="text-muted mb-0">{{ profile.email }}</p>
        </div>
        <span :class="statusBadgeClass(profile.approval_status)" class="badge fs-6">
          {{ profile.approval_status }}
        </span>
      </div>
      <div class="card-body p-4">
        <h2 class="h5 fw-semibold mb-3">Company Details</h2>
        <div class="row">
          <div class="col-md-12">
            <p><strong class="fw-medium">HR Contact:</strong> {{ profile.hr_contact || 'N/A' }}</p>
          </div>
        </div>
        <div class="mt-3">
          <p><strong class="fw-medium">Description:</strong></p>
          <p>{{ profile.description || 'No description provided.' }}</p>
        </div>
        <div class="text-end mt-4">
          <button @click="isEditModalOpen = true" class="btn btn-primary">
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Profile Modal -->
  <div v-if="isEditModalOpen" class="modal fade show" style="display: block;" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Company Profile</h5>
          <button type="button" @click="isEditModalOpen = false" class="btn-close" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateProfile" id="editProfileForm">
            <div class="mb-3">
              <label for="company_name" class="form-label">Company Name</label>
              <input type="text" id="company_name" v-model="editForm.company_name" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="hr_contact" class="form-label">HR Contact</label>
              <input type="text" id="hr_contact" v-model="editForm.hr_contact" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea id="description" v-model="editForm.description" rows="4" class="form-control"></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" @click="isEditModalOpen = false" class="btn btn-secondary">Cancel</button>
          <button type="submit" form="editProfileForm" class="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../utils/axios';

const profile = ref(null);
const loading = ref(true);
const error = ref('');
const isEditModalOpen = ref(false);
const editForm = ref({});

async function fetchCompanyProfile() {
  try {
    const token = localStorage.getItem('access_token');
    const response = await apiClient.get('/company/profile', {
      headers: { Authorization: `Bearer ${token}` }
    });
    profile.value = response.data;
    editForm.value = { ...response.data };
  } catch (err) {
    error.value = 'Could not load company profile.';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function updateProfile() {
  try {
    const token = localStorage.getItem('access_token');
    await apiClient.put('/company/profile', editForm.value, {
      headers: { Authorization: `Bearer ${token}` }
    });
    isEditModalOpen.value = false;
    await fetchCompanyProfile(); // Refresh profile data
  } catch (err) {
    console.error('Failed to update profile:', err);
    // Handle error display to the user
  }
}

function statusBadgeClass(status) {
    const classes = {
      'PENDING': 'bg-warning text-dark',
      'APPROVED': 'bg-success',
      'REJECTED': 'bg-danger'
    };
    return classes[status] || 'bg-secondary';
  }

onMounted(fetchCompanyProfile);
</script>
