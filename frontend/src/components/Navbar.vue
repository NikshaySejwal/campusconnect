<template>
  <header class="main-header">
    <nav class="container">
      <router-link to="/" class="logo">Placement Portal</router-link>
      <div class="nav-links">
        <!-- Logged-out users -->
        <template v-if="!isLoggedIn">
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
        </template>
        
        <!-- Logged-in users -->
        <template v-else>
          <router-link v-if="userRole === 'Admin'" to="/admin/dashboard">Dashboard</router-link>
          <router-link v-if="userRole === 'Company'" to="/company/dashboard">Dashboard</router-link>
          <router-link v-if="userRole === 'Student'" to="/student/dashboard">Dashboard</router-link>
          <router-link v-if="userRole === 'Student'" to="/student/applications">My Applications</router-link>
          <a href="#" @click.prevent="logout">Logout</a>
        </template>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      isLoggedIn: false,
      userRole: null,
    };
  },
  created() {
    this.updateLoginState();
    window.addEventListener('storage', this.updateLoginState);
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.updateLoginState);
  },
  methods: {
    updateLoginState() {
      const token = localStorage.getItem("access_token");
      this.isLoggedIn = !!token;
      if (token) {
        try {
          const user = JSON.parse(localStorage.getItem("user"));
          this.userRole = user ? user.role : null;
        } catch (e) {
          this.userRole = null;
        }
      } else {
        this.userRole = null;
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      this.updateLoginState();
      this.$router.push("/login");
    },
  },
  watch: {
    '$route'() {
      this.updateLoginState();
    }
  }
};
</script>

<style scoped>
.main-header {
  background: white;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}
nav.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
.logo {
  font-weight: 700;
  font-size: 1.5rem;
  color: #3F51B5;
  text-decoration: none;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  font-weight: 500;
}
.nav-links a {
  text-decoration: none;
  color: #212529;
  transition: color 0.3s ease;
}
.nav-links a:hover, .nav-links a.router-link-exact-active {
  color: #3F51B5;
}
</style>
