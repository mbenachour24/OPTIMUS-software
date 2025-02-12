<template>
    <div class="container mx-auto p-6">
      <h1 class="text-3xl font-bold">General Log</h1>
      <ul>
        <li v-for="entry in logEntries" :key="entry.timestamp">
          {{ entry.message }} ({{ entry.timestamp }})
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: "GeneralLogView",
    data() {
      return { logEntries: [] };
    },
    async created() {
      const response = await fetch("/api/get_activities");
      this.logEntries = await response.json();
    }
  };
  </script>
  