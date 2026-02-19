<template>
  <div class="register-page">
    <div class="register-card">
      <h2 class="card-title">Create an Account</h2>

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

      <!-- Registration Form -->
      <form v-if="!registrationComplete" @submit.prevent="handleRegister">
        <!-- Common fields -->
        <div class="form-group">
          <label for="name">Full Name</label>
          <input type="text" id="name" v-model="form.name" required placeholder="Your Name">
        </div>
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" id="email" v-model="form.email" required placeholder="your.email@example.com">
        </div>

        <!-- Student-specific fields -->
        <template v-if="selectedRole === 'Student'">
          <div class="form-group">
            <label for="usn">USN (University Seat Number)</label>
            <input type="text" id="usn" v-model="form.usn" required placeholder="1AB23CD456">
          </div>
          <div class="form-group">
            <label for="department">Department</label>
            <input type="text" id="department" v-model="form.department" required placeholder="e.g., Computer Science">
          </div>
        </template>

        <!-- Company-specific fields -->
        <template v-if="selectedRole === 'Company'">
          <div class="form-group">
            <label for="company_name">Company Name</label>
            <input type="text" id="company_name" v-model="form.company_name" required placeholder="Your Company Inc.">
          </div>
        </template>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="form.password" required placeholder="Choose a strong password">
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" class="btn btn-primary btn-block">Register</button>
      </form>

      <!-- Completion Message -->
      <div v-else class="completion-view">
        <h3>Thank you for registering!</h3>
        <p v-if="selectedRole === 'Company'">Your company profile has been submitted and is now pending approval from the placement office.</p>
        <router-link to="/login" class="btn btn-secondary">Return to Login</router-link>
      </div>

      <div class="login-link">
        <p>Already have an account? <router-link to="/login">Sign In</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      roles: ["Student", "Company"],
      selectedRole: "Student",
      form: {
        name: "",
        email: "",
        password: "",
        usn: "",
        department: "",
        company_name: "",
      },
      error: null,
      registrationComplete: false,
    };
  },
  methods: {
    async handleRegister() {
      this.error = null;
      const payload = {
        role: this.selectedRole,
        name: this.form.name,
        email: this.form.email,
        password: this.form.password,
      };

      if (this.selectedRole === "Student") {
        payload.usn = this.form.usn;
        payload.department = this.form.department;
      } else if (this.selectedRole === "Company") {
        payload.company_name = this.form.company_name;
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "An error occurred during registration.");
        }

        if (this.selectedRole === "Student") {
          // Auto-login student upon successful registration
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("user", JSON.stringify(data.user));
          window.dispatchEvent(new Event("storage"));
          this.$router.push("/student/dashboard");
        } else {
          // Show completion message for company
          this.registrationComplete = true;
        }

      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>

<style scoped>
/* Using similar styling to Login page for consistency */
.register-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 4rem 2rem;
  background-color: #f8f9fa;
}

.register-card {
  max-width: 480px;
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

.form-group {
  margin-bottom: 1rem;
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
  margin-top: 1rem;
}

.btn-primary {
  background-color: #3F51B5;
  color: white;
}
.btn-primary:hover {
  background-color: #303f9f;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  display: inline-block;
}
.btn-secondary:hover {
  background-color: #5a6268;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.login-link a {
  color: #3F51B5;
  text-decoration: none;
  font-weight: 500;
}

.completion-view {
  text-align: center;
  padding: 2rem 0;
}

.completion-view h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.completion-view p {
  color: #6c757d;
  margin-bottom: 2rem;
}
</style>
