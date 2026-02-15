<template>
  <div class="batch-jobs-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-9">
          <!-- Page Header -->
          <div class="text-center mb-5">
            <h1 class="fw-bold">Batch Processing Jobs</h1>
            <p class="text-muted">Trigger and monitor intensive background tasks for the platform.</p>
          </div>

          <!-- Job Status Section -->
          <div class="card shadow-sm mb-5" v-if="lastJob">
            <div class="card-body p-4 d-flex justify-content-between align-items-center">
               <div>
                  <h6 class="fw-semibold mb-1">Last Job Run</h6>
                  <p class="mb-0 text-muted"><strong>{{ lastJob.name }}</strong> - {{ new Date(lastJob.timestamp).toLocaleString() }}</p>
               </div>
               <div>
                   <span :class="['badge', getStatusClass(lastJob.status)]">
                       <i :class="['bi', getStatusIcon(lastJob.status), 'me-1']"></i>
                       {{ lastJob.status }}
                   </span>
               </div>
            </div>
          </div>

          <!-- Jobs List -->
          <div class="vstack gap-4">
            <!-- Job 1: Pre-Screening -->
            <div class="card shadow-sm">
              <div class="card-body p-4 d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                  <div class="icon-circle bg-primary-soft me-4">
                    <i class="bi bi-person-check-fill h4 text-primary"></i>
                  </div>
                  <div>
                    <h5 class="fw-semibold mb-1">Run Global Pre-Screening</h5>
                    <p class="text-muted mb-0">Scan all student profiles for policy violations and eligibility criteria.</p>
                  </div>
                </div>
                <button class="btn btn-primary" @click="triggerJob('screening')">
                  <i class="bi bi-play-fill me-1"></i> Trigger Job
                </button>
              </div>
            </div>

            <!-- Job 2: Export -->
            <div class="card shadow-sm">
              <div class="card-body p-4 d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                  <div class="icon-circle bg-success-soft me-4">
                     <i class="bi bi-file-earmark-spreadsheet-fill h4 text-success"></i>
                  </div>
                  <div>
                    <h5 class="fw-semibold mb-1">Export Application History</h5>
                    <p class="text-muted mb-0">Generate a CSV export of all applications for the current year.</p>
                  </div>
                </div>
                <button class="btn btn-primary" @click="triggerJob('export')">
                   <i class="bi bi-play-fill me-1"></i> Trigger Job
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const lastJob = ref(null);

const jobMap = {
  screening: "Global Pre-Screening",
  export: "Application History Export"
};

const triggerJob = (jobName) => {
  console.log(`Triggering ${jobMap[jobName]}`);
  lastJob.value = {
    name: jobMap[jobName],
    status: 'Running',
    timestamp: Date.now(),
  };

  // Simulate job completion
  setTimeout(() => {
    if (lastJob.value && lastJob.value.name === jobMap[jobName]) {
        lastJob.value.status = Math.random() > 0.2 ? 'Completed' : 'Failed';
    }
  }, 5000);
};

const getStatusClass = (status) => {
    const statusMap = {
        'Running': 'bg-warning-soft text-warning',
        'Completed': 'bg-success-soft text-success',
        'Failed': 'bg-danger-soft text-danger'
    };
    return statusMap[status];
};

const getStatusIcon = (status) => {
    const iconMap = {
        'Running': 'bi-arrow-repeat',
        'Completed': 'bi-check-circle-fill',
        'Failed': 'bi-x-circle-fill'
    };
    return iconMap[status];
};
</script>

<style scoped>
.batch-jobs-page {
  background-color: #f8fafc;
  min-height: 100vh;
}
.card {
    border: none;
}
.fw-semibold { font-weight: 600; }
.text-muted { color: #64748b !important; }

.icon-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.bg-primary-soft { background-color: #eef2ff; }
.bg-success-soft { background-color: #f0fdf4; }
.text-primary { color: #4f46e5 !important; }
.text-success { color: #16a34a !important; }

.badge {
  font-size: .8rem;
  padding: .5em .8em;
  font-weight: 600;
  letter-spacing: .5px;
}

.badge.bg-success-soft {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    color: #166534 !important;
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
</style>
