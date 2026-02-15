<template>
  <div class="login-container">
    <div class="header">
      <img src="../assets/logo.svg" alt="CampusConnect Logo" class="logo">
      <h1>CampusConnect</h1>
      <p>The unified bridge between aspiring talent and industry leaders.</p>
    </div>

    <div class="card login-card">
      <h2>Portal Access</h2>
      <p class="subtitle">Select your role to continue</p>

      <div class="role-selector">
        <button
          :class="{ active: role === 'student' }"
          @click="role = 'student'"
        >
          Student
        </button>
        <button
          :class="{ active: role === 'company' }"
          @click="role = 'company'"
        >
          Company
        </button>
        <button
          :class="{ active: role === 'admin' }"
          @click="role = 'admin'"
        >
          Admin
        </button>
      </div>

      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">{{ role.charAt(0).toUpperCase() + role.slice(1) }} Email</label>
          <input type="email" id="email" v-model="email" placeholder="john@university.edu" class="form-control">
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary btn-block">{{ loginButtonText }}</button>
      </form>

      <div class="register-link">
        New student? <router-link to="/register">Self Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: 'student',
      email: '',
      password: '',
    };
  },
  computed: {
    loginButtonText() {
        return `Login as ${this.role.charAt(0).toUpperCase() + this.role.slice(1)}`;
    }
  },
  methods: {
    login() {
      // Handle login logic based on role
      console.log(`Logging in as ${this.role} with email ${this.email}`);
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--background-color);
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  height: 60px;
  width: 60px;
  margin-bottom: 1rem;
}

.header h1 {
    color: #000;
    font-weight: 700;
}

.login-card {
  max-width: 450px;
  width: 100%;
  padding: 2rem;
}

.subtitle {
    color: #6c757d;
    text-align: center;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
}

.role-selector {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
  background-color: #e9ecef;
  border-radius: 0.375rem;
  padding: 5px;
}

.role-selector button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-radius: 0.375rem;
  color: #6c757d;
  font-weight: 500;
}

.role-selector button.active {
  background-color: #fff;
  color: var(--primary-color);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.form-group label {
    font-weight: 500;
    margin-bottom: .5rem;
    display: block;
}

.btn-block {
    width: 100%;
    padding: 0.75rem;
    background-color: var(--primary-color);
}

.btn-block:hover {
    background-color: #2c3a8e;
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
}

.register-link a {
    font-weight: 500;
}
</style>
