// src/config.js

// On récupère la variable d'environnement VITE_API_BASE_URL définie dans ton .env,
// ou on utilise "https://optimus-software.onrender.com" comme valeur par défaut.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://optimus-software.onrender.com";
console.log("API_BASE_URL in frontend:", API_BASE_URL);
