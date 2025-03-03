//vite.config.js

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Allows `@` to refer to `src/`
    },
  },
  server: {
    host: true, // Allows network access (useful for mobile testing)
    port: 5173, // Default Vite port
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        secure: false,
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
      },
    },
  },
  build: {
    outDir: path.resolve(__dirname, 'dist'), // Ensures it's inside frontend/
    sourcemap: true, // Enables source maps for debugging in production
    chunkSizeWarningLimit: 500, // Adjusts chunk size warnings
  },
  optimizeDeps: {
    include: ["vue", "axios"], // Pre-bundle dependencies for faster startup
    exclude: ["some-heavy-lib"], // Avoid pre-bundling large dependencies
  },
});