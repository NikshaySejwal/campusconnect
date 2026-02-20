<template>
  <div class="admin-dashboard">
    <!-- Navbar placeholder -->
    <header class="bg-white">
      <div class="container py-3 px-4">
        <span class="fw-bold fs-5 text-dark">CampusConnect</span>
      </div>
    </header>

    <main class="dashboard">
      <!-- Header Section -->
      <div class="header-content">
        <h1 class="fw-bold text-primary mb-2">Placement Cell HQ</h1>
        <p class="text-muted">Manage approvals, moderation, and institutional reports.</p>
      </div>

      <!-- Actions -->
      <div class="actions-toolbar">
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

      <!-- Stats -->
      <div class="metrics-row">
        <div v-for="stat in stats" :key="stat.label" class="metric-card">
          <div class="card stat-card h-100 p-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="text-sm font-medium text-muted">{{ stat.label }}</span>
                 <i :class="['h5', stat.icon, 'text-primary']"></i>
              </div>
              <div class="fs-4 fw-bold text-dark">{{ stat.value }}</div>
              <p class="text-xs mt-1 mb-0 text-muted">{{ stat.trend }}</p>
          </div>
        </div>
      </div>

      <!-- Main Content Tabs -->
      <div class="tabs-container">
        <div class="tabs-row">
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
        <div v-if="activeTab === 'Approvals'" class="approvals-row">
             <!-- Company Applications -->
            <div class="approval-panel">
                <div class="card h-100 border-light-subtle shadow-sm">
                    <div class="card-body p-4">
                        <h5 class="card-title fw-semibold">Company Applications</h5>
                        <p class="card-subtitle text-muted">Verify and approve corporate registration requests.</p>
                        <div class="content-stack mt-4">
                            <div v-for="company in pendingCompanies" :key="company.id" class="d-flex justify-content-between align-items-center p-3 border rounded-3 bg-light bg-opacity-50">
                                <div>
                                    <p class="fw-semibold text-dark mb-0">{{ company.company_name }}</p>
                                    <p class="text-xs text-muted mb-0">{{ company.email }}</p>
                                </div>
                                <div class="d-flex gap-2">
                                    <button @click="updateCompanyStatus(company.id, 'REJECTED')" class="btn btn-sm btn-outline-danger">Reject</button>
                                    <button @click="updateCompanyStatus(company.id, 'APPROVED')" class="btn btn-sm btn-success">Approve</button>
                                </div>
                            </div>
                            <div v-if="!pendingCompanies.length" class="text-center py-5 text-muted fst-italic">No pending applications.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Drive Requests -->
            <div class="approval-panel">
                <div class="card h-100 border-light-subtle shadow-sm">
                    <div class="card-body p-4">
                        <h5 class="card-title fw-semibold">Drive Approval Requests</h5>
                        <p class="card-subtitle text-muted">Review new placement drives submitted by companies.</p>
                        <div class="content-stack mt-4">
                            <div v-for="drive in pendingDrives" :key="drive.id" class="d-flex justify-content-between align-items-center p-3 border rounded-3 bg-light bg-opacity-50">
                                <div>
                                    <p class="fw-semibold text-dark mb-0">{{ drive.title }}</p>
                                    <p class="text-xs text-muted mb-0">{{ drive.company }}</p>
                                </div>
                                <div class="d-flex gap-2">
                                    <button @click="updateDriveStatus(drive.id, 'REJECTED')" class="btn btn-sm btn-outline-danger">Reject</button>
                                    <button @click="updateDriveStatus(drive.id, 'APPROVED')" class="btn btn-sm btn-success">Approve</button>
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
                  <td v-if="user.role === 'Student'" class="px-4 py-3 text-end">
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
import { ref, computed, onMounted } from 'vue';

const activeTab = ref('Approvals');
const search = ref('');

const stats = ref([]);
const allCompanies = ref([]);
const allDrives = ref([]);
const allStudents = ref([]);

const pendingCompanies = computed(() => allCompanies.value.filter(c => c.approval_status === 'PENDING'));

// Correctly filter drives with a 'PENDING' status.
const pendingDrives = computed(() => allDrives.value.filter(d => d.status === 'PENDING'));

const users = computed(() => {
  const students = allStudents.value.map(s => ({ ...s, role: 'Student' }));
  const companies = allCompanies.value.map(c => ({ ...c, name: c.company_name, role: 'Company' }));
  return [...students, ...companies];
});

const filteredUsers = computed(() => {
  return users.value.filter(u =>
    u.name.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase())
  );
});

const getAuthHeader = () => ({ 'Authorization': `Bearer ${localStorage.getItem('access_token')}` });

const fetchData = async (url) => {
  const response = await fetch(url, { headers: getAuthHeader() });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || data.msg || `Failed to fetch from ${url}`);
  }
  return data;
};

const postData = async (url, body) => {
  const response = await fetch(url, {
    method: 'POST',
    headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || data.msg || `Failed to post to ${url}`);
  }
  return data;
};

const fetchAllData = async () => {
  try {
    const [statsData, companiesData, drivesData, studentsData] = await Promise.all([
      fetchData('/api/admin/stats'),
      fetchData('/api/admin/companies'),
      fetchData('/api/admin/drives'),
      fetchData('/api/admin/students'),
    ]);

    stats.value = [
        { label: 'Total Students', value: statsData.total_students, trend: 'Batch 2025', icon: 'bi-people' },
        { label: 'Active Companies', value: statsData.active_companies, trend: 'Approved partners', icon: 'bi-building' },
        { label: 'Active Drives', value: statsData.active_drives, trend: `${statsData.total_drives - statsData.active_drives} pending`, icon: 'bi-briefcase' },
        { label: 'Placement %', value: `${statsData.placements}%`, trend: 'Target: 90%', icon: 'bi-bar-chart-line' },
    ];
    allCompanies.value = companiesData.companies;
    allDrives.value = drivesData.drives;
    allStudents.value = studentsData.students;

  } catch (error) {
    console.error('Dashboard Error:', error);
    // Maybe redirect to login if auth fails
  }
};

const updateCompanyStatus = async (id, status) => {
  try {
    await postData(`/api/admin/company/${id}/status`, { status });
    await fetchAllData(); // Refresh
  } catch (error) {
    console.error('Error updating company status:', error);
  }
};

const updateDriveStatus = async (id, status) => {
  try {
    await postData(`/api/admin/drive/${id}/status`, { status });
    await fetchAllData();
  } catch (error) {
    console.error('Error updating drive status:', error);
  }
};

const toggleBlacklist = async (user) => {
  try {
    await postData(`/api/admin/user/${user.id}/blacklist`, {});
    await fetchAllData();
  } catch (error) {
    console.error('Error moderating user:', error);
  }
};

onMounted(fetchAllData);

</script>

<style scoped>
.admin-dashboard {
  background-color: #f8fafc; 
}

/* New Flexbox Layout */
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 2rem 2.5rem; /* Replicating container padding */
  max-width: 1200px;
  margin: 0 auto;
}

.metrics-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
}

.metric-card {
  flex: 1;
}

.tabs-row {
  display: flex;
  padding: 0.25rem;
  background-color: #f1f5f9; /* bg-light equivalent */
  border-radius: 0.375rem;
  width: fit-content;
}

.approvals-row {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.approval-panel {
  flex: 1;
}

.content-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Replicating gap-3 utility */
}


/* Base & Component Styles (Largely Unchanged) */
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

.btn-light.text-muted {
  color: #64748b !important;
  background-color: transparent;
  border: none;
}
.btn.bg-white.text-dark.shadow-sm {
  background-color: #fff;
  color: #212529;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}
</style>