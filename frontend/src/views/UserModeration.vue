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
          <tr v-for="user in filteredUsers" :key="user.id" :class="{ 'blacklisted': user.blacklisted }">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td><span :class="['badge', getRoleClass(user.role)]">{{ user.role }}</span></td>
            <td>
              <button class="btn btn-sm action-btn" :class="user.blacklisted ? 'btn-outline-success' : 'btn-outline-danger'" @click="toggleBlacklist(user.id)">
                {{ user.blacklisted ? 'Unblacklist' : 'Blacklist' }}
              </button>
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
        { id: 1, name: 'John Doe', email: 'john.doe@university.edu', role: 'Student', blacklisted: false },
        { id: 2, name: 'Innovate Corp', email: 'contact@innovate.com', role: 'Company', blacklisted: false },
        { id: 3, name: 'Jane Smith', email: 'jane.smith@university.edu', role: 'Student', blacklisted: false },
        { id: 4, name: 'Tech Solutions', email: 'hr@techsolutions.dev', role: 'Company', blacklisted: false },
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
    toggleBlacklist(userId) {
      const user = this.users.find(u => u.id === userId);
      if (user) {
        user.blacklisted = !user.blacklisted;
      }
    },
    getRoleClass(role) {
        return {
            'Student': 'badge-student',
            'Company': 'badge-company'
        }
    }
  },
};
</script>
<style scoped>
.card {
    border: 1px solid #dee2e6;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    overflow: hidden;
}
.card-header {
    background-color: #fff;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #dee2e6;
}
.table {
    margin-bottom: 0;
}
.table-hover tbody tr:hover {
    background-color: #f8f9fa;
}
.badge {
    padding: .5em .75em;
    font-size: .8rem;
    font-weight: 600;
    border-radius: 8px;
}
.badge-student {
    background-color: #e8eaf6;
    color: #3f51b5;
}
.badge-company {
    background-color: #fff3e0;
    color: #ff9800;
}
.action-btn {
    padding: .35rem .7rem;
    font-size: .875rem;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
    min-width: 110px; /* Fix for table shifting */
    text-align: center;
}

.btn-outline-danger {
    border: 1px solid #d9534f;
    color: #d9534f;
}
.btn-outline-danger:hover {
    background-color: #d9534f;
    color: white;
}

.btn-outline-success {
    border: 1px solid #4caf50;
    color: #4caf50;
}
.btn-outline-success:hover {
    background-color: #4caf50;
    color: white;
}

.blacklisted td {
    text-decoration: line-through;
    color: #adb5bd;
}
.blacklisted .badge {
    opacity: 0.6;
}
</style>
