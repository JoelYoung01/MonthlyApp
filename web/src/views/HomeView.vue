<script setup lang="ts">
import type { AppDefinitionDashboard, AppSubmissionDetail } from "@/types";
import { get } from "@/utils";
import { useSessionStore } from "@/stores/session";
import AppDefinitionCard from "@/components/AppDefinitionCard.vue";
import AppSubmissionModal from "@/components/AppSubmissionModal.vue";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Info } from "@lucide/vue";

const sessionStore = useSessionStore();

const appDefinitions = ref<AppDefinitionDashboard[]>();
const submissions = ref<AppSubmissionDetail[]>([]);
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

function appSubmissions(appId: number) {
  return submissions.value.filter((s) => s.app_definition_id === appId);
}

async function getAppDefinitions() {
  try {
    appDefinitions.value = await get(`/app-definition/`);
    activeApps.value = await get(`/app-definition/active/`);
  } catch (er) {
    console.error(er);
  }
}

async function getSubmissions() {
  try {
    submissions.value = await get("/app-submission/");
  } catch (er) {
    console.error(er);
  }
}

watch(
  () => sessionStore.currentUser,
  (value) => {
    if (value) {
      getAppDefinitions();
      getSubmissions();
    }
  },
  { immediate: true }
);
</script>

<template>
  <div class="mx-auto w-full max-w-7xl space-y-10 px-4 py-8">
    <section class="space-y-4">
      <h2 class="text-2xl font-semibold tracking-tight">Active App</h2>
      <Alert v-if="!activeApps?.length">
        <Info />
        <AlertTitle>No active apps</AlertTitle>
        <AlertDescription>No Active Apps found in db.</AlertDescription>
      </Alert>
      <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <AppDefinitionCard
          v-for="definition in activeApps"
          :key="definition.id"
          :definition="definition"
          :submissions="appSubmissions(definition.id)"
          @add-submit="onSubmitClick(definition)"
        />
      </div>
    </section>

    <section class="space-y-4">
      <h2 class="text-2xl font-semibold tracking-tight">Completed Applications</h2>
      <Alert v-if="!completeApps?.length">
        <Info />
        <AlertTitle>No completed apps</AlertTitle>
        <AlertDescription>No Completed Apps found in db.</AlertDescription>
      </Alert>
      <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <AppDefinitionCard
          v-for="definition in completeApps"
          :key="definition.id"
          :definition="definition"
          :submissions="appSubmissions(definition.id)"
          @add-submit="onSubmitClick(definition)"
        />
      </div>
    </section>

    <AppSubmissionModal
      v-model="submitCardVisible"
      :definition="submitDefinition"
      @submit="getSubmissions()"
    />
  </div>
</template>
