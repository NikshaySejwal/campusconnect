<template>
  <nav class="navbar">
    <router-link to="/" class="brand">CampusConnect</router-link>
    <div class="nav-links">
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
      <router-link to="/student-dashboard">Student Dashboard</router-link>
      <router-link to="/admin-dashboard">Admin Dashboard</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.brand {
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: none;
  color: #333;
}
.nav-links {
  display: flex;
  gap: 1.5rem;
}
.nav-links a {
  text-decoration: none;
  color: #555;
  font-weight: 500;
}
.nav-links a:hover {
  color: #007bff;
}
</style>
