<template>
  <div class="student-profile-page bg-light">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">

          <div class="card shadow-sm">
            <div class="card-body p-4">
              <!-- Profile Header -->
              <div class="d-flex flex-column flex-sm-row align-items-center mb-4">
                <img :src="`https://i.pravatar.cc/150?u=${student.id}`" alt="Profile Picture" class="rounded-circle me-sm-4 mb-3 mb-sm-0" width="100" height="100">
                <div class="text-center text-sm-start flex-grow-1">
                  <h2 class="fw-bold mb-1">{{ student.name }}</h2>
                  <p class="text-muted mb-2">{{ student.email }}</p>
                  <p v-if="!isEditing" class="text-sm text-muted">{{ student.bio }}</p>
                </div>
                <div class="mt-3 mt-sm-0">
                   <button v-if="!isEditing" @click="isEditing = true" class="btn btn-outline-primary">Edit Profile</button>
                   <button v-if="isEditing" @click="saveProfile" class="btn btn-primary me-2">Save</button>
                   <button v-if="isEditing" @click="cancelEdit" class="btn btn-light">Cancel</button>
                </div>
              </div>

              <!-- Profile Content -->
              <div>
                 <div v-if="isEditing" class="mb-4">
                     <label for="bio" class="form-label fw-semibold">Profile Bio</label>
                     <textarea v-model="editableStudent.bio" id="bio" class="form-control" rows="3"></textarea>
                 </div>

                <div class="row g-4">
                    <!-- Academics -->
                    <div class="col-md-6">
                        <h5 class="fw-semibold mb-3">Academics</h5>
                        <div class="vstack gap-2">
                           <div class="d-flex justify-content-between">
                               <span class="text-muted">Branch</span>
                               <input v-if="isEditing" type="text" class="form-control form-control-sm w-50" v-model="editableStudent.branch">
                               <span v-else class="fw-medium">{{ student.branch }}</span>
                           </div>
                           <div class="d-flex justify-content-between">
                               <span class="text-muted">CGPA</span>
                               <input v-if="isEditing" type="number" step="0.1" class="form-control form-control-sm w-50" v-model="editableStudent.cgpa">
                               <span v-else class="fw-medium">{{ student.cgpa }}</span>
                           </div>
                             <div class="d-flex justify-content-between">
                               <span class="text-muted">Graduation</span>
                               <input v-if="isEditing" type="text" class="form-control form-control-sm w-50" v-model="editableStudent.graduationYear">
                               <span v-else class="fw-medium">{{ student.graduationYear }}</span>
                           </div>
                        </div>
                    </div>
                    <!-- Skills -->
                    <div class="col-md-6">
                        <h5 class="fw-semibold mb-3">Skills</h5>
                        <div v-if="isEditing">
                            <input type="text" class="form-control" v-model="editableStudent.skills" placeholder="Comma-separated skills">
                        </div>
                        <div v-else class="d-flex flex-wrap gap-2">
                            <span v-for="skill in student.skills.split(',')" :key="skill" class="badge bg-primary-soft text-primary fw-medium">
                                {{ skill.trim() }}
                            </span>
                        </div>
                    </div>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isEditing = ref(false);

const student = ref({
  id: '1',
  name: 'John Doe',
  email: 'john.doe@example.com',
  bio: 'Passionate developer with a knack for creating elegant and efficient solutions. Eager to contribute to a challenging and innovative team.',
  branch: 'Computer Science',
  cgpa: 8.8,
  graduationYear: 2025,
  skills: 'Vue.js, Node.js, Python, SQL, Docker',
});

const editableStudent = ref(null);

onMounted(() => {
  // In a real app, you would fetch the student data based on route.params.id
});

const saveProfile = () => {
  student.value = { ...editableStudent.value };
  isEditing.value = false;
  console.log('Profile saved:', student.value);
  // API call to save data would go here
};

const cancelEdit = () => {
    isEditing.value = false;
}

// Watch for isEditing to change to clone the student object
import { watch } from 'vue';
watch(isEditing, (newValue) => {
    if (newValue) {
        editableStudent.value = { ...student.value };
    }
});

</script>

<style scoped>
.student-profile-page {
  min-height: 100vh;
}
.fw-semibold { font-weight: 600; }
.fw-medium { font-weight: 500; }
.fw-bold { font-weight: 700; }
.text-muted { color: #64748b !important; }
.text-sm { font-size: 0.9rem; }

.badge.bg-primary-soft {
    background-color: #eef2ff !important;
    color: #4338ca !important;
    font-size: .8rem;
    padding: .5em .8em;
}
</style>
