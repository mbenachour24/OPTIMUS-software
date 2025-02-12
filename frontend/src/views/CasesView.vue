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
        <h2>Case Management</h2>
  
        <!-- Case Filters -->
        <div class="filters">
          <button @click="fetchCases('all')" id="filter-all" class="active">All</button>
          <button @click="fetchCases('pending')" id="filter-pending">Pending</button>
          <button @click="fetchCases('solved')" id="filter-solved">Solved</button>
        </div>
  
        <!-- Cases Table -->
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
      </main>
  
      <footer>
        © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
      </footer>
    </div>
  </template>
  
  <script>
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
          apiUrl = '/api/get_pending_cases';
        } else if (filter === "solved") {
          apiUrl = '/api/get_solved_cases';
        } else {
          apiUrl = '/api/get_all_cases';
        }
  
        try {
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
              <th>Resolved At</th>
            `;
          } else {
            tableHeader.innerHTML = `
              <th>ID</th>
              <th>Text</th>
              <th>Norm ID</th>
              <th>Created At</th>
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
  
          // Populate the table with cases
          cases.forEach(caseItem => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${caseItem.id || 'N/A'}</td>
              <td>${caseItem.text || 'N/A'}</td>
              <td>${caseItem.norm_id || 'N/A'}</td>
              <td>${caseItem.created_at ? new Date(caseItem.created_at).toLocaleString() : 'N/A'}</td>
              ${
                filter === "all"
                  ? `<td>${caseItem.status || 'N/A'}</td><td>${caseItem.resolved_at || 'Pending'}</td>`
                  : `<td>${caseItem.resolved_at || 'Pending'}</td>`
              }
            `;
            casesList.appendChild(row);
          });
  
          // Highlight selected filter
          document.querySelectorAll('.filters button').forEach(btn => btn.classList.remove('active'));
          document.getElementById(`filter-${filter}`).classList.add('active');
  
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
  