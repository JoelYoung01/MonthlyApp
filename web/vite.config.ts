import { fileURLToPath, URL } from "node:url";

import { defineConfig, loadEnv, type Plugin } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import AutoImport from "unplugin-auto-import/vite";

function validateVars(requiredEnvVars: string[]): Plugin {
  return {
    name: "ValidateVars",
    config(_config, { mode }) {
      const fileEnv = loadEnv(mode, process.cwd(), "VITE_");
      const missingVars = requiredEnvVars.filter(
        (envVar) => !process.env[envVar] && !fileEnv[envVar]
      );

      if (missingVars.length > 0) {
        throw new Error(
          `Required environment variables are missing:\n` +
            missingVars.map((v) => `- ${v}`).join("\n") +
            `\n\nPlease check your .env file and ensure all required variables are defined.`
        );
      }
    }
  };
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    validateVars(["VITE_APP_TITLE", "VITE_API_URL", "VITE_GOOGLE_CLIENT_ID"]),
    AutoImport({
      // https://github.com/unplugin/unplugin-auto-import?tab=readme-ov-file#configuration
      include: [/\.vue$/, /\.vue\?vue/, /\.ts$/],
      imports: [
        {
          from: "vue",
          imports: ["ref", "reactive", "computed", "watch", "watchEffect"]
        }
      ],
      dts: "./auto-imports.d.ts"
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  }
});
