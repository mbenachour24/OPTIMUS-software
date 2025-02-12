<template>
    <div>
      <header>
        <h1>Optimus - Rule of Law Interactive System</h1>
      </header>
  
      <aside class="sidebar">
        <h3>Navigation</h3>
        <ul>
          <li><a href="/" class="active-link">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
        <h3>Systems</h3>
        <ul>
          <li><a href="/judicial">Judicial System</a></li>
          <li><a href="/political">Political System</a></li>
          <li><a href="/norms">View Norms</a></li>
          <li><a href="/cases">View Cases</a></li>
        </ul>
        <h3>Analytics</h3>
        <ul>
          <li class="has-submenu">
            <a href="/general_log">General Log</a>
            <ul class="submenu">
              <li><a href="/general_log#todays-activities">Today's Activities</a></li>
              <li><a href="/general_log#norm-updates">Norm Updates</a></li>
              <li><a href="/general_log#case-decisions">Case Decisions</a></li>
            </ul>
          </li>
          <li><a href="/statistics">Statistics Dashboard</a></li>
        </ul>
      </aside>
  
      <main class="main-content">
        <h2>Welcome to Optimus</h2>
  
        <div class="usage-guide">
          <h3>How to Use This Platform</h3>
          <p>Optimus is an interactive system for analyzing the interaction between political and judicial systems.
          Use the navigation menu to explore different sections:</p>
          <ul>
            <li><strong>Political System:</strong> Create and manage legal norms.</li>
            <li><strong>Judicial System:</strong> Review cases and evaluate their constitutionality.</li>
            <li><strong>View Cases:</strong> Browse pending and resolved legal cases.</li>
            <li><strong>View Norms:</strong> Check existing norms and their status.</li>
            <li><strong>General Log:</strong> Track system activities and key events.</li>
            <li><strong>Statistics Dashboard:</strong> View real-time analytics on system performance.</li>
          </ul>
        </div>
  
        <div class="log-section">
          <h3>System Overview</h3>
          <div class="overview-grid">
            <div class="card overview-card">
              <i data-lucide="book" class="mb-4"></i>
              <h4>Political System</h4>
              <p>Create and manage norms through the political interface.</p>
              <a href="/political" class="action-button">Access Political System</a>
            </div>
            <div class="card overview-card">
              <i data-lucide="gavel" class="mb-4"></i>
              <h4>Judicial System</h4>
              <p>Review cases and evaluate norm constitutionality.</p>
              <a href="/judicial" class="action-button">Access Judicial System</a>
            </div>
          </div>
        </div>
  
        <div class="log-section">
          <h3>Recent Activity</h3>
          <div id="activities-log" class="card">
            <!-- Activities will be loaded here -->
          </div>
        </div>
  
        <div class="log-section">
          <h3>Quick Statistics</h3>
          <div class="stats-grid">
            <div class="card">
              <h4>Norms</h4>
              <div id="norm-stats">Loading...</div>
            </div>
            <div class="card">
              <h4>Cases</h4>
              <div id="case-stats">Loading...</div>
            </div>
          </div>
        </div>
      </main>
  
      <footer>
        © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'OptimusApp',
    mounted() {
      this.updateData();
      setInterval(this.updateData, 30000);
    },
    methods: {
      async fetchActivities() {
        try {
          const response = await fetch('/api/get_activities');
          const activities = await response.json();
          const activitiesLog = document.getElementById('activities-log');
          activitiesLog.innerHTML = activities.length
            ? activities.map(activity => `<div class="log-entry">${activity}</div>`).join('')
            : '<p>No activities recorded today.</p>';
        } catch (error) {
          console.error('Error fetching activities:', error);
        }
      },
      async fetchQuickStats() {
        try {
          const [normsRes, casesRes, solvedCasesRes] = await Promise.all([
            fetch('/api/get_norms'),
            fetch('/api/get_all_cases'),
            fetch('/api/get_solved_cases')
          ]);
  
          const [norms, cases, solved] = await Promise.all([
            normsRes.json(),
            casesRes.json(),
            solvedCasesRes.json()
          ]);
  
          document.getElementById('norm-stats').innerHTML = `
            <p>Total Norms: ${norms.length}</p>
            <p>Valid: ${norms.filter(n => n.valid).length}</p>
            <p>Invalid: ${norms.filter(n => !n.valid).length}</p>
          `;
  
          document.getElementById('case-stats').innerHTML = `
            <p>Total Cases: ${cases.total}</p>
            <p>Recently Resolved: ${solved.solved_cases.slice(-5).length}</p>
          `;
        } catch (error) {
          console.error('Error fetching quick stats:', error);
        }
      },
      updateData() {
        this.fetchActivities();
        this.fetchQuickStats();
      }
    }
  };
  </script>
  
  <style>
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
    position: fixed;
    top: var(--header-height);
    left: 0;
    width: var(--sidebar-width);
    height: calc(100vh - var(--header-height));
    background: white;
    border-right: 1px solid #e5e7eb;
    padding: 1.5rem;
    overflow-y: auto;
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
    margin-left: var(--sidebar-width);
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
    padding: 1.5rem;
    text-align: center;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
  }
  
  @media (max-width: 1024px) {
    .sidebar {
      transform: translateX(-100%);
      transition: transform 0.3s;
    }
  
    .sidebar.active {
      transform: translateX(0);
    }
  
    .main-content, footer {
      margin-left: 0;
    }
  }
  </style>
  