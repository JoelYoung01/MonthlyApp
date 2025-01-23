<script setup lang="ts">
import AppDefinitionCard from "@/components/AppDefinitionCard.vue";
import AppSubmissionModal from "@/components/AppSubmissionModal.vue";
import type { AppDefinitionDashboard } from "@/types";
import { onMounted } from "vue";

const appDefinitions = ref<AppDefinitionDashboard[]>();
const activeApps = ref<AppDefinitionDashboard[]>();
const submitCardVisible = ref(false);
const submitDefinition = ref<AppDefinitionDashboard>();

const completeApps = computed(() => {
  return appDefinitions.value?.filter((app) => new Date(app.due_date + "Z") < new Date());
});

function onSubmitClick(definition: AppDefinitionDashboard) {
  submitDefinition.value = definition;
  submitCardVisible.value = true;
}

async function getAppDefinitions() {
  const result = await fetch(`${import.meta.env.VITE_API_URL}/app-definition/`);
  appDefinitions.value = await result.json();

  const activeResult = await fetch(`${import.meta.env.VITE_API_URL}/app-definition/active/`);
  activeApps.value = await activeResult.json();
}

onMounted(() => {
  getAppDefinitions();
});
</script>

<template>
  <v-container>
    <section>
      <h2>Active App</h2>
      <v-alert v-if="!activeApps?.length" type="info"> No Active Apps found in db. </v-alert>
      <v-row v-else>
        <v-col v-for="definition in activeApps" :key="definition.id" cols="4">
          <AppDefinitionCard
            :definition="definition"
            include-actions
            @add-submit="onSubmitClick(definition)"
          />
        </v-col>
      </v-row>
    </section>

    <section>
      <h2>Completed Applications</h2>
      <v-alert v-if="!completeApps?.length" type="info"> No Completed Apps found in db. </v-alert>
      <v-row v-else>
        <v-col v-for="definition in completeApps" :key="definition.id" cols="4">
          <AppDefinitionCard
            :definition="definition"
            include-actions
            @add-submit="onSubmitClick(definition)"
          />
        </v-col>
      </v-row>
    </section>

    <AppSubmissionModal v-model="submitCardVisible" :definition="submitDefinition" />
  </v-container>
</template>

<style scoped>
section {
  margin-bottom: 2rem;
}
</style>
