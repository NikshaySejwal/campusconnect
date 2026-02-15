<template>
  <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4>User Moderation</h4>
      <input type="search" v-model="searchQuery" placeholder="Search users..." class="form-control" style="width: 300px;" />
    </div>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td><span :class="['badge', getRoleClass(user.role)]">{{ user.role }}</span></td>
            <td>
              <button class="btn btn-sm btn-danger" @click="blacklistUser(user.id)">Blacklist</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      users: [
        { id: 1, name: 'John Doe', email: 'john.doe@university.edu', role: 'Student' },
        { id: 2, name: 'Innovate Corp', email: 'contact@innovate.com', role: 'Company' },
        { id: 3, name: 'Jane Smith', email: 'jane.smith@university.edu', role: 'Student' },
        { id: 4, name: 'Tech Solutions', email: 'hr@techsolutions.dev', role: 'Company' },
      ],
    };
  },
  computed: {
    filteredUsers() {
      if (!this.searchQuery) {
        return this.users;
      }
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.users.filter(user =>
        user.name.toLowerCase().includes(lowerCaseQuery) ||
        user.email.toLowerCase().includes(lowerCaseQuery)
      );
    },
  },
  methods: {
    blacklistUser(userId) {
      console.log(`Blacklisting user ${userId}`);
      // API call to /api/userblacklist endpoint would be made here
      this.users = this.users.filter(u => u.id !== userId);
    },
    getRoleClass(role) {
        return {
            'Student': 'bg-primary-light text-primary',
            'Company': 'bg-warning-light text-warning'
        }
    }
  },
};
</script>
<style scoped>
.card {
     border: none;
    box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
}
.card-header {
    background-color: #fff;
    padding: 1.5rem;
    border-bottom: 1px solid #dee2e6;
}
.table-hover tbody tr:hover {
    background-color: #f8f9fa;
}
.badge {
    padding: .4em .65em;
    font-size: .75em;
    font-weight: 500;
    border-radius: .25rem;
}
.bg-primary-light {
    background-color: #e7e9fd;
}
.text-primary {
    color: var(--primary-color) !important;
}
.bg-warning-light {
    background-color: #fff8e1;
}
.text-warning {
    color: #f59e0b !important;
}
.btn-danger {
    background-color: #fbe9e7;
    border-color: #fbe9e7;
    color: #d9534f;
}
</style>
