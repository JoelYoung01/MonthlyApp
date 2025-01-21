<script setup lang="ts">
import type { AppDefinition } from "@/types";

const appDefinitions = ref<AppDefinition[]>();

async function getAppDefinitions() {
  const result = await fetch(`${import.meta.env.VITE_API_URL}/app-definition/`);
  appDefinitions.value = await result.json();
}

getAppDefinitions();
</script>

<template>
  <v-container>
    <section>
      <h2>Active App</h2>
      <div class="d-flex">
        <v-card class="pa-2">
          <v-card-title>
            <h5>Monthly App Challenge</h5>
          </v-card-title>
          <v-card-subtitle>
            <span class="fw-bold">Due Date: </span> Jan 31st, 2025
          </v-card-subtitle>
          <v-card-text> This app challenges you to build one app per month. </v-card-text>
          <v-card-actions>
            <v-btn color="success">Update Submission</v-btn>
            <v-btn to="/app-definition/1/detail">View Details</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </section>

    <section>
      <h2>Past Submissions</h2>
    </section>
  </v-container>
</template>

<style scoped>
section {
  margin-bottom: 2rem;
}
</style>
