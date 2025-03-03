// PoliticalInterfaceView.vue

<template>
    <div>
      <header>
        <h1>Optimus - Political System Interface</h1>
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
          <li><a href="/political" class="active-link">Political System</a></li>
          <li><a href="/norms">View Norms</a></li>
          <li><a href="/cases">View Cases</a></li>
        </ul>
        <h3>Analytics</h3>
        <ul>
          <li><a href="/statistics">Statistics Dashboard</a></li>
        </ul>
      </aside>
  
      <main class="main-content">
        <h2>Welcome, Political System</h2>
        <h3>Notifications</h3>
        <div id="notifications" class="scrollable-section">
          <!-- Notifications will be dynamically loaded here -->
          <p>No notifications yet.</p>
        </div>
  
        <h3>Log Entries</h3>
        <div id="log-entries" class="scrollable-section">
          <div v-for="norm in logs" :key="norm.id" class="log-entry">
            <strong>Norm #{{ norm.id }}:</strong> {{ norm.text }} - Valid: {{ norm.valid }}
          </div>
        </div>
  
        <!-- Interaction Area -->
        <div class="action-buttons">
          <button @click="createNewNorm">Create New Norm</button>
          <button @click="reviewJudicialFeedback">Review Judicial Feedback</button>
        </div>
      </main>
  
      <footer>
        © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PoliticalSystem',
    data() {
      return {
        socket: null,
      };
    },
    mounted() {
      this.connectWebSocket();
      this.fetchLogs();
      this.fetchNotifications();
      setInterval(this.fetchLogs, 30000);
      setInterval(this.fetchNotifications, 30000);
    },
    methods: {
      connectWebSocket() {
        this.socket = new WebSocket("ws://localhost:8000/ws");
  
        this.socket.onopen = () => {
          console.log("✅ WebSocket connected successfully.");
        };
  
        this.socket.onmessage = (event) => {
          try {
            let data = JSON.parse(event.data);
  
            if (data.event === "norm_created") {
              console.log("📡 Norm created via WebSocket:", data);
              this.fetchLogs(); // Refresh logs when a new norm is created
            }
  
            if (data.event === "mark_unconstitutional") {
              console.log(`📡 Norm marked as unconstitutional via WebSocket: ${data.data.norm_id}`);
              this.fetchNotifications(); // Refresh notifications
            }
          } catch (error) {
            console.error("❌ WebSocket message error:", error);
          }
        };
  
        this.socket.onclose = (event) => {
          console.warn(`⚠️ WebSocket disconnected. Reconnecting in 5s...`);
          setTimeout(this.connectWebSocket, 5000);
        };
  
        this.socket.onerror = (error) => {
          console.error("❌ WebSocket encountered an error:", error);
        };
      },
      async fetchLogs() {
        try {
            const response = await fetch('/api/get_norms');

            // ✅ Log response before parsing
            console.log("🔍 Fetch Logs Response:", response);

            if (!response.ok) {
                throw new Error(`Failed to fetch norms: ${response.status} ${response.statusText}`);
            }

            const norms = await response.json(); // Ensure this is valid JSON
            console.log("✅ Parsed Norms:", norms);

            // 🚀 Sort newest first
            this.logs = norms.sort((a, b) => b.id - a.id);

        } catch (error) {
            console.error("❌ Error fetching norms:", error);
        }
    },
          
      async fetchNotifications() {
        try {
          const response = await fetch('/api/get_notifications');
          if (!response.ok) throw new Error(`Failed to fetch notifications: ${response.status}`);
  
          const notifications = await response.json();
          const notificationsDiv = document.getElementById('notifications');
          if (!notificationsDiv) {
            console.error("❌ Error: 'notifications' element not found.");
            return;
          }
  
          const unconstitutionalNotifications = notifications.filter(n =>
            n.type === "mark_unconstitutional" && n.message.includes("marked as unconstitutional")
          );
  
          notificationsDiv.innerHTML = unconstitutionalNotifications.length
            ? unconstitutionalNotifications.map(n => `
                <div class="notification-item ${n.type}">
                  <p class="notification-message">${n.message}</p>
                  <small class="notification-time">${new Date(n.timestamp).toLocaleString()}</small>
                </div>
              `).join('')
            : '<p>No unconstitutional norm notifications.</p>';
        } catch (error) {
          console.error('Error fetching notifications:', error);
        }
      },
      async createNewNorm() {
        const normText = prompt("Enter a description for the new norm:");
        if (!normText) return;
  
        try {
          const response = await fetch('/api/create_norm', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: normText })
          });
  
          const norm = await response.json();
          if (norm.error) {
            alert(`Error: ${norm.error}`);
          } else {
            alert(`Created Norm #${norm.id}: ${norm.text}`);
            this.fetchLogs();
          }
        } catch (error) {
          console.error('Error creating norm:', error);
          alert('An error occurred while creating the norm.');
        }
      },
      async reviewJudicialFeedback() {
        const normId = prompt("Enter the Norm ID to review feedback:");
        if (!normId) return;
  
        try {
          const response = await fetch('/api/check_constitutionality', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ norm_id: parseInt(normId) })  // ✅ Ensures integer conversion
          });
  
          const result = await response.json();
  
          if (response.status === 404) {
            alert(`Error: ${result.detail}`);
          } else if (response.status !== 200) {
            alert(`Unexpected error: ${result.detail}`);
          } else {
            alert(`Feedback on Norm #${result.id}: Valid: ${result.valid ? "Yes" : "No"}`);
          }
  
          this.fetchLogs(); // ✅ Refresh logs after checking
        } catch (error) {
          console.error('Error reviewing feedback:', error);
          alert('An error occurred while reviewing feedback.');
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
  
  .notification-item {
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
    background-color: #f8f9fa;
    border-left: 4px solid #ccc;
  }
  
  .notification-item.judicial {
    border-left-color: #dc3545;
    background-color: #fff3f3;
  }
  
  .notification-message {
    margin: 0;
    font-size: 1.1em;
  }
  
  .notification-time {
    color: #666;
    font-size: 0.9em;
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
  