<script setup lang="ts">
import type { AppDefinition } from "@/types";
import { useRoute } from "vue-router";

const route = useRoute();

const detail = ref<AppDefinition>();

async function loadAppDefinition() {
  const result = await fetch(
    `${import.meta.env.VITE_API_URL}/app-definition/${route.params.app_definition_id}`
  );
  detail.value = await result.json();
}

loadAppDefinition();
</script>

<template>
  <v-container class="d-flex flex-column gap-2">
    <v-card class="d-flex align-center pa-2 gap-2">
      <h1>Monthly App Challenge</h1>

      <v-spacer />

      <v-btn prepend-icon="mdi-pencil" color="primary">Edit Definition</v-btn>
      <v-btn prepend-icon="mdi-plus" color="success">Add Submission</v-btn>
    </v-card>
    <v-card class="pa-2">
      <v-row>
        <v-col cols="3">
          <dt>Start Date</dt>
          <dd>Jan 1st, 2025</dd>
        </v-col>
        <v-col cols="3">
          <dt>Due Date</dt>
          <dd>Jan 31st, 2025</dd>
        </v-col>
        <v-col cols="3">
          <dt>Description</dt>
          <dd>This is an app designed to challenge you to build an app each month.</dd>
        </v-col>
      </v-row>
    </v-card>

    <v-card class="pa-2">
      <h3>Requirements</h3>
      <v-table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Live App</td>
            <td>The App is live and accessible from internet.</td>
          </tr>
          <tr>
            <td>Supports Users</td>
            <td>Can support users and is specific to each user.</td>
          </tr>
          <tr>
            <td>Apps filled out for 2025</td>
            <td>All app ideas for 2025 are in.</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <v-card class="pa-2">
      <h3>Your Submissions</h3>
      <v-table>
        <thead>
          <tr>
            <th>Status</th>
            <th>Created On</th>
            <th>Submitted On</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Submitted</td>
            <td>Jan 16th, 2025</td>
            <td>Jan 16th, 2025</td>
            <td>
              <v-btn variant="text" color="red" icon="mdi-delete" />
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<style scoped>
.d-flex dl {
  flex: 0 0 33.33%;
}
</style>
