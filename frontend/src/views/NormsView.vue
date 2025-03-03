// NormsView.vue

<template>
  <div>
    <header>
      <h1>Optimus - Norm Management</h1>
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
        <li><a href="/norms" class="active-link">View Norms</a></li>
        <li><a href="/cases">View Cases</a></li>
      </ul>
      <h3>Analytics</h3>
      <ul>
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <main class="main-content">
      <h2>Norm Management</h2>

      <!-- Norm Filters -->
      <div class="filters">
        <button @click="fetchNorms('all')" id="filter-all" class="active">All</button>
        <button @click="fetchNorms('valid')" id="filter-valid">Valid</button>
        <button @click="fetchNorms('invalid')" id="filter-invalid">Invalid</button>
      </div>

      <!-- Norms Table -->
      <table class="styled-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Text</th>
            <th>Complexity</th>
            <th>Valid</th>
          </tr>
        </thead>
        <tbody id="norms-list">
          <!-- Norms will be dynamically loaded here -->
        </tbody>
      </table>
    </main>

    <footer>
      © 2025 Optimus Interface - Enhancing Rule of Law through Systems Interaction
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:8000";

export default {
  name: 'ViewNorms',
  mounted() {
    this.fetchNorms('all');
  },
  methods: {
    async fetchNorms(filter = "all") {
      let endpoint;

      // Détermine l'endpoint de l'API en fonction du filtre
      if (filter === "valid") {
        endpoint = '/api/get_valid_norms';
      } else if (filter === "invalid") {
        endpoint = '/api/get_invalid_norms';
      } else {
        endpoint = '/api/get_all_norms';
      }

      try {
        const apiUrl = `${API_BASE_URL}${endpoint}`;
        console.log(`Fetching norms from: ${apiUrl}`);
        const response = await axios.get(apiUrl);
        const norms = response.data; // La réponse est directement le tableau de normes
        console.log("Norms array:", norms);

        const normsList = document.getElementById('norms-list');
        const tableHeader = document.querySelector('.styled-table thead tr');

        if (!normsList || !tableHeader) {
          console.error('Error: Table elements not found in the DOM.');
          return;
        }

        normsList.innerHTML = ''; // Efface le contenu du tableau

        if (norms.length === 0) {
          normsList.innerHTML = '<tr><td colspan="4">No norms found.</td></tr>';
          return;
        }

        // Remplit le tableau avec les normes
        norms.sort((a, b) => b.id - a.id); // Tri du plus récent au plus ancien
        norms.forEach(norm => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${norm.id || 'N/A'}</td>
            <td>${norm.text || 'N/A'}</td>
            <td>${norm.complexity || 'N/A'}</td>
            <td>${norm.valid ? 'Yes' : 'No'}</td>
          `;
          normsList.appendChild(row);
        });

        // Met en évidence le filtre sélectionné
        document.querySelectorAll('.filters button').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`filter-${filter}`).classList.add('active');
      } catch (error) {
        console.error('Error fetching norms:', error);
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
  width: var(--sidebar-width) !important;
  height: calc(100vh - var(--header-height)) !important;
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
  margin-left: var(--sidebar-width) !important;
  width: calc(100vw - var(--sidebar-width)) !important;
  min-height: 100vh;
  margin-top: var(--header-height);
  padding: 2rem;
}

.filters {
  margin-bottom: 20px;
}

.filters button {
  padding: 10px;
  margin: 5px;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.3s;
}

.filters button:hover {
  background-color: #45a049;
}

.filters button.active {
  background-color: #45a049;
  color: black;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
}

.styled-table th, .styled-table td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
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
