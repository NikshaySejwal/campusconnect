<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <router-link v-if="isStudentView" :to="{ name: 'StudentDashboard' }">Dashboard</router-link>
          <router-link v-if="isStudentView" :to="{ name: 'ApplicationHistory' }">My Applications</router-link>
          <router-link v-if="isStudentView" :to="{ name: 'StudentProfile' }">My Profile</router-link>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <div v-if="student" class="profile-card">
        <div class="profile-header">
          <div class="avatar-wrapper">
            <img :src="fullAvatarUrl" alt="Profile Picture" class="avatar">
            <div v-if="isStudentView" class="avatar-overlay" @click="triggerFileInput">
              <i class="bi bi-camera"></i>
              <span>Change Picture</span>
            </div>
            <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" accept="image/*">
          </div>
          <div class="header-info">
            <h2 class="student-name">{{ student.name }}</h2>
            <p class="student-email">{{ student.email }}</p>
            <p v-if="!isEditing" class="student-bio">{{ student.bio || 'No bio provided.' }}</p>
          </div>
          <div class="header-actions">
            <button v-if="!isEditing && isStudentView" @click="startEditing" class="btn-edit">Edit Profile</button>
            <button v-if="isEditing" @click="saveProfile" class="btn-save">Save</button>
            <button v-if="isEditing" @click="cancelEdit" class="btn-cancel">Cancel</button>
            <button v-if="isStudentView" @click="initiateExport" :disabled="exporting" class="btn-export">{{ exporting ? 'Exporting...' : 'Export CSV' }}</button>
            <a :href="exportUrl" v-if="exportUrl" download="application_history.csv" class="btn-download">Download Export</a>
          </div>
        </div>

        <div class="profile-body">
          <div v-if="isEditing" class="bio-editor">
            <label for="bio">Profile Bio</label>
            <textarea v-model="editableStudent.bio" id="bio" class="form-control" rows="3"></textarea>
          </div>

          <div class="details-grid">
            <div class="detail-section">
              <h5 class="section-title">Academics</h5>
              <ul class="info-list">
                <li>
                  <span>Branch</span>
                  <input v-if="isEditing" type="text" class="form-control-sm" v-model="editableStudent.branch">
                  <strong v-else>{{ student.branch }}</strong>
                </li>
                <li>
                  <span>CGPA</span>
                  <input v-if="isEditing" type="number" step="0.1" class="form-control-sm" v-model="editableStudent.cgpa">
                  <strong v-else>{{ student.cgpa }}</strong>
                </li>
                <li>
                  <span>Graduation Year</span>
                  <input v-if="isEditing" type="text" class="form-control-sm" v-model="editableStudent.graduation_year">
                  <strong v-else>{{ student.graduation_year }}</strong>
                </li>
              </ul>
            </div>

            <div class="detail-section">
              <h5 class="section-title">Skills</h5>
              <div v-if="isEditing" class="skills-editor">
                <input type="text" class="form-control" v-model="editableStudent.skills" placeholder="Comma-separated skills">
              </div>
              <div v-else-if="student.skills" class="skills-tags">
                <span v-for="skill in student.skills.split(',')" :key="skill" class="skill-tag">
                  {{ skill.trim() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading Profile...</p>
      </div>
    </main>
  </div>
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
    // Append a timestamp to the URL to bypass browser cache
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
    // Set the editable copy *after* fetching the student data
    editableStudent.value = { ...data };
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

onMounted(fetchStudentProfile);

const startEditing = () => {
  // Ensure editableStudent is a fresh copy of the current student data
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
    // Update the main student data with the saved data
    student.value = { ...editableStudent.value };
    isEditing.value = false;
  } catch (error) {
    console.error('Error saving profile:', error);
  }
};

const cancelEdit = () => {
    // No need to copy, just toggle the editing flag
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
        // Directly update the avatar URL in the student data to trigger re-render
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
        }, 3000); // Wait for 3 seconds to allow the export to be generated
    } catch (error) {
        console.error('Error initiating export:', error);
        exporting.value = false;
    }
};

</script>

<style scoped>
/* ... styles remain the same ... */
</style>
