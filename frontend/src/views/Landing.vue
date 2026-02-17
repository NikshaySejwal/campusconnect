<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#portal">Portal Access</a>
          <button class="cta-button-main">Get Started</button>
        </div>
      </nav>
    </header>

    <main>
      <section class="hero-section container">
        <div class="hero-left">
          <span class="trust-badge">&#9733; Trusted by 500+ Institutions</span>
          <h1 class="hero-title">Empowering the Next Generation of Talent</h1>
          <p class="hero-subtitle">CampusConnect is the ultimate bridge between academic excellence and corporate opportunity. Streamlined, secure, and AI-driven.</p>
          <div class="hero-buttons">
            <button class="access-portal-btn">Access Portal &#8594;</button>
            <button class="watch-demo-btn">Watch Demo</button>
          </div>
        </div>
        <div class="hero-right">
          <div class="signin-card">
            <div class="signin-header">
              <h2 class="signin-title">Sign In to Dashboard</h2>
              <p class="signin-subtitle">Select your role to access features</p>
            </div>
            <div class="signin-tabs">
              <button v-for="tab in ['Student', 'Company', 'Admin']" :key="tab" :class="['tab', { active: activeTab === tab }]" @click="activeTab = tab">
                {{ tab }}
              </button>
            </div>
            <div class="signin-content">
              <form @submit.prevent="">
                <label for="email">University Email</label>
                <input type="email" id="email" placeholder="student@university.edu" class="signin-input">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="" class="signin-input">
                <button class="signin-button">{{ activeTab }} Login</button>
              </form>
              <div class="register-link">
                Don't have an account? <a href="#">Register Now</a>
              </div>
            </div>
            <div class="card-footer">
                <span>&#128272; ENTERPRISE GRADE SECURITY</span>
                <span>SYSTEM V-2.1.0</span>
            </div>
          </div>
        </div>
      </section>

      <section id="features" class="features-section">
        <div class="container">
            <div class="features-header">
              <h2>One Platform, Three Ecosystems</h2>
              <p>We've engineered dedicated experiences for every participant in the recruitment cycle.</p>
            </div>
            <div class="features-grid">
              <div class="feature-card institutes-card">
                  <div class="feature-icon">&#127979;</div>
                  <h3 class="feature-title">For Institutes</h3>
                  <p class="feature-description">Centralized control over company approvals, drive moderation, and comprehensive student data management.</p>
                  <ul class="feature-list">
                      <li>&#9989; Blanket Moderation</li>
                      <li>&#9989; Automated Reports</li>
                      <li>&#9989; Robust AI Screening</li>
                  </ul>
              </div>
              <div class="feature-card companies-card">
                  <div class="feature-icon">&#127970;</div>
                  <h3 class="feature-title">For Companies</h3>
                  <p class="feature-description">Seamlessly announce placement drives, track applications, and update selection results in real-time.</p>
                  <ul class="feature-list">
                      <li>&#9989; AI Job Descriptions</li>
                      <li>&#9989; Easy Shortlisting</li>
                      <li>&#9989; Interview Tracking</li>
                  </ul>
              </div>
              <div class="feature-card students-card">
                  <div class="feature-icon">&#127891;</div>
                  <h3 class="feature-title">For Students</h3>
                  <p class="feature-description">One-click applications to top companies and real-time tracking of placement status and history.</p>
                  <ul class="feature-list">
                      <li>&#9989; Real-time Status</li>
                      <li>&#9989; Drive Notifications</li>
                      <li>&#9989; Academic Profiling</li>
                  </ul>
              </div>
            </div>
        </div>
      </section>
    </main>

    <footer class="main-footer">
        <div class="container footer-content">
            <div class="footer-logo">&#127891; CampusConnect</div>
            <div class="footer-links">
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
                <a href="#">Support</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 CampusConnect | Built for Institutes of Excellence.</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeTab = ref('Student');
</script>

<style scoped>
/* Global Styles & Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --primary-blue: #3F51B5;
  --accent-orange: #FF9800;
  --neutral-dark: #2c3e50;
  --background-light: #f8f9fa;
  --text-primary: #212529;
  --text-secondary: #6c757d;
  --border-color: #dee2e6;
  --card-radius: 16px;
  --button-radius: 8px;
}

.page-wrapper {
  font-family: 'Inter', sans-serif;
  background-color: white;
  color: var(--text-primary);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.main-header {
  background: white;
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 10;
  background: white; 
}

nav.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--primary-blue);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  font-weight: 500;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-primary);
}

.cta-button-main {
  background-color: var(--primary-blue);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: var(--button-radius);
  cursor: pointer;
  font-weight: 500;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  align-items: center;
  gap: 4rem;
  padding: 5rem 24px;
}

.trust-badge {
  display: inline-block;
  background-color: #e8eaf6;
  color: var(--primary-blue);
  padding: 8px 16px;
  border-radius: 99px;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 550px;
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
}

.access-portal-btn {
  background-color: var(--primary-blue);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: var(--button-radius);
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

.watch-demo-btn {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  padding: 14px 28px;
  border-radius: var(--button-radius);
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

/* Sign-In Card */
.signin-card {
  background: white;
  border-radius: var(--card-radius);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07);
  border: 1px solid var(--border-color);
}

.signin-header {
  padding: 1.5rem;
  text-align: center;
}

.signin-title { font-size: 1.5rem; font-weight: 700; }
.signin-subtitle { color: var(--text-secondary); margin-top: 0.5rem; }

.signin-tabs {
  display: flex;
  padding: 0 1.5rem;
}

.tab {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: transparent;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab.active {
  color: var(--primary-blue);
  border-bottom-color: var(--primary-blue);
}

.signin-content {
  padding: 1.5rem;
}

.signin-content label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    font-size: 0.9rem;
}

.signin-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--button-radius);
  background-color: #f8f9fa;
}

.signin-button {
  background-color: var(--primary-blue);
  color: white;
  border: none;
  width: 100%;
  padding: 14px;
  border-radius: var(--button-radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
}

.register-link {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
}
.register-link a { color: var(--primary-blue); text-decoration: none; }

.card-footer {
    display: flex;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background-color: #f8f9fa;
    border-top: 1px solid var(--border-color);
    font-size: 0.75rem;
    color: var(--text-secondary);
    border-bottom-left-radius: var(--card-radius);
    border-bottom-right-radius: var(--card-radius);
}

/* Features Section */
.features-section {
  background-color: var(--background-light);
  padding: 6rem 0;
  text-align: center;
}

.features-header h2 { font-size: 2.5rem; font-weight: 700; }
.features-header p { color: var(--text-secondary); max-width: 500px; margin: 1rem auto 0; }

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
  text-align: left;
}

.feature-card {
  background: white;
  padding: 2rem;
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  border-top-width: 4px;
}

.feature-icon {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.feature-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem; }
.feature-description { color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1rem; }

.feature-list {
    list-style: none;
    padding: 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
}
.feature-list li {
    margin-bottom: 0.5rem;
}

.institutes-card { border-top-color: var(--primary-blue); }
.companies-card { border-top-color: var(--accent-orange); }
.students-card { border-top-color: var(--neutral-dark); }

/* Footer */
.main-footer {
    background-color: #212529;
    color: #f8f9fa;
    padding-top: 3rem;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid #495057;
}

.footer-logo { font-size: 1.25rem; font-weight: 600; }
.footer-links { display: flex; gap: 1.5rem; }
.footer-links a { color: #f8f9fa; text-decoration: none; }

.footer-bottom {
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.9rem;
    color: #adb5bd;
}
</style>
