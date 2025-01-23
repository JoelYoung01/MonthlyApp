<script setup lang="ts">
import { AppDefinitionStatus, type AppDefinitionDashboard } from "@/types";
import { formatDate } from "@/utils";

interface Props {
  definition?: AppDefinitionDashboard;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  addSubmit: [];
}>();

const isActive = computed(() => {
  return props.definition?.status === AppDefinitionStatus.Active;
});
const dateRange = computed(() => {
  return `${formatDate(props.definition?.start_date, true)} - ${formatDate(props.definition?.due_date, true)}`;
});
const daysRemaining = computed(() => {
  if (!props.definition) return null;
  const now = new Date();
  const due = new Date(props.definition.due_date + "Z");
  const timeDiff = due.getTime() - now.getTime();
  const days = Math.ceil(timeDiff / (1000 * 3600 * 24)); // Convert milliseconds to days
  return `${days} days remaining`;
});
</script>

<template>
  <v-card @click="$router.push(`/app-definition/${definition?.id}/detail`)">
    <v-card-title class="d-flex align-center">
      <div class="me-2">{{ definition?.name }}</div>
      <v-chip v-if="isActive" variant="elevated" color="success" size="small"> Active </v-chip>
      <v-spacer />
      <div class="text-end">
        <div class="fs-7 text-disabled">{{ dateRange }}</div>
        <div v-if="isActive" class="fs-7">{{ daysRemaining }}</div>
      </div>
    </v-card-title>
    <v-card-text>
      {{ definition?.description }}
    </v-card-text>
    <v-card-actions v-if="isActive" class="flex-row-reverse">
      <v-btn color="success" @click.stop="emit('addSubmit')">Add Submission</v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.fs-7 {
  font-size: 0.75rem;
}
</style>
