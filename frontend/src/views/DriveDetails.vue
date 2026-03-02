<template>
  <div class="drive-details-page">
    <div class="container my-5">
      <div v-if="drive" class="drive-content">
        
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-start mb-4">
          <div>
            <h1 class="fw-bold text-dark">{{ drive.title }}</h1>
            <p class="text-muted fw-medium">Posted by {{ drive.company }}</p>
          </div>
          <span class="badge bg-success-soft">Active</span>
        </div>

        <!-- Drive Info Card -->
        <div class="card info-card">
          <div class="card-body">
            <div class="row g-4">
              <div class="col-md-4 info-item">
                <h6 class="text-muted">Salary</h6>
                <p class="fw-semibold text-dark fs-5">{{ drive.salary }}</p>
              </div>
              <div class="col-md-4 info-item">
                <h6 class="text-muted">Location</h6>
                <p class="fw-semibold text-dark fs-5">{{ drive.location }}</p>
              </div>
              <div class="col-md-4 info-item">
                <h6 class="text-muted">Eligibility</h6>
                <p class="fw-semibold text-dark fs-5">{{ drive.branch }}</p>
              </div>
              <div class="col-md-4 info-item">
                <h6 class="text-muted">Minimum CGPA</h6>
                <p class="fw-semibold text-dark fs-5">{{ drive.cgpa }}</p>
              </div>
              <div class="col-md-4 info-item">
                <h6 class="text-muted">Application Deadline</h6>
                <p class="fw-semibold text-dark fs-5">{{ drive.deadline }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Job Description Card -->
        <div class="card description-card mt-4">
          <div class="card-body">
            <h5 class="fw-bold text-dark mb-3">Job Description</h5>
            <p class="text-muted">{{ drive.description }}</p>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="actions-bar mt-4">
          <button @click="apply" class="btn btn-primary btn-lg" :disabled="isApplied">
            <span v-if="isApplied">Applied</span>
            <span v-else>Apply Now</span>
          </button>
          <button class="btn btn-outline-secondary btn-lg ms-2">Save for Later</button>
        </div>

      </div>
      <div v-else class="loading-state">
        <div class="spinner-border text-primary"></div>
        <p class="mt-2">Loading Drive Details...</p>
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
    min-height: 100vh;
}

.drive-content {
    max-width: 900px;
    margin: auto;
}

.info-card, .description-card {
    border: none;
    border-radius: .75rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.fw-bold { font-weight: 700; }
.fw-semibold { font-weight: 600; }
.fw-medium { font-weight: 500; }

.text-dark { color: #1a202c !important; }
.text-muted { color: #64748b !important; }

.badge.bg-success-soft {
    font-size: .8rem;
    padding: .5em .9em;
}

.info-item h6 {
    font-size: .85rem;
    text-transform: uppercase;
    letter-spacing: .5px;
}

.loading-state {
    text-align: center;
    padding: 5rem;
}

.actions-bar {
    display: flex;
    justify-content: flex-end;
}
</style>
