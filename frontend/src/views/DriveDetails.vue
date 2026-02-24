<template>
  <div class="drive-details-page">
    <div class="container my-5">
      <div v-if="drive" class="drive-content">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="card-title fw-bold">{{ drive.title }}</h1>
                <span class="badge bg-success-soft">Active</span>
            </div>

            <div class="mb-4">
                <h5 class="text-primary fw-semibold">{{ drive.company }}</h5>
                <p class="text-muted">
                    {{ drive.description.substring(0, 100) }}...
                </p>
            </div>

            <div class="row border-top pt-4 mb-4">
                <div class="col-md-3">
                    <p class="text-muted mb-1">Salary</p>
                    <h6 class="fw-semibold">{{ drive.salary }}</h6>
                </div>
                <div class="col-md-3">
                    <p class="text-muted mb-1">Location</p>
                    <h6 class="fw-semibold">{{ drive.location }}</h6>
                </div>
                <div class="col-md-3">
                    <p class="text-muted mb-1">Eligibility</p>
                    <h6 class="fw-semibold">{{ drive.branch }}</h6>
                </div>
                <div class="col-md-3">
                    <p class="text-muted mb-1">Min CGPA</p>
                    <h6 class="fw-semibold">{{ drive.cgpa }}</h6>
                </div>
                <div class="col-md-3 mt-3">
                    <p class="text-muted mb-1">Deadline</p>
                    <h6 class="fw-semibold">{{ drive.deadline }}</h6>
                </div>
            </div>

            <h5 class="fw-bold mb-3">Job Description</h5>
            <p class="text-muted">{{ drive.description }}</p>

            <div class="mt-5">
                <button @click="apply" class="btn btn-primary btn-lg" :disabled="isApplied">
                  <span v-if="isApplied">Applied</span>
                  <span v-else>Apply Now</span>
                </button>
                <button class="btn btn-outline-secondary btn-lg ms-2">Save for Later</button>
            </div>
        </div>
      </div>
      <div v-else class="loading-state">
        <p>Loading...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const drive = ref(null);
const route = useRoute();
const isApplied = ref(false);

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

onMounted(async () => {
  const driveId = route.params.id;
  try {
    const response = await fetch(`/api/drive/${driveId}`);
    const data = await response.json();
    drive.value = {
        ...data,
        deadline: new Date(data.deadline).toLocaleDateString()
    };
  } catch (error) {
    console.error('Failed to fetch drive details:', error);
  }
});

const apply = async () => {
  const driveId = route.params.id;
  try {
    const response = await fetch(`/api/student/drive/${driveId}/apply`, {
      method: 'POST',
      headers: getAuthHeader(),
    });
    const data = await response.json();
    if (response.ok) {
      isApplied.value = true;
    } else {
      throw new Error(data.message || 'Failed to apply');
    }
  } catch (error) {
    console.error('Failed to apply:', error);
    alert(error.message);
  }
};
</script>

<style scoped>

.drive-details-page {
    background-color: #f8fafc;
}
.drive-content {
    max-width: 800px;
    margin: auto;
    background: white;
    padding: 2.5rem;
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
}

.fw-bold { font-weight: 700; }
.fw-semibold { font-weight: 600; }
.text-primary { color: #4f46e5 !important; }
.text-muted { color: #64748b !important; }

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
    font-size: .8rem;
    padding: .5em .9em;
}
</style>
