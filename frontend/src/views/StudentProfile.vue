<template>
  <main class="container py-4">
    <!-- Page Header -->
    <div class="page-header mb-4">
      <h1 class="fw-bold">My Profile</h1>
      <p class="text-muted">View and manage your personal details, academic information, and skills.</p>
    </div>

    <!-- Loading State -->
    <div v-if="!student" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading Profile...</p>
    </div>

    <!-- Profile Content -->
    <div v-else class="card">
      <div class="card-body p-4">
        <!-- Profile Header -->
        <div class="row align-items-center mb-4">
          <div class="col-md-auto text-center text-md-start mb-3 mb-md-0">
            <div class="avatar-wrapper position-relative d-inline-block">
              <img :src="fullAvatarUrl" alt="Profile Picture" class="avatar rounded-circle border p-1">
              <div v-if="isStudentView && isEditing" class="avatar-overlay position-absolute top-0 start-0 w-100 h-100 rounded-circle d-flex align-items-center justify-content-center" @click="triggerFileInput">
                <i class="bi bi-camera fs-4"></i>
              </div>
              <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" accept="image/*">
            </div>
          </div>

          <div class="col-md">
            <h2 class="fw-bold">{{ student.name }}</h2>
            <p class="text-muted mb-2">{{ student.email }}</p>
            <p v-if="!isEditing" class="text-muted">{{ student.bio || 'No bio provided.' }}</p>
          </div>

          <div class="col-md-auto d-flex flex-column align-items-stretch gap-2 mt-3 mt-md-0">
            <button v-if="!isEditing && isStudentView" @click="startEditing" class="btn btn-primary">Edit Profile</button>
            <button v-if="isEditing" @click="saveProfile" class="btn btn-success">Save Changes</button>
            <button v-if="isEditing" @click="cancelEdit" class="btn btn-secondary">Cancel</button>
          </div>
        </div>

        <!-- Bio Editor -->
        <div v-if="isEditing" class="mb-4">
          <label for="bio" class="form-label fw-semibold">Profile Bio</label>
          <textarea v-model="editableStudent.bio" id="bio" class="form-control" rows="3"></textarea>
        </div>

        <!-- Details Grid -->
        <div class="row">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <h5 class="fw-semibold mb-3">Academics</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Branch</span>
                <input v-if="isEditing" type="text" class="form-control form-control-sm w-50" v-model="editableStudent.branch">
                <strong v-else>{{ student.branch }}</strong>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>CGPA</span>
                <input v-if="isEditing" type="number" step="0.1" class="form-control form-control-sm w-50" v-model="editableStudent.cgpa">
                <strong v-else>{{ student.cgpa }}</strong>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Graduation Year</span>
                <input v-if="isEditing" type="text" class="form-control form-control-sm w-50" v-model="editableStudent.graduation_year">
                <strong v-else>{{ student.graduation_year }}</strong>
              </li>
            </ul>
          </div>

          <div class="col-lg-6">
            <h5 class="fw-semibold mb-3">Skills</h5>
            <div v-if="isEditing" class="mb-3">
              <input type="text" class="form-control" v-model="editableStudent.skills" placeholder="Comma-separated skills">
            </div>
            <div v-if="student.skills" class="d-flex flex-wrap gap-2">
              <span v-for="skill in student.skills.split(',').filter(s => s.trim())" :key="skill" class="badge bg-secondary-soft text-secondary">
                {{ skill.trim() }}
              </span>
            </div>
            <p v-else-if="!isEditing" class="text-muted fst-italic">No skills listed.</p>
          </div>
        </div>

        <!-- Export Section -->
        <div class="mt-4 border-top pt-4">
             <h5 class="fw-semibold mb-3">Data Export</h5>
             <p class="text-muted">Export your application history as a CSV file.</p>
            <button @click="initiateExport" :disabled="exporting" class="btn btn-outline-primary">
                {{ exporting ? 'Exporting...' : 'Export Application History' }}
            </button>
             <a :href="exportUrl" v-if="exportUrl" download="application_history.csv" class="btn btn-link text-success fw-semibold ms-2">Download Available</a>
        </div>

      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isEditing = ref(false);
const student = ref(null);
const editableStudent = ref(null);
const fileInput = ref(null);
const exporting = ref(false);
const exportUrl = ref(null);

const isStudentView = computed(() => !route.params.id);

const fullAvatarUrl = computed(() => {
  if (student.value?.avatar_url) {
    return `${student.value.avatar_url}?t=${new Date().getTime()}`;
  }
  return `https://i.pravatar.cc/150?u=${student.value?.id}`;
});

const getAuthHeader = (isMultipart = false) => {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` };
    if (!isMultipart) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
};

const fetchStudentProfile = async () => {
  const profileId = route.params.id;
  const url = profileId ? `/api/student/${profileId}/profile` : '/api/student/profile';

  try {
    const response = await fetch(url, { headers: getAuthHeader() });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || data.msg || `Failed to fetch profile: ${response.statusText}`);
    }
    student.value = data;
    editableStudent.value = { ...data };
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

onMounted(fetchStudentProfile);

const startEditing = () => {
  editableStudent.value = { ...student.value };
  isEditing.value = true;
};

const saveProfile = async () => {
  try {
    const response = await fetch('/api/student/profile', {
      method: 'PUT',
      headers: getAuthHeader(),
      body: JSON.stringify(editableStudent.value),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || data.msg || 'Failed to save profile');
    }
    student.value = { ...editableStudent.value };
    isEditing.value = false;
  } catch (error) {
    console.error('Error saving profile:', error);
  }
};

const cancelEdit = () => {
    isEditing.value = false;
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/student/avatar', {
            method: 'POST',
            headers: getAuthHeader(true),
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || data.msg || 'Failed to upload avatar');
        }
        student.value.avatar_url = data.avatar_url;
    } catch (error) {
        console.error('Error uploading avatar:', error);
    }
};

const initiateExport = async () => {
    exporting.value = true;
    exportUrl.value = null;
    try {
        const response = await fetch('/api/student/export', {
            method: 'POST',
            headers: getAuthHeader(),
        });
        if (!response.ok) throw new Error('Failed to initiate export');
        setTimeout(() => {
            exportUrl.value = '/api/student/export';
            exporting.value = false;
        }, 3000);
    } catch (error) {
        console.error('Error initiating export:', error);
        exporting.value = false;
    }
};

</script>

<style scoped>
.page-header {
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.avatar-wrapper .avatar {
    width: 120px;
    height: 120px;
}

.avatar-wrapper .avatar-overlay {
    background-color: rgba(0,0,0,0.5);
    color: white;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.avatar-wrapper:hover .avatar-overlay {
    opacity: 1;
}

.badge.bg-secondary-soft {
    background-color: #f8f9fa !important;
    border: 1px solid #dee2e6;
    color: #6c757d !important;
    font-weight: 600;
}
</style>
