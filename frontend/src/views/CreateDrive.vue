<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#portal">Portal Access</a>
          <button class="cta-button-main">Get Started</button>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-9">
          <div class="page-header">
            <h1 class="page-title">Create a New Placement Drive</h1>
            <p class="page-subtitle">Streamline your recruitment process with a well-defined drive.</p>
          </div>

          <form @submit.prevent="createDrive" class="form-wrapper">
            <!-- Job Description Card -->
            <div class="form-card">
              <div class="card-header">
                <h5 class="card-title">Job Description</h5>
                <button type="button" class="ai-assist-btn" @click="aiAssist">&#x2728; AI Assist</button>
              </div>
              <div class="card-body">
                <div class="form-group">
                  <label for="jobTitle">Job Title</label>
                  <input type="text" class="form-control" id="jobTitle" v-model="drive.title" placeholder="e.g., Software Development Engineer">
                </div>
                <div class="form-group">
                  <label for="jobDescription">Detailed Description</label>
                  <textarea class="form-control" id="jobDescription" v-model="drive.description" rows="6" placeholder="Describe the role, responsibilities, and team."></textarea>
                </div>
              </div>
            </div>

            <!-- Requirements Card -->
            <div class="form-card">
              <div class="card-header">
                  <h5 class="card-title">Candidate Requirements</h5>
              </div>
              <div class="card-body">
                <div class="form-row">
                  <div class="form-group-col">
                    <label for="requiredMajors">Eligible Majors</label>
                    <input type="text" class="form-control" id="requiredMajors" v-model="drive.majors" placeholder="e.g., Computer Science, IT">
                  </div>
                  <div class="form-group-col">
                    <label for="cgpaCutoff">Minimum CGPA</label>
                    <input type="number" step="0.1" class="form-control" id="cgpaCutoff" v-model="drive.cgpa" placeholder="e.g., 8.0">
                  </div>
                </div>
              </div>
            </div>

            <!-- Application Details Card -->
            <div class="form-card">
              <div class="card-header">
                  <h5 class="card-title">Application Details</h5>
              </div>
              <div class="card-body">
                <div class="form-row">
                  <div class="form-group-col">
                    <label for="deadline">Application Deadline</label>
                    <input type="date" class="form-control" id="deadline" v-model="drive.deadline">
                  </div>
                  <div class="form-group-col">
                    <label for="salary">Compensation (CTC)</label>
                    <input type="text" class="form-control" id="salary" v-model="drive.salary" placeholder="e.g., 12 LPA">
                  </div>
                </div>
              </div>
            </div>

            <div class="submit-button-wrapper">
              <button type="submit" class="publish-drive-btn">Publish Drive</button>
            </div>
          </form>
        </div>
      </div>
    </main>
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
  drive.value.description = 'As a Software Development Engineer, you will work with a team of talented engineers to design, build, and ship features for our flagship product. You will be responsible for writing clean, maintainable code and ensuring the performance and reliability of our systems.';
};

const createDrive = () => {
  console.log('Creating drive with data:', drive.value);
  alert('Placement drive has been successfully created!');
};
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.container { max-width: 960px; }

.main-header { background: white; border-bottom: 1px solid #dee2e6; padding: 1rem 0; position: sticky; top: 0; z-index: 10; }
nav.container { display: flex; justify-content: space-between; align-items: center; }
.logo { font-weight: 700; font-size: 1.5rem; color: #3F51B5; }
.nav-links { display: flex; align-items: center; gap: 1.5rem; font-weight: 500; }
.nav-links a { text-decoration: none; color: #212529; }
.cta-button-main { background-color: #3F51B5; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; }

.page-header { text-align: center; margin-bottom: 3rem; }
.page-title { font-size: 2.5rem; font-weight: 800; color: #2c3e50; }
.page-subtitle { font-size: 1.1rem; color: #6c757d; }

.form-wrapper { display: flex; flex-direction: column; gap: 1.5rem; }
.form-card { background-color: white; border-radius: 12px; border: 1px solid #dee2e6; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.card-header { padding: 1rem 1.5rem; border-bottom: 1px solid #e9ecef; display: flex; justify-content: space-between; align-items: center; }
.card-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0; }
.card-body { padding: 1.5rem; }

.form-group, .form-group-col { margin-bottom: 1.5rem; }
.form-group:last-child, .form-group-col:last-child { margin-bottom: 0; }

.form-label, label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #343a40; }
.form-control { width: 100%; padding: 12px 16px; border: 1px solid #ced4da; border-radius: 8px; font-size: 1rem; background-color: #f8f9fa; transition: border-color 0.2s, box-shadow 0.2s; }
.form-control:focus { outline: none; border-color: #3F51B5; box-shadow: 0 0 0 3px rgba(63, 81, 181, 0.1); }

.ai-assist-btn { background-color: #e8eaf6; color: #3F51B5; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; }

.form-row { display: flex; flex-wrap: wrap; gap: 1.5rem; }
.form-group-col { flex: 1; min-width: 250px; /* Ensures columns can shrink but have a minimum width */ }

.submit-button-wrapper { text-align: right; margin-top: 1rem; }
.publish-drive-btn { background-color: #3F51B5; color: white; border: none; padding: 14px 32px; font-size: 1.1rem; font-weight: 600; border-radius: 8px; cursor: pointer; transition: background-color 0.2s; }
.publish-drive-btn:hover { background-color: #303f9f; }

/* Responsive adjustments */
@media (max-width: 768px) {
  .form-row { flex-direction: column; gap: 0; }
  .form-group-col { margin-bottom: 1.5rem; }
  .nav-links { display: none; } /* Example: Hide nav links on small screens */
}
</style>
