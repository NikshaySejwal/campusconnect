<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <a href="/student-dashboard">Dashboard</a>
          <a href="/applications">My Applications</a>
          <a href="/profile/1">My Profile</a>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <div class="profile-card">
        <!-- Profile Header -->
        <div class="profile-header">
          <div class="avatar-wrapper">
            <img :src="`https://i.pravatar.cc/150?u=${student.id}`" alt="Profile Picture" class="avatar">
          </div>
          <div class="header-info">
            <h2 class="student-name">{{ student.name }}</h2>
            <p class="student-email">{{ student.email }}</p>
            <p v-if="!isEditing" class="student-bio">{{ student.bio }}</p>
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
                  <span>Graduation</span>
                  <input v-if="isEditing" type="text" class="form-control-sm" v-model="editableStudent.graduationYear">
                  <strong v-else>{{ student.graduationYear }}</strong>
                </li>
              </ul>
            </div>

            <!-- Skills -->
            <div class="detail-section">
              <h5 class="section-title">Skills</h5>
              <div v-if="isEditing" class="skills-editor">
                <input type="text" class="form-control" v-model="editableStudent.skills" placeholder="Comma-separated skills">
              </div>
              <div v-else class="skills-tags">
                <span v-for="skill in student.skills.split(',')" :key="skill" class="skill-tag">
                  {{ skill.trim() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const isEditing = ref(false);
const student = ref({
  id: '1', name: 'John Doe', email: 'john.doe@example.com',
  bio: 'Passionate developer with a knack for creating elegant and efficient solutions. Eager to contribute to a challenging and innovative team.',
  branch: 'Computer Science', cgpa: 8.8, graduationYear: 2025,
  skills: 'Vue.js, Node.js, Python, SQL, Docker',
});
const editableStudent = ref(null);

watch(isEditing, (isEditing) => {
  if (isEditing) editableStudent.value = { ...student.value };
});

const saveProfile = () => {
  student.value = { ...editableStudent.value };
  isEditing.value = false;
};

const cancelEdit = () => { isEditing.value = false; };
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
.avatar-wrapper { margin-right: 1.5rem; }
.avatar { width: 100px; height: 100px; border-radius: 50%; }
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
