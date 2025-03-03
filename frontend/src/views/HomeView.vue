//HomeView.vue

<template>
  <div>
    <header>
      <h1>Optimus - Rule of Law Interactive System</h1>
    </header>

    <aside class="sidebar">
      <h3>Navigation</h3>
      <ul>
        <li><router-link :to="{ path: '/' }" :class="{ 'active-link': $route.path === '/' }">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
      </ul>
      <h3>Systems</h3>
      <ul>
        <li><router-link to="/judicial">Judicial System</router-link></li>
        <li><router-link to="/political">Political System</router-link></li>
        <li><router-link to="/norms">View Norms</router-link></li>
        <li><router-link to="/cases">View Cases</router-link></li>
      </ul>
      <h3>Analytics</h3>
      <ul>
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <main class="main-content">
      <h2>Welcome to Optimus</h2>

      <section class="usage-guide">
        <h3>How to Use This Platform</h3>
        <p>Optimus is an interactive system for analyzing the interaction between political and judicial systems.
        Use the navigation menu to explore different sections:</p>
        <ul>
          <li><strong>Political System:</strong> Create and manage legal norms.</li>
          <li><strong>Judicial System:</strong> Review cases and evaluate their constitutionality.</li>
          <li><strong>View Cases:</strong> Browse pending and resolved legal cases.</li>
          <li><strong>View Norms:</strong> Check existing norms and their status.</li>
          <li><strong>Statistics Dashboard:</strong> View real-time analytics on system performance.</li>
        </ul>
      </section>

      <section class="log-section">
        <h3>System Overview</h3>
        <div class="overview-grid">
          <div class="card overview-card">
            <i data-lucide="book" class="mb-4"></i>
            <h4>Political System</h4>
            <p>Create and manage norms through the political interface.</p>
            <router-link to="/political" class="action-button">Access Political System</router-link>
          </div>
          <div class="card overview-card">
            <i data-lucide="gavel" class="mb-4"></i>
            <h4>Judicial System</h4>
            <p>Review cases and evaluate norm constitutionality.</p>
            <router-link to="/judicial" class="action-button">Access Judicial System</router-link>
          </div>
        </div>
      </section>

      <section class="log-section">
        <h3>Recent Activity</h3>
        <div v-if="activities.length" class="card">
          <div v-for="activity in activities" :key="activity.id" class="log-entry">{{ activity.text }}</div>
        </div>
        <div v-else class="card">
          <p>No activities recorded today.</p>
        </div>
      </section>

      <section class="log-section">
        <h3>Quick Statistics</h3>
        <div class="stats-grid">
          <div class="card">
            <h4>Norms</h4>
            <br>
            <p>Total Norms: {{ normsStats.total }}</p>
            <p>Valid: {{ normsStats.valid }}</p>
            <p>Invalid: {{ normsStats.invalid }}</p>
          </div>
          <div class="card">
            <h4>Cases</h4>
            <br>
            <p>Total Cases: {{ casesStats.total }}</p>
            <p>Recently Resolved: {{ casesStats.recentlyResolvedCount }}</p>
          </div>
        </div>
      </section>
    </main>

    <footer>
      © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'OptimusApp',
  setup() {
    const activities = ref([])
    const normsStats = ref({ total: 0, valid: 0, invalid: 0 })
    const casesStats = ref({ total: 0, recentlyResolvedCount: 0 })
    let intervalId = null

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

    console.log("VITE_API_BASE_URL:", API_BASE_URL); // Debugging

    const fetchActivities = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/get_activities`);
        activities.value = await response.json();
      } catch (error) {
        console.error('Error fetching activities:', error);
      }
    };

    const fetchQuickStats = async () => {
      try {
        const [normsRes, casesRes, solvedCasesRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/get_norms`),
          fetch(`${API_BASE_URL}/api/get_all_cases`),
          fetch(`${API_BASE_URL}/api/get_solved_cases`)
        ]);

        const [norms, cases, solved] = await Promise.all([
          normsRes.json(),
          casesRes.json(),
          solvedCasesRes.json()
        ]);

        normsStats.value = {
          total: norms.length,
          valid: norms.filter(n => n.valid).length,
          invalid: norms.filter(n => !n.valid).length
        };

        casesStats.value = {
          total: cases.total,
          recentlyResolvedCount: solved.solved_cases.slice(-5).length
        };
      } catch (error) {
        console.error('Error fetching quick stats:', error);
      }
    };

    const updateData = () => {
      fetchActivities();
      fetchQuickStats();
    };

    onMounted(() => {
      updateData();
      intervalId = setInterval(updateData, 30000);
    });

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
    });

    return {
      activities,
      normsStats,
      casesStats
    };
  }
};
</script>

