<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Placement Portal</h1>
        <p class="hero-subtitle">Connecting students and companies for a seamless recruitment experience.</p>
        <div class="hero-actions">
          <router-link to="/register" class="btn btn-primary">Get Started</router-link>
          <router-link to="/login" class="btn btn-secondary">Access Portal</router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <h2 class="section-title">One Platform, Three Roles</h2>
        <p class="section-subtitle">Dedicated experiences for every participant in the recruitment cycle.</p>
        <div class="features-grid">
          <!-- For Institutes -->
          <div class="feature-card">
            <div class="feature-icon">&#127979;</div>
            <h3 class="feature-title">For Institutes</h3>
            <p class="feature-description">Centralized control over company approvals, drive moderation, and comprehensive student data management.</p>
          </div>
          <!-- For Companies -->
          <div class="feature-card">
            <div class="feature-icon">&#127970;</div>
            <h3 class="feature-title">For Companies</h3>
            <p class="feature-description">Seamlessly announce placement drives, track applications, and update selection results in real-time.</p>
          </div>
          <!-- For Students -->
          <div class="feature-card">
            <div class="feature-icon">&#127891;</div>
            <h3 class="feature-title">For Students</h3>
            <p class="feature-description">One-click applications to top companies and real-time tracking of placement status and history.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "Landing",
};
</script>

<style scoped>
.landing-page {
  width: 100%;
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 6rem 2rem;
  background-color: #ffffff;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions .btn {
  margin: 0 0.5rem;
  padding: 12px 24px;
  font-size: 1rem;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #3F51B5;
  color: white;
}

.btn-primary:hover {
  background-color: #303f9f;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

/* Features Section */
.features-section {
  padding: 4rem 2rem;
  background-color: #f8f9fa;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  font-size: 1.1rem;
  color: #6c757d;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  text-align: center;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.feature-description {
  color: #6c757d;
}
</style>
