<template>
  <div class="admin-dashboard">
    <!-- Navbar placeholder -->
    <header class="w-100 bg-white">
      <div class="container py-3 px-4">
        <span class="fw-bold fs-5 text-dark">CampusConnect</span>
      </div>
    </header>

    <main class="container p-4 py-5">
      <!-- Header Section -->
      <div class="mb-5">
        <h1 class="fw-bold text-primary mb-2">Placement Cell HQ</h1>
        <p class="text-muted">Manage approvals, moderation, and institutional reports.</p>
      </div>

      <!-- Actions -->
      <div class="mb-5">
          <button class="btn btn-link p-0 text-dark fw-medium mb-3">Activity Report</button>
          <div class="position-relative">
             <i class="bi bi-search position-absolute text-muted search-icon"></i>
            <input 
              v-model="search" 
              type="text" 
              placeholder="Search portal..." 
              class="form-control ps-5 py-2 shadow-sm"
            />
          </div>
      </div>

      <!-- Stats Grid -->
      <div class="row g-4 mb-5">
        <div v-for="stat in stats" :key="stat.label" class="col-md-3">
          <div class="card stat-card h-100 p-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="text-sm font-medium text-muted">{{ stat.label }}</span>
                 <i :class="['h5', stat.icon, 'text-primary']"></i>
              </div>
              <div class="fs-4 fw-bold text-dark">{{ stat.value }}</div>
              <p class="text-xs mt-1 mb-0" :class="stat.trendClass">{{ stat.trend }}</p>
          </div>
        </div>
      </div>

      <!-- Main Content Tabs -->
      <div class="w-100">
        <div class="d-inline-flex p-1 rounded bg-light mb-4">
          <button 
            v-for="tab in ['Approvals', 'Moderation']" 
            :key="tab"
            @click="activeTab = tab"
            :class="[
              'btn btn-sm',
              activeTab === tab ? 'bg-white text-dark shadow-sm' : 'btn-light text-muted'
            ]"
          >
            {{ tab === 'Approvals' ? 'Pending Approvals' : 'User Moderation' }}
          </button>
        </div>

        <!-- Approvals Content -->
        <div v-if="activeTab === 'Approvals'" class="row g-4">
             <!-- Company Applications -->
            <div class="col-lg-6">
                <div class="card h-100 border-light-subtle shadow-sm">
                    <div class="card-body p-4">
                        <h5 class="card-title fw-semibold">Company Applications</h5>
                        <p class="card-subtitle text-muted">Verify and approve corporate registration requests.</p>
                        <div class="vstack gap-3 mt-4">
                            <div v-for="company in pendingCompanies" :key="company.id" class="d-flex justify-content-between align-items-center p-3 border rounded-3 bg-light bg-opacity-50">
                                <div>
                                    <p class="fw-semibold text-dark mb-0">{{ company.companyName }}</p>
                                    <p class="text-xs text-muted mb-0">{{ company.website }}</p>
                                </div>
                                <div class="d-flex gap-2">
                                    <button @click="updateStatus(company.id, 'COMPANY', 'REJECTED')" class="btn btn-sm btn-outline-danger">Reject</button>
                                    <button @click="updateStatus(company.id, 'COMPANY', 'APPROVED')" class="btn btn-sm btn-success">Approve</button>
                                </div>
                            </div>
                            <div v-if="!pendingCompanies.length" class="text-center py-5 text-muted fst-italic">No pending applications.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Drive Requests -->
            <div class="col-lg-6">
                <div class="card h-100 border-light-subtle shadow-sm">
                    <div class="card-body p-4">
                        <h5 class="card-title fw-semibold">Drive Approval Requests</h5>
                        <p class="card-subtitle text-muted">Review new placement drives submitted by companies.</p>
                        <div class="vstack gap-3 mt-4">
                            <div v-for="drive in pendingDrives" :key="drive.id" class="d-flex justify-content-between align-items-center p-3 border rounded-3 bg-light bg-opacity-50">
                                <div>
                                    <p class="fw-semibold text-dark mb-0">{{ drive.jobTitle }}</p>
                                    <p class="text-xs text-muted mb-0">{{ drive.companyName }}</p>
                                </div>
                                <div class="d-flex gap-2">
                                    <button @click="updateStatus(drive.id, 'DRIVE', 'REJECTED')" class="btn btn-sm btn-outline-danger">Reject</button>
                                    <button @click="updateStatus(drive.id, 'DRIVE', 'APPROVED')" class="btn btn-sm btn-success">Approve</button>
                                </div>
                            </div>
                            <div v-if="!pendingDrives.length" class="text-center py-5 text-muted fst-italic">No pending drive requests.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Moderation Content -->
        <div v-else class="card border-light-subtle shadow-sm">
          <div class="card-header bg-white d-flex flex-row align-items-center justify-content-between p-4">
            <div>
              <h5 class="fw-semibold mb-0">User Control Panel</h5>
              <p class="card-subtitle text-muted mt-1">Global management of students and approved companies.</p>
            </div>
            <button class="btn btn-light border">Export All Users</button>
          </div>
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="bg-light">
                <tr class="border-light-subtle">
                  <th class="px-4 py-3 text-uppercase text-muted fw-medium">Identity</th>
                  <th class="px-4 py-3 text-uppercase text-muted fw-medium">Access Role</th>
                  <th class="px-4 py-3 text-uppercase text-muted fw-medium">System Status</th>
                  <th class="px-4 py-3 text-uppercase text-muted fw-medium text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td class="px-4 py-3">
                    <div class="fw-bold text-dark">{{ user.name }}</div>
                    <div class="text-xs text-muted">{{ user.email }}</div>
                  </td>
                  <td class="px-4 py-3">
                    <span class="badge fw-semibold border border-light-subtle text-dark">{{ user.role }}</span>
                  </td>
                  <td class="px-4 py-3">
                    <span :class="[
                        'badge fw-semibold',
                        user.is_blacklisted ? 'bg-danger-soft text-danger' : 'bg-success-soft text-success'
                      ]"
                    >
                      {{ user.is_blacklisted ? 'Blacklisted' : 'Active' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-end">
                    <button @click="toggleBlacklist(user)" class="btn btn-link text-danger text-decoration-none fw-semibold p-0 text-xs">
                      <i class="bi bi-slash-circle me-1"></i>
                      {{ user.is_blacklisted ? 'Un-blacklist' : 'Blacklist' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const activeTab = ref('Approvals');
const search = ref('');
const pendingCompanies = ref([
  { id: '1', companyName: 'Amazon', website: 'https://amazon.jobs' },
]);
const pendingDrives = ref([
  { id: '1', jobTitle: 'AWS Solutions Architect', companyName: 'Amazon' }
]);
const users = ref([
  { id: '1', name: 'John Doe', email: 'john@insti.edu', role: 'Student', is_blacklisted: false },
  { id: '2', name: 'Innovate Corp', email: 'contact@innovate.com', role: 'Company', is_blacklisted: true }
]);

const stats = [
  { label: 'Total Students', value: '1,248', trend: 'Batch 2025', trendClass: 'text-muted', icon: 'bi-people' },
  { label: 'Active Companies', value: '86', trend: 'Approved partners', trendClass: 'text-success fw-medium', icon: 'bi-building' },
  { label: 'Active Drives', value: '24', trend: '1 pending', trendClass: 'text-warning fw-medium', icon: 'bi-briefcase' },
  { label: 'Placement %', value: '76.4%', trend: 'Target: 90%', trendClass: 'text-muted', icon: 'bi-bar-chart-line' },
];

const generateReport = () => {
  alert('Generating monthly placement activity report...');
};

const updateStatus = async (id, type, status) => {
  console.log(`Updating ${type} ${id} to ${status}`);
};

const toggleBlacklist = async (user) => {
  console.log(`Moderating user: ${user.name}`);
  user.is_blacklisted = !user.is_blacklisted;
};

const filteredUsers = computed(() => {
  return users.value.filter(u => 
    u.name.toLowerCase().includes(search.value.toLowerCase()) || 
    u.email.toLowerCase().includes(search.value.toLowerCase())
  );
});
</script>

<style scoped>
.admin-dashboard {
  background-color: #f8fafc; 
}
.text-primary {
    color: #4354e8 !important;
}
.fw-bold {
    font-weight: 700 !important;
}
.search-icon {
    top: 50%;
    left: 1.25rem;
    transform: translateY(-50%);
    pointer-events: none;
}

.ps-5 { padding-left: 3.5rem !important; }
.text-xs { font-size: .8rem; }
.fw-medium { font-weight: 500; }
.text-muted {
    color: #64748b !important; 
}

.stat-card {
    border: 1px solid #e2e8f0; 
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
}

.vstack { display: flex; flex-direction: column; }

.table-hover tbody tr:hover {
    background-color: #f8fafc;
}

.badge.bg-success-soft {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
}

.badge.bg-danger-soft {
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
}

.border-light-subtle { border-color: #e2e8f0 !important; }
.card {
    --bs-card-border-color: transparent;
}
</style>
