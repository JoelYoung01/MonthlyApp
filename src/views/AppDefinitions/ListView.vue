<script setup lang="ts">
import type { AppDefinition } from "@/types";

const appDefinitions = ref<AppDefinition[]>([]);

async function getAppDefinitions() {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/app-definition/`);
  appDefinitions.value = await response.json();
}

getAppDefinitions();
</script>
