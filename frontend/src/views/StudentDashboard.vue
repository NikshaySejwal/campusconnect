<template>
  <main class="container py-4">
    <!-- Page Header -->
    <div class="page-header mb-4">
      <div>
        <h1 class="fw-bold">Welcome, {{ studentName || 'Student' }}!</h1>
        <p class="text-muted">Explore and apply to the latest placement drives from top companies.</p>
      </div>
    </div>

    <!-- Available Drives -->
    <h4 class="fw-semibold mb-3">Available Drives</h4>
    <div v-if="availableDrives.length" class="vstack gap-3">
      <div v-for="drive in availableDrives" :key="drive.id" class="card list-item-card">
        <div class="card-body p-4 d-flex flex-column flex-md-row align-items-start align-items-md-center">
          
          <div class="d-flex align-items-center flex-grow-1 mb-3 mb-md-0">
            <div class="company-logo-wrapper me-3">
              <img :src="`https://logo.clearbit.com/${drive.company.toLowerCase().replace(/ /g, '')}.com`" :alt="drive.company" class="company-logo">
            </div>
            <div>
              <h5 class="card-title fw-bold mb-1">{{ drive.title }}</h5>
              <p class="card-subtitle text-muted fw-semibold mb-2">{{ drive.company }}</p>
              <div class="d-flex flex-wrap gap-3 text-muted text-xs">
                <span><i class="bi bi-cash-stack me-1"></i>{{ drive.salary }}</span>
                <span><i class="bi bi-geo-alt-fill me-1"></i>{{ drive.location }}</span>
                <span><i class="bi bi-calendar-event-fill me-1"></i>Deadline: {{ new Date(drive.deadline).toLocaleDateString() }}</span>
              </div>
            </div>
          </div>

          <div class="ms-md-4">
            <router-link :to="{ name: 'DriveDetails', params: { id: drive.id } }" class="btn btn-primary">View Details</router-link>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-5 text-muted fst-italic border rounded-3">
      <p>No placement drives are currently available for you.</p>
      <p class="mb-0">This may be because no drives match your profile or no drives have been approved yet.</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const student = ref(null);
const availableDrives = ref([]);

const studentName = computed(() => {
  if (student.value) {
    return student.value.name;
  }
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    return JSON.parse(storedUser).name;
  }
  return 'Student';
});

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const fetchStudentProfile = async () => {
  try {
    const response = await fetch('/api/student/profile', { headers: getAuthHeader() });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || data.msg || 'Failed to fetch student profile');
    }
    student.value = data;
  } catch (error) {
    console.error('Error fetching student profile:', error);
  }
};

const fetchAvailableDrives = async () => {
    try {
        const response = await fetch('/api/student/drives', { headers: getAuthHeader() });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || data.msg || 'Failed to fetch drives');
        }
        availableDrives.value = data.drives;
    } catch (error) {
        console.error('Failed to fetch drives:', error);
    }
};

onMounted(async () => {
  await fetchStudentProfile();
  await fetchAvailableDrives();
});
</script>

<style scoped>
.page-header {
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.list-item-card {
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}

.company-logo-wrapper {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: .375rem;
  border: 1px solid #e2e8f0;
  background-color: white;
}

.company-logo {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

.fw-bold { font-weight: 700 !important; }
.fw-semibold { font-weight: 600; }
.text-muted { color: #64748b !important; }
.text-xs { font-size: 0.8rem; }
</style>
