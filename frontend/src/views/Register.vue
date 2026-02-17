<template>
  <div class="page-wrapper">
    <header class="main-header">
      <nav class="container">
        <div class="logo">CampusConnect</div>
        <div class="nav-links">
          <a href="/">Home</a>
          <a href="/login">Login</a>
        </div>
      </nav>
    </header>

    <main class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-6">
          <div class="register-card">
            <div v-if="!companyRegistrationPending">
              <div class="card-header">
                <h2 class="card-title">Create Your Account</h2>
                <p class="card-subtitle">Join CampusConnect to unlock your future.</p>
              </div>

              <div class="card-body">
                <div class="role-selector">
                  <button :class="{ active: role === 'student' }" @click="role = 'student'">Student</button>
                  <button :class="{ active: role === 'company' }" @click="role = 'company'">Company</button>
                </div>

                <form @submit.prevent="register">
                  <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" v-model="email" class="form-control" required placeholder="your.email@university.edu">
                  </div>
                  <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" class="form-control" required placeholder="Create a strong password">
                  </div>
                  <button type="submit" class="submit-btn">Register as {{ role.charAt(0).toUpperCase() + role.slice(1) }}</button>
                </form>
              </div>

              <div class="card-footer">
                Already have an account? <router-link to="/login">Sign In</router-link>
              </div>
            </div>

            <div v-else class="pending-approval">
              <div class="card-body text-center">
                <div class="approval-icon">&#128337;</div>
                <h3 class="approval-title">Thank You for Registering!</h3>
                <p class="approval-text">Your company profile is pending approval from the admin. You will be notified via email once your registration is confirmed.</p>
                <router-link to="/login" class="btn btn-primary">Back to Login</router-link>
              </div>
            </div>

          </div>
        </div>
      </div>
    </main>
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
        console.log(`Company registration for ${this.email} is pending.`);
      } else {
        console.log(`Registering student ${this.email}`);
        this.$router.push('/student-dashboard');
      }
    },
  },
};
</script>

<style scoped>
.page-wrapper { background-color: #f8f9fa; min-height: 100vh; }
.container { max-width: 960px; }

/* Consistent Header */
.main-header { background: white; border-bottom: 1px solid #dee2e6; padding: 1rem 0; }
nav.container { display: flex; justify-content: space-between; align-items: center; }
.logo { font-weight: 700; font-size: 1.5rem; color: #3F51B5; }
.nav-links { display: flex; align-items: center; gap: 1.5rem; font-weight: 500; }
.nav-links a { text-decoration: none; color: #212529; }

/* Registration Card */
.register-card {
  background-color: white;
  border-radius: 16px;
  border: 1px solid #dee2e6;
  box-shadow: 0 8px 24px rgba(0,0,0,0.07);
  overflow: hidden;
}

.card-header, .card-body, .card-footer {
  padding: 1.75rem;
}

.card-header {
  text-align: center;
  border-bottom: 1px solid #e9ecef;
}
.card-title { font-size: 1.75rem; font-weight: 700; color: #2c3e50; }
.card-subtitle { font-size: 1rem; color: #6c757d; margin-top: 0.25rem; }

.role-selector {
  display: flex;
  background-color: #f1f3f5;
  border-radius: 8px;
  padding: 5px;
  margin-bottom: 2rem;
}
.role-selector button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 6px;
  color: #6c757d;
  font-weight: 600;
}
.role-selector button.active {
  background-color: #fff;
  color: #3F51B5;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.form-group { margin-bottom: 1.5rem; }
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #343a40;
}
.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #f8f9fa;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background-color: #3F51B5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.card-footer {
  background-color: #f8f9fa;
  text-align: center;
  border-top: 1px solid #e9ecef;
  color: #6c757d;
}
.card-footer a { color: #3F51B5; text-decoration: none; font-weight: 600; }

/* Pending Approval State */
.approval-icon { font-size: 3rem; color: #3F51B5; margin-bottom: 1rem; }
.approval-title { font-size: 1.5rem; font-weight: 600; }
.approval-text { color: #6c757d; margin-bottom: 2rem; }
.btn-primary { background-color: #3F51B5; border: none; padding: 12px 24px; border-radius: 8px; }
</style>
