<script setup lang="ts">
import { CalendarClock, Check, ChevronLeft, ChevronRight, Plus } from "@lucide/vue";
import {
  AppDefinitionStatus,
  type AppDefinitionDashboard,
  type AppSubmissionDetail
} from "@/types";
import { useSessionStore } from "@/stores/session";
import {
  appsForMonthKey,
  monthKeyFromParts,
  parseAppDate,
  type MonthKey
} from "@/utils/reschedule";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const sessionStore = useSessionStore();

export type CalendarMonth = {
  year: number;
  month: number;
  key: MonthKey;
  label: string;
  isCurrent: boolean;
  apps: AppDefinitionDashboard[];
};

interface Props {
  definitions?: AppDefinitionDashboard[];
  submissions?: AppSubmissionDetail[];
  year?: number;
  rescheduleMode?: boolean;
  /** Live preview definitions while dragging; falls back to definitions */
  previewDefinitions?: AppDefinitionDashboard[] | null;
  dropTargetKey?: string | null;
}

const props = withDefaults(defineProps<Props>(), {
  definitions: () => [],
  submissions: () => [],
  year: new Date().getFullYear(),
  rescheduleMode: false,
  previewDefinitions: null,
  dropTargetKey: null
});

const emit = defineEmits<{
  "update:year": [value: number];
  selectMonth: [month: CalendarMonth];
  addSubmission: [definition: AppDefinitionDashboard];
  viewApp: [definition: AppDefinitionDashboard];
  "update:rescheduleMode": [value: boolean];
  dragPreview: [payload: { appId: number; targetMonthKey: string } | null];
  dropApp: [payload: { appId: number; targetMonthKey: string }];
  nudgeApp: [payload: { appId: number; deltaMonths: number }];
}>();

const visibleYear = computed({
  get: () => props.year,
  set: (value: number) => emit("update:year", value)
});

const now = new Date();
const currentKey = monthKeyFromParts(now.getFullYear(), now.getMonth());

const displayDefinitions = computed(
  () => props.previewDefinitions ?? props.definitions ?? []
);

const draggingAppId = ref<number | null>(null);

const months = computed<CalendarMonth[]>(() => {
  const apps = displayDefinitions.value;
  return Array.from({ length: 12 }, (_, month) => {
    const key = monthKeyFromParts(visibleYear.value, month);
    const label = new Date(visibleYear.value, month, 1).toLocaleDateString(undefined, {
      month: "long"
    });
    return {
      year: visibleYear.value,
      month,
      key,
      label,
      isCurrent: key === currentKey,
      apps: appsForMonth(apps, visibleYear.value, month)
    };
  });
});

function appsForMonth(apps: AppDefinitionDashboard[], year: number, month: number) {
  return appsForMonthKey(apps, monthKeyFromParts(year, month));
}

function primaryApp(month: CalendarMonth) {
  return month.apps[0] ?? null;
}

function isOverdue(app: AppDefinitionDashboard) {
  return parseAppDate(app.due_date).getTime() < startOfToday().getTime();
}

function startOfToday() {
  const today = new Date();
  return new Date(today.getFullYear(), today.getMonth(), today.getDate());
}

function latestSubmission(appId: number) {
  const appSubs = (props.submissions ?? []).filter((s) => s.app_definition_id === appId);
  if (!appSubs.length) return null;
  return appSubs.toSorted(
    (a, b) => new Date(b.created_on).getTime() - new Date(a.created_on).getTime()
  )[0];
}

function showAddSubmission(month: CalendarMonth) {
  if (props.rescheduleMode) return false;
  const app = primaryApp(month);
  if (!app) return false;
  const hasSubmission = Boolean(latestSubmission(app.id));
  return !isOverdue(app) || !hasSubmission;
}

