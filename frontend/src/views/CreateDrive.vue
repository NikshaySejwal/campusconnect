<template>
  <div class="create-drive-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="text-center mb-5">
            <h1 class="fw-bold">Create a New Placement Drive</h1>
            <p class="text-muted">Streamline your recruitment process with a well-defined drive.</p>
          </div>

          <form @submit.prevent="createDrive" class="vstack gap-4">
            <!-- Job Description Card -->
            <div class="card shadow-sm">
              <div class="card-body p-4">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title fw-semibold mb-0">Job Description</h5>
                    <button type="button" class="btn btn-light btn-sm" @click="aiAssist">
                        <i class="bi bi-stars text-primary me-2"></i>AI Assist
                    </button>
                  </div>
                <div class="mb-3">
                  <label for="jobTitle" class="form-label">Job Title</label>
                  <input type="text" class="form-control" id="jobTitle" v-model="drive.title" placeholder="e.g., Software Development Engineer">
                </div>
                <div class="mb-3">
                  <label for="jobDescription" class="form-label">Detailed Description</label>
                  <textarea class="form-control" id="jobDescription" v-model="drive.description" rows="6" placeholder="Describe the role, responsibilities, and team."></textarea>
                </div>
              </div>
            </div>

            <!-- Requirements Card -->
            <div class="card shadow-sm">
              <div class="card-body p-4">
                <h5 class="card-title fw-semibold mb-3">Candidate Requirements</h5>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="requiredMajors" class="form-label">Eligible Majors</label>
                    <input type="text" class="form-control" id="requiredMajors" v-model="drive.majors" placeholder="e.g., Computer Science, Electrical Engineering">
                  </div>
                  <div class="col-md-6">
                    <label for="cgpaCutoff" class="form-label">Minimum CGPA</label>
                    <input type="number" step="0.1" class="form-control" id="cgpaCutoff" v-model="drive.cgpa" placeholder="e.g., 8.0">
                  </div>
                </div>
              </div>
            </div>

            <!-- Application Details Card -->
            <div class="card shadow-sm">
              <div class="card-body p-4">
                <h5 class="card-title fw-semibold mb-3">Application Details</h5>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="deadline" class="form-label">Application Deadline</label>
                    <input type="date" class="form-control" id="deadline" v-model="drive.deadline">
                  </div>
                  <div class="col-md-6">
                    <label for="salary" class="form-label">Compensation (CTC)</label>
                    <input type="text" class="form-control" id="salary" v-model="drive.salary" placeholder="e.g., 12 LPA">
                  </div>
                </div>
              </div>
            </div>

            <div class="d-grid">
              <button type="submit" class="btn btn-primary btn-lg">Publish Drive</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const drive = ref({
  title: '',
  description: '',
  majors: '',
  cgpa: null,
  deadline: '',
  salary: '',
});

const aiAssist = () => {
  // Simulate AI generating content
  drive.value.description = 'As a Software Development Engineer, you will work with a team of talented engineers to design, build, and ship features for our flagship product. You will be responsible for writing clean, maintainable code and ensuring the performance and reliability of our systems.';
};

const createDrive = () => {
  console.log('Creating drive with data:', drive.value);
  // POST request to /api/drives would be sent here
  alert('Placement drive has been successfully created!');
};
</script>

<style scoped>
.create-drive-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.form-label {
    font-weight: 500;
}
</style>
