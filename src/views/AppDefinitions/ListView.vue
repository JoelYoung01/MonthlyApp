<script setup lang="ts">
import type { AppDefinition } from "@/types";
import { formatDate } from "@/utils";

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
    <v-row>
      <v-col v-for="definition in appDefinitions" :key="definition.id" cols="3">
        <v-card :to="`/app-definition/${definition.id}/detail`">
          <v-card-title class="d-flex align-center"
            >{{ definition.name }} <v-spacer />
            <span class="fs-7 text-disabled"
              >{{ formatDate(definition.start_date, true) }} -
              {{ formatDate(definition.due_date, true) }}</span
            ></v-card-title
          >
          <v-card-text>
            {{ definition.description }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.fs-7 {
  font-size: 0.75rem;
}
</style>
