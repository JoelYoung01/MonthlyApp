/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_API_URL: string;
  // Add Env Variables here
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
