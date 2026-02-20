<template>
  <div class="page-wrapper">
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
              </div>
              <div class="card-body">
                <div class="form-group">
                  <label for="jobTitle">Job Title</label>
                  <input type="text" class="form-control" id="jobTitle" v-model="drive.job_title" placeholder="e.g., Software Development Engineer" required>
                </div>
                <div class="form-group">
                  <label for="jobDescription">Detailed Description</label>
                  <textarea class="form-control" id="jobDescription" v-model="drive.job_description" rows="6" placeholder="Describe the role, responsibilities, and team." required></textarea>
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
                    <label for="eligibility_branch">Eligible Branches</label>
                    <input type="text" class="form-control" id="eligibility_branch" v-model="drive.eligibility_branch" placeholder="e.g., Computer Science, IT" required>
                  </div>
                  <div class="form-group-col">
                    <label for="eligibility_min_cgpa">Minimum CGPA</label>
                    <input type="number" step="0.1" class="form-control" id="eligibility_min_cgpa" v-model.number="drive.eligibility_min_cgpa" placeholder="e.g., 8.0" required>
                  </div>
                   <div class="form-group-col">
                    <label for="eligibility_year">Eligibility Year</label>
                    <input type="number" class="form-control" id="eligibility_year" v-model.number="drive.eligibility_year" placeholder="e.g., 2025" required>
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
                    <label for="application_deadline">Application Deadline</label>
                    <input type="date" class="form-control" id="application_deadline" v-model="drive.application_deadline" required>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

            <div class="submit-button-wrapper">
              <button type="submit" class="publish-drive-btn" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Publishing...' : 'Publish Drive' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const drive = ref({
  job_title: '',
  job_description: '',
  eligibility_branch: '',
  eligibility_min_cgpa: null,
  eligibility_year: null,
  application_deadline: '',
});

const isLoading = ref(false);
const error = ref(null);

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const createDrive = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await fetch('/api/company/drives', {
      method: 'POST',
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
      body: JSON.stringify(drive.value),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Failed to create drive.');
    }
    // On success, redirect to dashboard
    router.push('/company/dashboard');
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.container { max-width: 960px; }

.page-header { text-align: center; margin-bottom: 3rem; }
.page-title { font-size: 2.5rem; font-weight: 800; color: #2c3e50; }
.page-subtitle { font-size: 1.1rem; color: #6c757d; }

.form-wrapper { display: flex; flex-direction: column; gap: 1.5rem; }
.form-card { background-color: white; border-radius: 12px; border: 1px solid #dee2e6; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.card-header { padding: 1rem 1.5rem; border-bottom: 1px solid #e9ecef; }
.card-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0; }
.card-body { padding: 1.5rem; }

.form-group, .form-group-col { margin-bottom: 1.5rem; }
.form-group:last-child, .form-group-col:last-child { margin-bottom: 0; }

.form-label, label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #343a40; }
.form-control { width: 100%; padding: 12px 16px; border: 1px solid #ced4da; border-radius: 8px; font-size: 1rem; transition: border-color 0.2s, box-shadow 0.2s; }
.form-control:focus { outline: none; border-color: #3F51B5; box-shadow: 0 0 0 3px rgba(63, 81, 181, 0.1); }

.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }

.submit-button-wrapper { text-align: right; margin-top: 1rem; }
.publish-drive-btn { background-color: #3F51B5; color: white; border: none; padding: 14px 32px; font-size: 1.1rem; font-weight: 600; border-radius: 8px; cursor: pointer; transition: background-color 0.2s; }
.publish-drive-btn:hover { background-color: #303f9f; }
.publish-drive-btn:disabled { background-color: #9fa8da; cursor: not-allowed; }

</style>
