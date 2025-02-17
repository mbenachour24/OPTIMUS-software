// src/config.js

// On récupère la variable d'environnement VITE_API_BASE_URL définie dans ton .env,
// ou on utilise "http://127.0.0.1:8000" comme valeur par défaut.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
console.log("API_BASE_URL in frontend:", API_BASE_URL);
