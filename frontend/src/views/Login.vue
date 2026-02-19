<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="card-title">Portal Login</h2>
      
      <!-- Role Selector -->
      <div class="role-selector">
        <button 
          v-for="roleName in roles"
          :key="roleName"
          :class="{ active: selectedRole === roleName }"
          @click="selectedRole = roleName">
          {{ roleName }}
        </button>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="your.email@example.com">
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="••••••••">
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn btn-primary btn-block">Login</button>
      </form>

      <div class="register-link">
        <p v-if="selectedRole === 'Student'">
          Don't have an account? <router-link to="/register">Register as Student</router-link>
        </p>
        <p v-else>
          Company or Admin accounts are created by the placement office.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      roles: ["Student", "Company", "Admin"],
      selectedRole: "Student",
      email: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;
      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.selectedRole,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "An error occurred.");
        }

        // Store token and user data
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        
        // Manually trigger storage event for navbar update
        window.dispatchEvent(new Event("storage"));

        // Redirect to the appropriate dashboard
        switch (data.user.role) {
          case "Admin":
            this.$router.push("/admin/dashboard");
            break;
          case "Company":
            this.$router.push("/company/dashboard");
            break;
          case "Student":
            this.$router.push("/student/dashboard");
            break;
          default:
            this.$router.push("/");
        }

      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 4rem 2rem;
  background-color: #f8f9fa;
}

.login-card {
  max-width: 420px;
  width: 100%;
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.card-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

/* Role Selector */
.role-selector {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
  background-color: #e9ecef;
  border-radius: 8px;
  padding: 5px;
}

.role-selector button {
  flex: 1;
  padding: 0.75rem 0.5rem;
  border: none;
  background: transparent;
  color: #6c757d;
  font-weight: 500;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease-in-out;
}

.role-selector button.active {
  background-color: #ffffff;
  color: #3F51B5;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Form */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 1rem;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  text-align: center;
}

.btn-block {
  width: 100%;
  padding: 0.85rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #3F51B5;
  color: white;
}
.btn-primary:hover {
  background-color: #303f9f;
}

/* Register Link */
.register-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.register-link a {
  color: #3F51B5;
  text-decoration: none;
  font-weight: 500;
}
.register-link a:hover {
  text-decoration: underline;
}
</style>
