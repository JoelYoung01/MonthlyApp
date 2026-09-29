<script setup lang="ts">
import {
  AppDefinitionStatus,
  type AppDefinitionDashboard,
  type AppSubmissionDetail
} from "@/types";
import { get, put } from "@/utils";
import {
  appsDifferingDates,
  previewMoveAppToMonth,
  previewShiftAppByMonths
} from "@/utils/reschedule";
import { useSessionStore } from "@/stores/session";
import YearCalendar, { type CalendarMonth } from "@/components/YearCalendar.vue";
import AppSubmissionModal from "@/components/AppSubmissionModal.vue";
import AppDefinitionCreateModal from "@/components/AppDefinitionCreateModal.vue";
import AppDefinitionDetailModal from "@/components/AppDefinitionDetailModal.vue";

const sessionStore = useSessionStore();

const appDefinitions = ref<AppDefinitionDashboard[]>([]);
const submissions = ref<AppSubmissionDetail[]>([]);
const visibleYear = ref(new Date().getFullYear());
const rescheduleMode = ref(false);
const previewDefinitions = ref<AppDefinitionDashboard[] | null>(null);
const dropTargetKey = ref<string | null>(null);
const saving = ref(false);

const createModalOpen = ref(false);
const createMonthKey = ref<string | null>(null);

const detailModalOpen = ref(false);
const detailAppId = ref<number | null>(null);

const submitModalOpen = ref(false);
const submitDefinition = ref<AppDefinitionDashboard>();

function latestSubmission(appId: number) {
  const appSubs = submissions.value.filter((s) => s.app_definition_id === appId);
  if (!appSubs.length) return null;
  return appSubs.toSorted(
    (a, b) => new Date(b.created_on).getTime() - new Date(a.created_on).getTime()
  )[0];
}

function onSelectMonth(month: CalendarMonth) {
  if (rescheduleMode.value) return;

  const app = month.apps[0];

  if (!app) {
    if (!sessionStore.currentUser?.admin) return;
    createMonthKey.value = month.key;
    createModalOpen.value = true;
    return;
  }

  if (app.status === AppDefinitionStatus.Complete) {
    const submission = latestSubmission(app.id);
    if (submission?.link) {
      window.open(submission.link, "_blank", "noopener,noreferrer");
      return;
    }
  }

  detailAppId.value = app.id;
  detailModalOpen.value = true;
}

function onAddSubmission(definition: AppDefinitionDashboard) {
  submitDefinition.value = definition;
  submitModalOpen.value = true;
}

function onViewApp(definition: AppDefinitionDashboard) {
  detailAppId.value = definition.id;
  detailModalOpen.value = true;
}

function onDetailAddSubmission() {
  const definition = appDefinitions.value.find((app) => app.id === detailAppId.value);
  if (!definition) return;
  detailModalOpen.value = false;
  onAddSubmission(definition);
}

function onDragPreview(payload: { appId: number; targetMonthKey: string } | null) {
  if (!payload) {
    previewDefinitions.value = null;
    dropTargetKey.value = null;
    return;
  }
  dropTargetKey.value = payload.targetMonthKey;
  previewDefinitions.value = previewMoveAppToMonth(
    appDefinitions.value,
    payload.appId,
    payload.targetMonthKey
  );
}

async function persistDefinitions(next: AppDefinitionDashboard[]) {
  const changed = appsDifferingDates(appDefinitions.value, next);
  if (!changed.length) {
    previewDefinitions.value = null;
    dropTargetKey.value = null;
    return;
  }

  saving.value = true;
  // Optimistic UI
  appDefinitions.value = next;
  previewDefinitions.value = null;
  dropTargetKey.value = null;

  try {
    await Promise.all(
      changed.map((app) =>
        put(`/app-definition/${app.id}/`, {
          start_date: app.start_date,
          due_date: app.due_date
        })
      )
    );
    await getAppDefinitions();
  } catch (er) {
    console.error(er);
    await getAppDefinitions();
  } finally {
    saving.value = false;
  }
}

async function onDropApp(payload: { appId: number; targetMonthKey: string }) {
  const next = previewMoveAppToMonth(
    appDefinitions.value,
    payload.appId,
    payload.targetMonthKey
  );
  await persistDefinitions(next);
}

async function onNudgeApp(payload: { appId: number; deltaMonths: number }) {
  const next = previewShiftAppByMonths(
    appDefinitions.value,
    payload.appId,
    payload.deltaMonths
  );
  await persistDefinitions(next);
}

watch(rescheduleMode, () => {
  previewDefinitions.value = null;
  dropTargetKey.value = null;
});

async function getAppDefinitions() {
  try {
    appDefinitions.value = await get(`/app-definition/`);
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

async function onCreated(id: number) {
  await getAppDefinitions();
  detailAppId.value = id;
  detailModalOpen.value = true;
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
  <div class="mx-auto w-full max-w-7xl space-y-6 px-4 py-8">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="text-3xl font-semibold tracking-tight">Year Overview</h1>
        <p class="mt-1 text-sm text-muted-foreground">
          <template v-if="rescheduleMode">
            Drag apps between months, or use the arrows to nudge ±1 month. Dropping onto an
            occupied month shifts the next contiguous apps until a gap.
          </template>
          <template v-else> Click a month to create, view, or open its submission. </template>
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-3">
        <span v-if="saving" class="text-xs text-muted-foreground">Saving…</span>
        <div v-if="!rescheduleMode" class="flex flex-wrap gap-2 text-xs text-muted-foreground">
          <span class="inline-flex items-center gap-1.5">
            <span class="size-2.5 rounded-full bg-primary" /> Active
          </span>
          <span class="inline-flex items-center gap-1.5">
            <span class="size-2.5 rounded-full bg-muted-foreground/40" /> Complete
          </span>
          <span class="inline-flex items-center gap-1.5">
            <span class="size-2.5 rounded-full bg-secondary-foreground/30" /> Upcoming
          </span>
        </div>
      </div>
    </div>

    <YearCalendar
      v-model:year="visibleYear"
      v-model:reschedule-mode="rescheduleMode"
      :definitions="appDefinitions"
      :preview-definitions="previewDefinitions"
      :drop-target-key="dropTargetKey"
      :submissions="submissions"
      @select-month="onSelectMonth"
      @add-submission="onAddSubmission"
      @view-app="onViewApp"
      @drag-preview="onDragPreview"
      @drop-app="onDropApp"
      @nudge-app="onNudgeApp"
    />

    <AppDefinitionCreateModal
      v-model="createModalOpen"
      :month-key="createMonthKey"
      @created="onCreated"
    />

    <AppDefinitionDetailModal
      v-model="detailModalOpen"
      :app-definition-id="detailAppId"
      @add-submission="onDetailAddSubmission"
    />

    <AppSubmissionModal
      v-model="submitModalOpen"
      :definition="submitDefinition"
      @submit="getSubmissions()"
    />
  </div>
</template>
