//judicialinterfaceview.vue

<template>
  <div>
    <header>
      <h1>Optimus - Judicial System Interface</h1>
    </header>

    <aside class="sidebar">
      <h3>Navigation</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
      <h3>Systems</h3>
      <ul>
        <li><a href="/judicial" class="active-link">Judicial System</a></li>
        <li><a href="/political">Political System</a></li>
        <li><a href="/norms">View Norms</a></li>
        <li><a href="/cases">View Cases</a></li>
      </ul>
      <h3>Analytics</h3>
      <ul>
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <main class="main-content">
      <h2>Welcome, Judicial System</h2>
      <div class="notification">
        <strong>Notification:</strong>
        <span id="latest-notification">No notifications yet.</span>
      </div>

      <!-- Log Entries Section -->
      <div>
        <h3>Log Entries</h3>
        <div id="log-entries" class="scrollable-section">
          <!-- Logs will be dynamically populated here -->
        </div>
      </div>

      <!-- Interaction Area -->
      <div class="action-buttons">
        <button @click="markNormUnconstitutional">Mark Norm as Unconstitutional</button>
        <button @click="requestReform">Request Reform</button>
      </div>

      <!-- Cases Section -->
      <div class="cases-section">
        <div class="section-header">
          <h2>Case Management</h2>
          <button @click="generateCitizenCases" class="generate-button">Generate Citizen Cases</button>
        </div>

        <div class="cases-container">
          <!-- Pending Cases -->
          <div>
            <h3>Pending Cases</h3>
            <div class="scrollable-section">
              <div v-for="caseItem in pendingCases" :key="caseItem.id" class="case-item">
                <p>Case #{{ caseItem.id }}: {{ caseItem.text }}</p>
                <button @click="() => solveCase(caseItem.id, 'Accepted')">Accept</button>
                <button @click="() => solveCase(caseItem.id, 'Rejected')">Reject</button>
              </div>
              <!-- Pending cases will be populated here -->
            </div>
          </div>

          <!-- Solved Cases -->
          <div>
            <h3>Solved Cases</h3>
            <div class="scrollable-section" id="solved-cases-list">
              <div v-for="caseItem in solvedCases" :key="caseItem.id" class="case-item solved">
                <p>Case #{{ caseItem.id }}: {{ caseItem.text }}</p>
              </div>
              <!-- Solved cases will be dynamically populated here -->
            </div>
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
import { API_BASE_URL } from '../config.js';

// Deduce the WebSocket URL from API_BASE_URL
const WS_URL = API_BASE_URL.replace(/^http/, 'ws') + '/ws';

