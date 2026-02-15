<template>
  <div class="company-dashboard-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-10">

          <!-- Header -->
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-5">
            <div>
              <h1 class="fw-bold">Company Dashboard</h1>
              <p class="text-muted">Welcome, Innovate Corp!</p>
            </div>
            <router-link to="/create-drive" class="btn btn-primary btn-lg">
                <i class="bi bi-plus-lg me-2"></i>Create Drive
            </router-link>
          </div>

          <!-- Active Drives -->
          <div>
            <h4 class="fw-semibold mb-4">Active Drives</h4>
            <div class="vstack gap-3">
              <!-- Drive 1 -->
              <div class="card shadow-sm">
                <div class="card-body p-4 d-flex justify-content-between align-items-center">
                  <div>
                    <h5 class="fw-bold mb-1">Software Development Engineer</h5>
                    <span class="badge bg-success-soft text-success">OPEN</span>
                  </div>
                  <div class="d-flex align-items-center gap-4">
                     <div class="text-center">
                         <div class="fs-4 fw-bold">25</div>
                         <div class="text-xs text-muted">Applicants</div>
                     </div>
                    <router-link to="/screening" class="btn btn-outline-primary">
                        View Applicants
                    </router-link>
                  </div>
                </div>
              </div>
              <!-- Drive 2 -->
              <div class="card shadow-sm">
                <div class="card-body p-4 d-flex justify-content-between align-items-center">
                  <div>
                    <h5 class="fw-bold mb-1">Product Manager Intern</h5>
                    <span class="badge bg-danger-soft text-danger">CLOSED</span>
                  </div>
                  <div class="d-flex align-items-center gap-4">
                     <div class="text-center">
                         <div class="fs-4 fw-bold">15</div>
                         <div class="text-xs text-muted">Applicants</div>
                     </div>
                    <router-link to="/screening" class="btn btn-outline-primary disabled">
                        View Applicants
                    </router-link>
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
// No script needed for this static example
</script>

<style scoped>
.company-dashboard-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.fw-semibold { font-weight: 600; }
.fw-bold { font-weight: 700; }
.text-muted { color: #64748b !important; }
.text-xs { font-size: 0.8rem; }

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
    font-weight: 600;
}

.badge.bg-danger-soft {
    background-color: #fef2f2 !important;
    border: 1px solid #fecaca;
    color: #991b1b !important;
    font-weight: 600;
}
</style>
