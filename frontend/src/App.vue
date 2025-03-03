<template>
  <div>
    <header class="app-header">
      <h1>Optimus Interface</h1>
      <button @click="toggleDarkMode" class="dark-mode-toggle">
        {{ isDarkMode ? "🌞 Light Mode" : "🌙 Dark Mode" }}
      </button>
    </header>

    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: localStorage.getItem("darkMode") === "true", // Load dark mode state
    };
  },
  mounted() {
    if (this.isDarkMode) {
      document.body.classList.add("dark-mode");
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.body.classList.toggle("dark-mode", this.isDarkMode);
      localStorage.setItem("darkMode", this.isDarkMode); // Save to localStorage
    },
  },
};
</script>

<style>
@import "./assets/tailwind.css";


/* 🌙 Dark Mode Variables */
:root {
  --background-light: #f9fafb;
  --background-dark: #1f2937;
  --text-light: #333;
  --text-dark: #f3f4f6;
  --primary-light: #2563eb;
  --primary-dark: #3b82f6;
}

/* 🎨 Default Light Mode */
body {
  background: var(--background-light);
  color: var(--text-light);
  transition: all 0.3s ease-in-out;
}

/* 🌙 Dark Mode */
.dark-mode {
  --background-light: #1f2937 !important;
  --text-light: #f3f4f6 !important;
  --primary-light: #3b82f6 !important;
}

.dark-mode body {
  background: var(--background-light) !important;
  color: var(--text-light) !important;
}

/* 🔵 Header */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--primary-light);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background 0.3s ease-in-out;
}

/* 🎛️ Dark Mode Toggle Button */
.dark-mode-toggle {
  background: white;
  color: var(--primary-light);
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease-in-out;
}

.dark-mode-toggle:hover {
  background: #ddd;
}

/* 🌙 Adjust Header in Dark Mode */
.dark-mode .app-header {
  background: var(--primary-dark) !important;
}
</style>