<style scoped>

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  :root {
    --primary: #2563eb;
    --sidebar-width: 280px;
    --header-height: 60px;
  }
  
  body {
    font-family: system-ui, -apple-system, sans-serif;
    background: #f9fafb;
  }
  
  header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    background: white;
    padding: 0 1.5rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #e5e7eb;
    z-index: 20;
  }
  
  .sidebar {
    width: var(--sidebar-width) !important;
    height: calc(100vh - var(--header-height)) !important;
  }
  
  .sidebar h3 {
    color: #6b7280;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 1.5rem 0 0.75rem;
  }
  
  .sidebar h3:first-child {
    margin-top: 0;
  }
  
  .sidebar ul {
    list-style: none;
    margin-bottom: 1rem;
  }
  
  .sidebar li {
    margin: 0.5rem 0;
  }
  
  .sidebar a {
    color: #374151;
    text-decoration: none;
    display: block;
    padding: 0.5rem;
    border-radius: 0.375rem;
    transition: all 0.2s;
  }
  
  .sidebar a:hover {
    background: #f3f4f6;
    color: var(--primary);
  }
  
  .submenu {
    margin-left: 1rem;
    font-size: 0.875rem;
    display: none;
  }
  
  .has-submenu:hover .submenu {
    display: block;
  }
  
  .main-content {
    margin-left: var(--sidebar-width) !important;
    width: calc(100vw - var(--sidebar-width)) !important;
    min-height: 100vh;
    margin-top: var(--header-height);
    padding: 2rem;
  }
  
  .overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
  }
  
  .card {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .overview-card {
    text-align: center;
  }
  
  .overview-card h4 {
    color: #111827;
    margin-bottom: 0.5rem;
  }
  
  .action-button {
    display: inline-block;
    background: var(--primary);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
    text-decoration: none;
    margin-top: 1rem;
    transition: opacity 0.2s;
  }
  
  .action-button:hover {
    opacity: 0.9;
  }
  
  .log-section {
    margin: 2rem 0;
  }
  
  .log-section h3 {
    color: #111827;
    margin-bottom: 1rem;
  }
  
  .log-entry {
    background: #f9fafb;
    padding: 1rem;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }
  
  .usage-guide {
    background: #f3f4f6;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin: 1.5rem 0;
  }
  
  .usage-guide ul {
    margin: 1rem 0;
    padding-left: 1.5rem;
  }
  
  .usage-guide li {
    margin: 0.5rem 0;
  }
  
  footer {
    margin-left: var(--sidebar-width);
    display: flex;
    justify-content: center;
    align-items: center;
    width: calc(100vw - var(--sidebar-width));
    padding: 1.5rem;
    text-align: center;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
  }
  
  @media (max-width: 1024px) {
    .sidebar {
        width: 200px; /* Adjusted width for smaller screens */
        position: fixed;
        min-height: 100vh;
    }

    .main-content {
        margin-left: 200px; /* Adjusted margin for new sidebar width */
    }

    footer {
        margin-left: 200px;
    }
  }
  </style>
  