import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  // server: {
  //   proxy: {
  //     "^/merge": "http://localhost:8000",
  //   },
  // },
  // server: {
  //   proxy: {
  //     "^/merge": "http://backend:8080",
  //   },
  // },
});
