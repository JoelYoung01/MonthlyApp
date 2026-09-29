<script setup lang="ts">
import { AppDefinitionStatus, type AppDefinitionDashboard, type AppSubmission } from "@/types";
import { formatDate } from "@/utils";
import { useRouter } from "vue-router";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from "@/components/ui/card";

interface Props {
  definition?: AppDefinitionDashboard;
  submissions?: AppSubmission[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  addSubmit: [];
}>();
const router = useRouter();

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
  const days = Math.ceil(timeDiff / (1000 * 3600 * 24));
  return `${days} days remaining`;
});
const latestSubmission = computed(() => {
  if (!props.submissions?.length) {
    return null;
  }

  return props.submissions.toSorted(
    (a, b) => new Date(b.created_on).getTime() - new Date(a.created_on).getTime()
  )[0];
});

function openDetail() {
  if (!props.definition) return;
  router.push(`/app-definition/${props.definition.id}/detail`);
}
</script>

<template>
  <Card class="cursor-pointer transition-colors hover:bg-muted/40" @click="openDetail">
    <CardHeader class="flex flex-row items-start justify-between gap-3 space-y-0">
      <div class="flex min-w-0 flex-1 items-center gap-2">
        <CardTitle class="truncate">{{ definition?.name }}</CardTitle>
        <Badge v-if="isActive" variant="secondary">Active</Badge>
      </div>
      <div class="shrink-0 text-end text-xs text-muted-foreground">
        <div>{{ dateRange }}</div>
        <div v-if="isActive" class="text-foreground">{{ daysRemaining }}</div>
      </div>
    </CardHeader>
    <CardContent>
      <CardDescription class="text-sm text-foreground/80">
        {{ definition?.description }}
      </CardDescription>
    </CardContent>
    <CardFooter class="justify-between gap-2">
      <Button v-if="latestSubmission" as-child size="sm" @click.stop>
        <a :href="latestSubmission.link ?? ''" target="_blank" rel="noopener noreferrer">
          Open Submission
        </a>
      </Button>
      <div v-else />
      <Button v-if="isActive" size="sm" variant="secondary" @click.stop="emit('addSubmit')">
        Add Submission
      </Button>
    </CardFooter>
  </Card>
</template>
