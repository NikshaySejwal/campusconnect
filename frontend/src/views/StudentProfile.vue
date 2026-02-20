<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <router-link :to="{ name: 'StudentDashboard' }">Dashboard</router-link>
          <router-link :to="{ name: 'ApplicationHistory' }">My Applications</router-link>
          <router-link :to="{ name: 'StudentProfile' }">My Profile</router-link>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <div v-if="student" class="profile-card">
        <!-- Profile Header -->
        <div class="profile-header">
          <div class="avatar-wrapper">
            <img :src="fullAvatarUrl" alt="Profile Picture" class="avatar">
            <div class="avatar-overlay" @click="triggerFileInput">
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
            <button v-if="!isEditing" @click="isEditing = true" class="btn-edit">Edit Profile</button>
            <button v-if="isEditing" @click="saveProfile" class="btn-save">Save</button>
            <button v-if="isEditing" @click="cancelEdit" class="btn-cancel">Cancel</button>
          </div>
        </div>

        <!-- Profile Body -->
        <div class="profile-body">
          <div v-if="isEditing" class="bio-editor">
            <label for="bio">Profile Bio</label>
            <textarea v-model="editableStudent.bio" id="bio" class="form-control" rows="3"></textarea>
          </div>

          <div class="details-grid">
            <!-- Academics -->
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

            <!-- Skills -->
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
import { ref, watch, onMounted, computed } from 'vue';

const isEditing = ref(false);
const student = ref(null);
const editableStudent = ref(null);
const fileInput = ref(null);

const fullAvatarUrl = computed(() => {
  if (student.value?.avatar_url) {
    return student.value.avatar_url;
  }
  return `https://i.pravatar.cc/150`;
});

const getAuthHeader = (isMultipart = false) => {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` };
    if (!isMultipart) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
};

const fetchStudentProfile = async () => {
  try {
    const response = await fetch('/api/student/profile', { headers: getAuthHeader() });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || data.msg || `Failed to fetch profile: ${response.statusText}`);
    }
    student.value = data;
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

onMounted(fetchStudentProfile);

watch(student, (newStudent) => {
  if (newStudent) {
    editableStudent.value = { ...newStudent };
  }
});

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
    await fetchStudentProfile();
    isEditing.value = false;
  } catch (error) {
    console.error('Error saving profile:', error);
  }
};

const cancelEdit = () => {
    editableStudent.value = { ...student.value };
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
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || data.msg || 'Failed to upload avatar');
        }
        await fetchStudentProfile();
    } catch (error) {
        console.error('Error uploading avatar:', error);
    }
};

</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.container { max-width: 960px; }

/* Header */
.main-header { background: white; border-bottom: 1px solid #dee2e6; padding: 1rem 0; }
nav.container { display: flex; justify-content: space-between; align-items: center; }
.logo { font-weight: 700; font-size: 1.5rem; color: #3F51B5; }
.nav-links { display: flex; align-items: center; gap: 1.5rem; font-weight: 500; }
.nav-links a { text-decoration: none; color: #212529; }

/* Profile Card */
.profile-card { background: white; border-radius: 16px; border: 1px solid #dee2e6; box-shadow: 0 8px 24px rgba(0,0,0,0.05); margin-top: 2rem; }

.profile-header {
  display: flex; align-items: flex-start; padding: 2rem; border-bottom: 1px solid #e9ecef;
}
.avatar-wrapper { 
    margin-right: 1.5rem; 
    position: relative; 
    cursor: pointer;
}
.avatar { 
    width: 100px; 
    height: 100px; 
    border-radius: 50%; 
    object-fit: cover; 
    display: block;
}

.avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: rgba(0,0,0,0.5);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}
.avatar-wrapper:hover .avatar-overlay {
    opacity: 1;
}
.avatar-overlay i { font-size: 1.5rem; }
.avatar-overlay span { font-size: 0.8rem; margin-top: 0.25rem; }

.header-info { flex-grow: 1; }
.student-name { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
.student-email { color: #6c757d; margin-bottom: 0.75rem; }
.student-bio { font-size: 1rem; color: #495057; }

.header-actions button { padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; border: 1px solid; }
.btn-edit { color: #3F51B5; background-color: transparent; border-color: #3F51B5; }
.btn-save { color: white; background-color: #3F51B5; border-color: #3F51B5; margin-right: 0.5rem;}
.btn-cancel { color: #6c757d; background-color: transparent; border-color: #dee2e6; }

.profile-body { padding: 2rem; }
.bio-editor { margin-bottom: 2rem; }
.bio-editor label { display: block; margin-bottom: 0.5rem; font-weight: 600; }
.form-control { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ced4da; }

.details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
.section-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 1.5rem; border-bottom: 2px solid #3F51B5; padding-bottom: 0.5rem;}

.info-list { list-style: none; padding: 0; }
.info-list li { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f1f3f5; }
.info-list li:last-child { border-bottom: none; }
.info-list span { color: #6c757d; }
.info-list strong { color: #212529; font-weight: 600; }
.form-control-sm { padding: 6px 10px; border: 1px solid #ced4da; border-radius: 6px; width: 60%; }

.skills-editor { margin-top: -1rem; }
.skills-tags { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.skill-tag { background-color: #e8eaf6; color: #3F51B5; padding: 6px 12px; border-radius: 16px; font-size: 0.9rem; font-weight: 500; }
</style>