export default {
  name: 'JudicialSystem',
  data() {
    return {
      socket: null,
      solvedCases: [],
      pendingCases: []
    };
  },
  mounted() {
    this.connectWebSocket();
    this.fetchLogs();
    this.loadPendingCases();
    this.loadSolvedCases();

    setInterval(() => {
      this.loadPendingCases();
      this.loadSolvedCases();
    }, 30000);

    this.$root.solveCase = this.solveCase;

    console.log("✅ Component mounted, checking solveCase method...");
    console.log("solveCase method exists?", typeof this.solveCase);
  },
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket(WS_URL);

      this.socket.onopen = () => {
        console.log("✅ WebSocket connected.");
      };

      this.socket.onmessage = (event) => {
        try {
          let data = JSON.parse(event.data);
          if (data.event === "case_solved") {
            console.log(`📡 Case #${data.data.case_id} solved.`);
            this.loadSolvedCases();  // Refresh solved cases
          }
        } catch (error) {
          console.error("❌ WebSocket message error:", error);
        }
      };

      this.socket.onclose = () => {
        console.warn("⚠️ WebSocket disconnected. Attempting to reconnect in 5s...");
        setTimeout(this.connectWebSocket, 5000);
      };

      this.socket.onerror = (error) => {
        console.error("❌ WebSocket encountered an error:", error);
      };
    },
    async fetchLogs() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/get_norms`);
        if (!response.ok) throw new Error(`Failed to fetch norms: ${response.status}`);

        const norms = await response.json();
        const logEntries = document.getElementById('log-entries');

        if (!logEntries) {
          console.error("❌ Error: 'log-entries' element not found.");
          return;
        }

        logEntries.innerHTML = '';
        norms.forEach(norm => {
          const logEntry = document.createElement('div');
          logEntry.className = 'log-entry';
          logEntry.innerHTML = `<strong>Norm #${norm.id}:</strong> ${norm.text} - Valid: ${norm.valid}`;
          logEntries.appendChild(logEntry);
        });
      } catch (error) {
        console.error('❌ Error fetching norms:', error);
      }
    },
    async markNormUnconstitutional() {
      const normId = prompt("Enter the Norm ID to mark as unconstitutional:");
      if (!normId) return;

      try {
        const response = await fetch(`${API_BASE_URL}/api/mark_unconstitutional`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ norm_id: parseInt(normId) })
        });
        const result = await response.json();

        if (result.error) {
          alert(`Error: ${result.error}`);
        } else {
          alert(`Notification sent to Political System: Norm #${normId} is unconstitutional.`);
          document.getElementById('latest-notification').innerText =
            `Political System notified about Norm #${normId}: unconstitutional.`;
        }
      } catch (error) {
        console.error('Error marking norm as unconstitutional:', error);
        alert('An error occurred while marking the norm as unconstitutional.');
      }
    },
    async solveCase(caseId, decision) {
      console.log("🛠️ solveCase called with:", caseId, decision);

      try {
        const response = await fetch(`${API_BASE_URL}/api/solve_case/${caseId}?decision=${decision}`, { method: 'POST' });

        if (!response.ok) {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
          return;
        }

        const result = await response.json();
        alert(result.message);
        this.loadPendingCases(); // Refresh pending cases
        this.loadSolvedCases();  // Refresh solved cases
      } catch (error) {
        console.error('❌ Error solving case:', error);
        alert('An error occurred while solving the case.');
      }
    },
    async loadPendingCases() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/get_pending_cases`);
        const data = await response.json();

        if (!data.pending_cases || !Array.isArray(data.pending_cases)) {
          console.error("❌ API response missing 'pending_cases' or not an array.");
          return;
        }

        // Sort cases from newest to oldest and update Vue state
        this.pendingCases = data.pending_cases.sort((a, b) => b.id - a.id);
      } catch (error) {
        console.error('❌ Error loading pending cases:', error);
      }
    },
    async loadSolvedCases() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/get_solved_cases`);
        const data = await response.json();
        this.solvedCases = data.solved_cases.sort((a, b) => b.id - a.id);
      } catch (error) {
        console.error('❌ Error loading solved cases:', error);
      }
    },
    async generateCitizenCases() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/generate_citizen_cases`, { method: 'POST' });
        const data = await response.json();

        alert(data.message);

        if (Array.isArray(data.cases) && data.cases.length > 0) {
          this.loadPendingCases();
        } else {
          console.warn("⚠️ No cases returned from API.");
        }
      } catch (error) {
        console.error('❌ Error generating citizen cases:', error);
        alert('An error occurred while generating citizen cases.');
      }
    },
    handleCaseClick(caseId, decision) {
      console.log("🔄 Calling solveCase:", caseId, decision);
      if (typeof this.solveCase !== 'function') {
        console.error("❌ solveCase is NOT defined in Vue!");
      } else {
        this.solveCase(caseId, decision);
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

.notification {
  background: #f3f4f6;
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.scrollable-section {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
}

.log-entry {
  background: white;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.cases-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.case-item {
  background: white;
  padding: 15px;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.case-item.solved {
  background-color: #f0f8f0;
}

.case-item button {
  background-color: #4CAF50;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.case-item button:hover {
  background-color: #45a049;
}

.action-buttons {
  margin: 20px 0;
}

.action-buttons button {
  background-color: var(--primary);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.action-buttons button:hover {
  background-color: #45a049;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.generate-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.generate-button:hover {
  background-color: #45a049;
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
