<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import type { AppDefinition } from "@/types";
import { formatDate } from "@/utils";

const route = useRoute();
const router = useRouter();

const detail = ref<AppDefinition>();

async function loadAppDefinition() {
  try {
    const url = `${import.meta.env.VITE_API_URL}/app-definition/${route.params.app_definition_id}/`;
    const response = await fetch(url);

    if (response.status === 404) {
      router.push("/definition-not-found");
    }

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    detail.value = await response.json();
  } catch (er) {
    console.error(er);
  }
}

loadAppDefinition();
</script>

<template>
  <v-container class="d-flex flex-column gap-2">
    <v-card class="d-flex align-center pa-3 gap-2">
      <h1>{{ detail?.name }}</h1>

      <v-spacer />

      <v-btn
        prepend-icon="mdi-pencil"
        color="primary"
        :to="`/app-definition/${route.params.app_definition_id}/update`"
      >
        Edit Definition
      </v-btn>
      <v-btn prepend-icon="mdi-plus" color="success">Add Submission</v-btn>
    </v-card>
    <v-card class="pa-3">
      <v-row>
        <v-col cols="3">
          <dt>Start Date</dt>
          <dd>{{ formatDate(detail?.start_date) }}</dd>
        </v-col>
        <v-col cols="3">
          <dt>Due Date</dt>
          <dd>{{ formatDate(detail?.due_date) }}</dd>
        </v-col>
        <v-col cols="3">
          <dt>Description</dt>
          <dd>{{ detail?.description }}</dd>
        </v-col>
      </v-row>
    </v-card>

    <v-card class="pa-3">
      <h3>Requirements</h3>
      <v-table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="req in detail?.requirements ?? []" :key="req.id">
            <td>{{ req.name }}</td>
            <td>{{ req.description }}</td>
          </tr>
          <tr v-if="detail?.requirements.length === 0">
            <td colspan="2">No requirements defined for this App.</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <v-card class="pa-3">
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