function appTone(status: AppDefinitionStatus) {
  switch (status) {
    case AppDefinitionStatus.Active:
      return "bg-primary text-primary-foreground";
    case AppDefinitionStatus.Complete:
      return "bg-muted text-muted-foreground";
    case AppDefinitionStatus.Future:
      return "bg-secondary text-secondary-foreground";
    default:
      return "bg-accent text-accent-foreground";
  }
}

function shiftYear(delta: number) {
  visibleYear.value = visibleYear.value + delta;
}

function goToThisYear() {
  visibleYear.value = now.getFullYear();
}

function onAddSubmission(event: MouseEvent, app: AppDefinitionDashboard) {
  event.stopPropagation();
  emit("addSubmission", app);
}

function onMonthClick(month: CalendarMonth) {
  if (props.rescheduleMode) return;
  emit("selectMonth", month);
}

function toggleReschedule() {
  if (!sessionStore.currentUser?.admin) return;
  emit("update:rescheduleMode", !props.rescheduleMode);
  emit("dragPreview", null);
  draggingAppId.value = null;
}

function onDragStart(event: DragEvent, app: AppDefinitionDashboard) {
  if (!props.rescheduleMode) return;
  draggingAppId.value = app.id;
  event.dataTransfer?.setData("text/plain", String(app.id));
  event.dataTransfer!.effectAllowed = "move";
}

function onDragEnd() {
  draggingAppId.value = null;
  emit("dragPreview", null);
}

function onDragOver(event: DragEvent, month: CalendarMonth) {
  if (!props.rescheduleMode || draggingAppId.value == null) return;
  event.preventDefault();
  if (event.dataTransfer) event.dataTransfer.dropEffect = "move";
  emit("dragPreview", {
    appId: draggingAppId.value,
    targetMonthKey: month.key
  });
}

function onDrop(event: DragEvent, month: CalendarMonth) {
  if (!props.rescheduleMode) return;
  event.preventDefault();
  const raw = event.dataTransfer?.getData("text/plain");
  const appId = raw ? Number(raw) : draggingAppId.value;
  draggingAppId.value = null;
  emit("dragPreview", null);
  if (!appId || Number.isNaN(appId)) return;
  emit("dropApp", { appId, targetMonthKey: month.key });
}

function onNudge(event: MouseEvent, app: AppDefinitionDashboard, deltaMonths: number) {
  event.stopPropagation();
  emit("nudgeApp", { appId: app.id, deltaMonths });
}

function onViewApp(event: MouseEvent, app: AppDefinitionDashboard) {
  event.stopPropagation();
  emit("viewApp", app);
}
</script>

