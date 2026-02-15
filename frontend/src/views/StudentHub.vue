<template>
  <div>
    <h1>Student Hub</h1>
    <div v-for="drive in approvedDrives" :key="drive.id">
      <h2>{{ drive.title }}</h2>
      <p>{{ drive.company.name }}</p>
      <button @click="apply(drive.id)">Apply</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      approvedDrives: [],
    };
  },
  methods: {
    apply(driveId) {
      // Send POST request to /api/apply with driveId
    },
  },
  created() {
    // Fetch approved drives from the backend
  },
};
</script>