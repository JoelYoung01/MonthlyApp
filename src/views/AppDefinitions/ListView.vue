<script setup lang="ts">
import type { AppDefinition } from "@/types";

const appDefinitions = ref<AppDefinition[]>([]);

async function getAppDefinitions() {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/app-definition/`);
  appDefinitions.value = await response.json();
}

getAppDefinitions();
</script>

<template>
  <v-container>
    <div class="d-flex">
      <h1>App Definitions</h1>

      <v-spacer />

      <v-btn color="primary" prepend-icon="mdi-plus" to="/app-definition/create">Create New</v-btn>
    </div>
    <v-card v-for="definition in appDefinitions" :key="definition.id">
      {{ definition.name }}
    </v-card>
  </v-container>
</template>
