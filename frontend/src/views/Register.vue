<template>
  <div class="register-container">
    <div class="card register-card">
      <h2>Create Your Account</h2>
      <p class="subtitle">Join CampusConnect today!</p>

      <div v-if="!companyRegistrationPending">
        <div class="role-selector">
            <button :class="{ active: role === 'student' }" @click="role = 'student'">Student</button>
            <button :class="{ active: role === 'company' }" @click="role = 'company'">Company</button>
        </div>

        <form @submit.prevent="register">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" class="form-control" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" class="form-control" required>
            </div>

            <button type="submit" class="btn btn-primary btn-block">Register as {{ role.charAt(0).toUpperCase() + role.slice(1) }}</button>
        </form>

        <div class="login-link">
            Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </div>
      
      <div v-else class="pending-approval">
        <h3>Thank you for registering!</h3>
        <p>Your company profile is pending approval from the admin. You will be notified via email once your registration is confirmed.</p>
        <router-link to="/login" class="btn btn-primary">Back to Login</router-link>
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
      companyRegistrationPending: false,
    };
  },
  methods: {
    register() {
      if (this.role === 'company') {
        this.companyRegistrationPending = true;
        // API call to register company would happen here
        console.log(`Company registration for ${this.email} is pending.`);
      } else {
        // API call to register student
        console.log(`Registering student ${this.email}`);
        this.$router.push('/student-dashboard');
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--background-color);
}

.register-card {
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

.btn-block {
    width: 100%;
    padding: 0.75rem;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
}

.pending-approval {
    text-align: center;
}
</style>
