<template>
  <div class="screening-room-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-11">

          <!-- Header -->
          <div class="mb-5">
            <p class="text-primary fw-semibold">Applicants for:</p>
            <h1 class="fw-bold">Software Development Engineer</h1>
          </div>

          <!-- Summary & Actions -->
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <div class="d-flex flex-column flex-md-row justify-content-between align-items-center">
                <!-- Stats -->
                <div class="d-flex gap-4 mb-3 mb-md-0">
                  <div v-for="stat in applicantStats" :key="stat.label">
                    <span class="fs-4 fw-bold">{{ stat.value }}</span>
                    <span class="text-muted ms-2">{{ stat.label }}</span>
                  </div>
                </div>
                <!-- Actions -->
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-secondary">Reject Selected</button>
                  <button class="btn btn-primary">Shortlist Selected</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Applicant Table -->
          <div class="card shadow-sm">
             <div class="card-header bg-white p-4">
                <input type="text" class="form-control" placeholder="Search applicants...">
            </div>
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="p-3" style="width: 50px;">
                        <input class="form-check-input" type="checkbox" @change="toggleSelectAll">
                    </th>
                    <th class="p-3">Applicant</th>
                    <th class="p-3">Applied On</th>
                    <th class="p-3">Status</th>
                    <th class="p-3 text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="applicant in applicants" :key="applicant.id">
                    <td class="p-3 align-middle">
                        <input class="form-check-input" type="checkbox" :value="applicant.id" v-model="selectedApplicants">
                    </td>
                    <td class="p-3 align-middle">
                      <div class="d-flex align-items-center">
                        <img :src="`https://i.pravatar.cc/150?u=${applicant.id}`" alt="" class="rounded-circle me-3" width="40" height="40">
                        <div>
                          <h6 class="fw-semibold mb-0">{{ applicant.name }}</h6>
                          <p class="text-muted text-xs mb-0">{{ applicant.major }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="p-3 align-middle text-muted">{{ applicant.appliedDate }}</td>
                    <td class="p-3 align-middle">
                      <span :class="['badge', getStatusClass(applicant.status)]">{{ applicant.status }}</span>
                    </td>
                    <td class="p-3 align-middle text-end">
                      <a href="#" class="btn btn-sm btn-outline-secondary me-2">View Profile</a>
                      <button v-if="applicant.status === 'Pending'" @click="shortlistApplicant(applicant.id)" class="btn btn-sm btn-success-soft">Shortlist</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const applicantStats = ref([
  { label: 'Total', value: 25 },
  { label: 'Pending', value: 10 },
  { label: 'Shortlisted', value: 5 },
]);

const applicants = ref([
  { id: 1, name: 'John Doe', major: 'Computer Science', appliedDate: '2024-07-28', status: 'Pending' },
  { id: 2, name: 'Jane Smith', major: 'Electrical Engineering', appliedDate: '2024-07-27', status: 'Shortlisted' },
  { id: 3, name: 'Peter Jones', major: 'Computer Science', appliedDate: '2024-07-26', status: 'Rejected' },
]);

const selectedApplicants = ref([]);

const toggleSelectAll = (event) => {
  if (event.target.checked) {
    selectedApplicants.value = applicants.value.map(a => a.id);
  } else {
    selectedApplicants.value = [];
  }
};

const getStatusClass = (status) => {
  const map = {
    Pending: 'bg-warning-soft text-warning',
    Shortlisted: 'bg-success-soft text-success',
    Rejected: 'bg-danger-soft text-danger',
  };
  return map[status];
};

const shortlistApplicant = (id) => {
    const applicant = applicants.value.find(a => a.id === id);
    if(applicant) applicant.status = 'Shortlisted';
}
</script>

<style scoped>
.screening-room-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.fw-semibold { font-weight: 600; }
.fw-bold { font-weight: 700; }
.text-muted { color: #64748b !important; }
.text-primary { color: #4f46e5 !important; }
.text-xs { font-size: 0.8rem; }

.badge {
  font-size: .75rem;
  padding: .4em .7em;
  font-weight: 600;
}

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
}
.btn-success-soft { 
    background-color: #f0fdf4 !important;
    color: #166534 !important;
    border: 1px solid #bbf7d0;
}

.badge.bg-danger-soft {
    background-color: #fef2f2 !important;
    border: 1px solid #fecaca;
    color: #991b1b !important;
}

.badge.bg-warning-soft {
    background-color: #fffbeb !important;
    border: 1px solid #fde68a;
    color: #854d0e !important;
}
.table-hover tbody tr:hover {
    background-color: #f8fafc;
}
</style>