<template>
  <div class="overflow-hidden rounded-xl border bg-card shadow-sm">
    <div class="flex flex-wrap items-center justify-between gap-3 border-b px-4 py-3">
      <div class="flex items-center gap-2">
        <Button variant="outline" size="icon-sm" @click="shiftYear(-1)">
          <ChevronLeft />
        </Button>
        <Button variant="outline" size="icon-sm" @click="shiftYear(1)">
          <ChevronRight />
        </Button>
        <h2 class="ms-1 text-xl font-semibold tracking-tight">{{ visibleYear }}</h2>
        <span
          v-if="rescheduleMode"
          class="ms-2 rounded-full bg-amber-500/15 px-2 py-0.5 text-xs font-medium text-amber-700 dark:text-amber-400"
        >
          Reschedule mode
        </span>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <Button
          v-if="visibleYear !== now.getFullYear()"
          variant="outline"
          size="sm"
          @click="goToThisYear"
        >
          This year
        </Button>
        <Button
          v-if="sessionStore.currentUser?.admin"
          :variant="rescheduleMode ? 'default' : 'outline'"
          size="sm"
          @click="toggleReschedule"
        >
          <Check v-if="rescheduleMode" data-icon="inline-start" />
          <CalendarClock v-else data-icon="inline-start" />
          {{ rescheduleMode ? "Done" : "Reschedule" }}
        </Button>
      </div>
    </div>

    <div class="grid gap-px bg-border sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="month in months"
        :key="month.key"
        role="button"
        tabindex="0"
        :class="
          cn(
            'flex min-h-36 flex-col gap-2 bg-card p-4 text-left transition-colors',
            !rescheduleMode &&
              'cursor-pointer hover:bg-muted/40 focus-visible:bg-muted/40 focus-visible:outline-none',
            rescheduleMode && 'cursor-default',
            'last:rounded-b-xl',
            'sm:[&:nth-child(11)]:rounded-bl-xl sm:last:rounded-bl-none sm:last:rounded-br-xl',
            'lg:[&:nth-child(10)]:rounded-bl-xl lg:[&:nth-child(11)]:rounded-bl-none',
            'xl:[&:nth-child(9)]:rounded-bl-xl xl:[&:nth-child(10)]:rounded-bl-none xl:[&:nth-child(11)]:rounded-bl-none',
            month.isCurrent && !rescheduleMode && 'ring-1 ring-inset ring-primary/40',
            rescheduleMode &&
              dropTargetKey === month.key &&
              'bg-amber-500/10 ring-2 ring-inset ring-amber-500/50'
          )
        "
        @click="onMonthClick(month)"
        @keydown.enter="onMonthClick(month)"
        @dragover="onDragOver($event, month)"
        @drop="onDrop($event, month)"
      >
        <div class="flex items-center justify-between gap-2">
          <span :class="cn('text-sm font-semibold', month.isCurrent && 'text-primary')">
            {{ month.label }}
          </span>
          <span
            v-if="month.isCurrent"
            class="rounded-full bg-primary px-2 py-0.5 text-[10px] font-medium text-primary-foreground"
          >
            Now
          </span>
        </div>

        <div v-if="month.apps.length" class="mt-auto flex flex-col gap-1.5">
          <div
            v-for="app in month.apps"
            :key="`${month.key}-${app.id}`"
            :draggable="rescheduleMode"
            :class="
              cn(
                'rounded-md px-2 py-1 text-xs font-medium',
                appTone(app.status),
                rescheduleMode && 'cursor-grab active:cursor-grabbing',
                draggingAppId === app.id && 'opacity-50'
              )
            "
            :title="app.name"
            @dragstart="onDragStart($event, app)"
            @dragend="onDragEnd"
            @click.stop
          >
            <div class="flex items-center gap-1">
              <div class="min-w-0 flex-1 truncate">{{ app.name }}</div>
              <Button
                size="xs"
                variant="secondary"
                class="h-5 shrink-0 bg-background/80 px-1.5 text-[10px] text-foreground hover:bg-background"
                @click="onViewApp($event, app)"
              >
                View
              </Button>
            </div>
            <div v-if="rescheduleMode" class="mt-1 flex items-center gap-1">
              <Button
                size="icon-xs"
                variant="secondary"
                class="size-5 bg-background/80 text-foreground hover:bg-background"
                title="Move 1 month earlier"
                @click="onNudge($event, app, -1)"
              >
                <ChevronLeft class="size-3" />
              </Button>
              <Button
                size="icon-xs"
                variant="secondary"
                class="size-5 bg-background/80 text-foreground hover:bg-background"
                title="Move 1 month later"
                @click="onNudge($event, app, 1)"
              >
                <ChevronRight class="size-3" />
              </Button>
            </div>
          </div>
          <Button
            v-if="showAddSubmission(month) && primaryApp(month)"
            size="xs"
            variant="outline"
            class="w-full"
            @click="onAddSubmission($event, primaryApp(month)!)"
          >
            <Plus data-icon="inline-start" />
            Add Submission
          </Button>
        </div>
        <p v-else class="mt-auto text-xs text-muted-foreground">
          <template v-if="rescheduleMode">Drop app here</template>
          <template v-else-if="sessionStore.currentUser?.admin">
            No app — click to create
          </template>
          <template v-else>No app this month</template>
        </p>
      </div>
    </div>
  </div>
</template>
