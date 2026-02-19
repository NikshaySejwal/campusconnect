<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <a href="/student-dashboard">Dashboard</a>
          <a href="/applications">My Applications</a>
          <a href="/profile/1">My Profile</a>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <!-- Header -->
      <div class="page-header-container">
        <div>
          <h1 class="welcome-title">Welcome, John!</h1>
          <p class="welcome-subtitle">Explore and apply to the latest placement drives from top companies.</p>
        </div>
        <div class="header-buttons">
          <router-link to="/profile/1" class="header-btn">My Profile</router-link>
          <router-link to="/applications" class="header-btn">My Applications</router-link>
        </div>
      </div>

      <!-- Available Drives -->
      <div class="drives-section">
        <h4 class="section-title">Available Drives</h4>
        <div class="drives-grid">
          <div v-for="drive in availableDrives" :key="drive.id" class="drive-card">
            <div class="card-content">
              <div class="company-logo-wrapper">
                <img :src="drive.companyLogo" :alt="drive.company" class="company-logo">
              </div>
              <div class="drive-details">
                <h5 class="job-title">{{ drive.jobTitle }}</h5>
                <p class="company-name">{{ drive.company }}</p>
                <div class="drive-meta">
                  <span>&#128176; {{ drive.salary }}</span>
                  <span>&#128197; Deadline: {{ drive.deadline }}</span>
                </div>
              </div>
              <router-link :to="`/drive/${drive.id}`" class="apply-btn">View Details</router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const availableDrives = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:5000/drives');
    const data = await response.json();
    availableDrives.value = data.drives.map(drive => ({
      id: drive.id,
      jobTitle: drive.title,
      company: drive.company,
      companyLogo: `https://logo.clearbit.com/${drive.company.toLowerCase().replace(/\s/g, '')}.com`,
      salary: 'Not Disclosed', // Backend does not provide this yet
      deadline: new Date(drive.deadline).toLocaleDateString(),
    }));
  } catch (error) {
    console.error('Failed to fetch drives:', error);
  }
});
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.container { max-width: 1200px; }

/* Header */
.main-header { background: white; border-bottom: 1px solid #dee2e6; padding: 1rem 0; }
nav.container { display: flex; justify-content: space-between; align-items: center; }
.logo { font-weight: 700; font-size: 1.5rem; color: #3F51B5; }
.nav-links { display: flex; align-items: center; gap: 1.5rem; font-weight: 500; }
.nav-links a { text-decoration: none; color: #212529; }

/* Page Header */
.page-header-container {
  display: flex; justify-content: space-between; align-items: center; 
  margin-bottom: 3rem;
}
.welcome-title { font-size: 2.25rem; font-weight: 700; color: #2c3e50; }
.welcome-subtitle { font-size: 1.1rem; color: #6c757d; }
.header-buttons { display: flex; gap: 1rem; }
.header-btn {
  background-color: white;
  border: 1px solid #dee2e6;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  color: #343a40;
  font-weight: 600;
}

/* Drives Section */
.drives-section { margin-top: 2rem; }
.section-title { font-size: 1.75rem; font-weight: 600; margin-bottom: 1.5rem; }
.drives-grid { display: flex; flex-direction: column; gap: 1rem; }

.drive-card {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  transition: all 0.2s ease;
}
.drive-card:hover { transform: translateY(-3px); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }

.card-content { display: flex; align-items: center; padding: 1.5rem; }
.company-logo-wrapper { flex-shrink: 0; width: 60px; height: 60px; display: grid; place-items: center; margin-right: 1.5rem; }
.company-logo { max-width: 100%; max-height: 100%; object-fit: contain; }

.drive-details { flex-grow: 1; }
.job-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 0.25rem; }
.company-name { color: #6c757d; font-weight: 500; margin-bottom: 0.75rem; }
.drive-meta { display: flex; gap: 1.5rem; font-size: 0.9rem; color: #495057; }

.apply-btn {
  background-color: #3F51B5;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  margin-left: 1.5rem;
  text-decoration: none;
  text-align: center;
}
</style>
