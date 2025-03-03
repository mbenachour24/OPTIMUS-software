<template>
  <div>
    <header>
      <h1>Optimus - Case Management</h1>
    </header>

    <aside class="sidebar">
      <h3>Navigation</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
      <h3>Systems</h3>
      <ul>
        <li><a href="/judicial">Judicial System</a></li>
        <li><a href="/political">Political System</a></li>
        <li><a href="/norms">View Norms</a></li>
        <li><a href="/cases" class="active-link">View Cases</a></li>
      </ul>
      <h3>Analytics</h3>
      <ul>
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <main class="main-content">
      <h2>Case Management</h2>

      <!-- Case Filters -->
      <div class="filters">
        <button @click="fetchCases('all')" id="filter-all" class="active">All</button>
        <button @click="fetchCases('pending')" id="filter-pending">Pending</button>
        <button @click="fetchCases('solved')" id="filter-solved">Solved</button>
      </div>

      <!-- Cases Table -->
      <div class="table-container">
        <table class="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Text</th>
              <th>Norm ID</th>
              <th>Created At</th>
              <th>Status</th>
              <th>Resolved At</th>
            </tr>
          </thead>
          <tbody id="cases-list">
            <!-- Cases will be dynamically loaded here -->
          </tbody>
        </table>
      </div>
    </main>

    <footer>
      © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
    </footer>
  </div>
</template>
<script>
import { API_BASE_URL } from '../config.js';

export default {
  name: 'ViewCases',
  mounted() {
    this.fetchCases('all'); // Fetch all cases by default
  },
  methods: {
    async fetchCases(filter = "all") {
      let apiUrl;

      // Determine the API URL based on the filter
      if (filter === "pending") {
        apiUrl = `${API_BASE_URL}/api/get_pending_cases`;
      } else if (filter === "solved") {
        apiUrl = `${API_BASE_URL}/api/get_solved_cases`;
      } else {
        apiUrl = `${API_BASE_URL}/api/get_all_cases`;
      }

      try {
        console.log(`Fetching cases from: ${apiUrl}`);
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`Failed to fetch cases: ${response.status}`);
        }

        const data = await response.json();
        const casesList = document.getElementById('cases-list');
        const tableHeader = document.querySelector('.styled-table thead tr');

        if (!casesList || !tableHeader) {
          console.error('Error: Table elements not found in the DOM.');
          return;
        }

        // Clear the table content
        casesList.innerHTML = '';

        // Dynamically adjust the table header based on the filter
        if (filter === "all") {
          tableHeader.innerHTML = `
            <th>ID</th>
            <th>Text</th>
            <th>Norm ID</th>
            <th>Created At</th>
            <th>Status</th>
            <th>Decision</th>
            <th>Resolved At</th>
          `;
        } else {
          tableHeader.innerHTML = `
            <th>ID</th>
            <th>Text</th>
            <th>Norm ID</th>
            <th>Created At</th>
            <th>Decision</th>
            <th>Resolved At</th>
          `;
        }

        // Select cases based on the filter
        const cases = filter === "pending"
          ? data.pending_cases
          : (filter === "solved" ? data.solved_cases : data.cases || []);

        if (!cases || cases.length === 0) {
          casesList.innerHTML = '<tr><td colspan="6">No cases found.</td></tr>';
          return;
        }

        cases.sort((a, b) => b.id - a.id);

        // Fill the table with cases
        cases.forEach(caseItem => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${caseItem.id || 'N/A'}</td>
            <td>${caseItem.text || 'N/A'}</td>
            <td>${caseItem.norm_id || 'N/A'}</td>
            <td>${caseItem.created_at ? new Date(caseItem.created_at).toLocaleString() : 'N/A'}</td>
            ${
              filter === "all"
                ? `<td>${caseItem.status || 'N/A'}</td><td>${caseItem.decision || 'N/A'}</td><td>${caseItem.resolved_at || 'Pending'}</td>`
                : `<td>${caseItem.decision || 'Pending'}</td><td>${caseItem.resolved_at || 'Pending'}</td>`
            }
          `;
          casesList.appendChild(row);
        });

        // Highlight the selected filter
        document.querySelectorAll('.filters button').forEach(btn => btn.classList.remove('active'));
        const activeFilter = document.getElementById(`filter-${filter}`);
        if (activeFilter) activeFilter.classList.add('active');

      } catch (error) {
        console.error('Error fetching cases:', error);
      }
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
  --secondary: #6b7280;
  --text-color: #374151;
  --bg-light: #f9fafb;
  --bg-white: #ffffff;
  --border-color: #e5e7eb;
  --sidebar-width: 280px;
  --header-height: 60px;
  --transition-speed: 0.2s;
  --shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  --border-radius: 8px;
  --font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

body {
  font-family: var(--font-family);
  background: var(--bg-light);
  color: var(--text-color);
}

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: var(--bg-white);
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  z-index: 20;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sidebar {
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: var(--sidebar-width);
  height: calc(100vh - var(--header-height));
  background: var(--bg-white);
  border-right: 1px solid var(--border-color);
  padding: 1.5rem;
  overflow-y: auto;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.05);
}

.sidebar h3 {
  color: var(--secondary);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.75rem;
}

.sidebar ul {
  list-style: none;
  margin-bottom: 1rem;
}

.sidebar a {
  color: var(--text-color);
  text-decoration: none;
  display: block;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed), color var(--transition-speed);
}

.sidebar a:hover {
  background: #f3f4f6;
  color: var(--primary);
}

.main-content {
  margin-left: var(--sidebar-width);
  margin-top: var(--header-height);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filters button {
  padding: 10px 20px;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background-color var(--transition-speed), color var(--transition-speed);
}

.filters button:hover {
  background-color: #1d4ed8;
}

.filters button.active {
  background-color: #1d4ed8;
  color: black;
}

.table-container {
  overflow-x: auto;
  box-shadow: var(--shadow);
  border-radius: var(--border-radius);
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.styled-table th, .styled-table td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.styled-table th {
  background-color: var(--primary);
  color: white;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #f3f4f6;
}

footer {
  margin-left: var(--sidebar-width);
  padding: 1.5rem;
  text-align: center;
  color: var(--secondary);
  border-top: 1px solid var(--border-color);
}

@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition-speed);
  }

  .sidebar.active {
    transform: translateX(0);
  }

  .main-content, footer {
    margin-left: 0;
  }
}
</style>
