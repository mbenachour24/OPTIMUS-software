import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// ✅ Stocke Vue globalement (évite les conflits)
let vueApp = null;

// 📌 Fonction qui monte Vue après MathJax
function mountVueApp() {
  if (vueApp) {
    console.warn("⚠️ Vue app is already mounted.");
    return;
  }

  console.log("🚀 Mounting Vue...");
  vueApp = createApp(App);
  vueApp.use(router);
  vueApp.mount('#app');

  // 📡 Stocker Vue globalement pour debugging
  window.__VUE_APP__ = vueApp;
  console.log("🎉 Vue App Successfully Mounted! 🚀");

  // 🌎 Ajout de méthodes globales
  vueApp.config.globalProperties.solveCase = solveCase;
  vueApp.config.globalProperties.loadSolvedCases = loadSolvedCases;
}

// ✅ Charger MathJax après Vue
function loadMathJax() {
    console.log("📄 Loading MathJax...");
  
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$']],
        processEscapes: true,
        packages: ['base', 'ams']  // Corrige le chargement des packages
      },
      loader: {
        load: ['input/tex', 'output/chtml', '[tex]/ams']
      },
      chtml: {
        scale: 1.0, // Échelle par défaut des maths rendues
        minScale: 0.5,
        matchFontHeight: true, // Ajuste la hauteur des maths aux polices de la page
        mtextInheritFont: true, // Les mathtext utilisent la police environnante
        merrorInheritFont: true,
        mathmlSpacing: false,
        skipAttributes: {},
        exFactor: 0.5,
        displayAlign: 'center',
        displayIndent: '0em'
      },      
      startup: {
        ready: () => {
          console.log("✅ MathJax initialized!");
          window.MathJax.startup.defaultReady();
          if (window.__VUE_APP__) {
            window.MathJax.typeset();
          }
        }
      }
    };
  }
  
// ✅ Fonction API : résoudre un cas
async function solveCase(caseId, decision) {
  console.log(`🛠️ solveCase(${caseId}, ${decision}) triggered`);

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/solve_case/${caseId}?decision=${decision}`, {
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

    // 🔄 Recharge les cas résolus
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
}

// ✅ Fonction API : charger les cas résolus
async function loadSolvedCases() {
  console.log("🔄 Calling loadSolvedCases()...");

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/get_solved_cases`);
    const data = await response.json();

    if (!Array.isArray(data.solved_cases)) {
      console.warn("⚠️ API did not return an array for solved_cases.");
      return;
    }

    console.log("📡 Solved Cases Updated:", data.solved_cases);

    // Met à jour l'état Vue si nécessaire
    if (window.__VUE_APP__._instance) {
      window.__VUE_APP__._instance.proxy.solvedCases = data.solved_cases.sort((a, b) => b.id - a.id);
    }
  } catch (error) {
    console.error("❌ Error loading solved cases:", error);
  }
}

// 🚀 **Lancement** : Monte Vue **puis** charge MathJax
mountVueApp();
loadMathJax();
