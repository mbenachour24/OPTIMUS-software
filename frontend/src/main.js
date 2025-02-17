import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Import MathJax
import 'mathjax/es5/tex-mml-chtml.js';

// 🔧 MathJax Configuration
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
  },
  loader: {
    load: ['input/tex', 'output/chtml', 'ui/menu', '[tex]/ams', '[tex]/amscd']
  }
};

// 🚀 FIX: Properly Initialize Vue App
const app = createApp(App);

// 🌎 Attach Vue globally for debugging & external calls
window.__VUE_APP__ = app;

console.log("✅ Vue App Initialized:", window.__VUE_APP__);

// 🔥 Register Global Method: solveCase
app.config.globalProperties.solveCase = async function (caseId, decision) {
  console.log(`🛠️ solveCase(${caseId}, ${decision}) triggered`);

  try {
    const response = await fetch(`${API_BASE_URL}/api/solve_case/${caseId}?decision=${decision}`, {
      method: 'POST',
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert(`❌ API Error: ${errorData.detail}`);
      return;
    }

    const result = await response.json();
    alert(`✅ Case ${caseId} solved as ${decision}`);
    console.log("📡 API Response:", result);

    // 🔄 Reload cases after solving
    if (typeof window.__VUE_APP__.config.globalProperties.loadSolvedCases === 'function') {
      console.log("🔄 Refreshing solved cases...");
      await window.__VUE_APP__.config.globalProperties.loadSolvedCases();
    } else {
      console.warn("⚠️ loadSolvedCases() not found in global properties!");
    }
  } catch (error) {
    console.error('❌ Error solving case:', error);
    alert('An unexpected error occurred while solving the case.');
  }
};

// 🔄 Register Global Method: loadSolvedCases (Ensure cases refresh properly)
app.config.globalProperties.loadSolvedCases = async function () {
  console.log("🔄 Calling loadSolvedCases()...");

  try {
    const response = await fetch(`${API_BASE_URL}/api/get_solved_cases`);
    const data = await response.json();

    if (!Array.isArray(data.solved_cases)) {
      console.warn("⚠️ API did not return an array for solved_cases.");
      return;
    }

    console.log("📡 Solved Cases Updated:", data.solved_cases);

    // Manually update Vue state if needed
    if (window.__VUE_APP__._instance) {
      window.__VUE_APP__._instance.proxy.solvedCases = data.solved_cases.sort((a, b) => b.id - a.id);
    }
  } catch (error) {
    console.error("❌ Error loading solved cases:", error);
  }
};

// ✅ Use router & mount Vue app
app.use(router).mount('#app');

console.log("🎉 Vue App Successfully Mounted! 🚀");
