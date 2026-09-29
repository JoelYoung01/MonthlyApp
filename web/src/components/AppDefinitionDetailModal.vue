<script setup lang="ts">
import { Pencil, Plus } from "@lucide/vue";
import { RouterLink } from "vue-router";
import type { AppDefinition, AppSubmission } from "@/types";
import { formatDate, get } from "@/utils";
import { useSessionStore } from "@/stores/session";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";

interface Props {
  modelValue: boolean;
  appDefinitionId?: number | null;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  addSubmission: [];
}>();

const sessionStore = useSessionStore();
const detail = ref<AppDefinition | null>(null);
const submissions = ref<AppSubmission[]>([]);
const loading = ref(false);

watch(
  () => [props.modelValue, props.appDefinitionId] as const,
  async ([open, id]) => {
    if (!open || !id) {
      detail.value = null;
      submissions.value = [];
      return;
    }
    loading.value = true;
    try {
      detail.value = await get(`/app-definition/${id}/`);
      submissions.value = await get(`/app-submission/${id}/`);
    } catch (er) {
      console.error(er);
      detail.value = null;
      submissions.value = [];
    } finally {
      loading.value = false;
    }
  }
);
</script>

<template>
  <Dialog :open="modelValue" @update:open="emit('update:modelValue', $event)">
    <DialogContent class="sm:max-w-xl">
      <DialogHeader>
        <DialogTitle class="flex flex-wrap items-center gap-2 pe-8">
          <span>{{ detail?.name ?? (loading ? "Loading..." : "App Detail") }}</span>
        </DialogTitle>
      </DialogHeader>

      <div v-if="loading" class="py-8 text-center text-sm text-muted-foreground">
        Loading app details...
      </div>
      <div v-else-if="detail" class="grid gap-4 py-1">
        <p v-if="detail.description" class="text-sm text-foreground/80">
          {{ detail.description }}
        </p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <dt class="text-muted-foreground">Start</dt>
            <dd class="font-medium">{{ formatDate(detail.start_date) }}</dd>
          </div>
          <div>
            <dt class="text-muted-foreground">Due</dt>
            <dd class="font-medium">{{ formatDate(detail.due_date) }}</dd>
          </div>
        </div>

        <div class="space-y-2">
          <h3 class="text-sm font-semibold">Requirements</h3>
          <Table v-if="detail.requirements.length">
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Description</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="req in detail.requirements" :key="req.id">
                <TableCell>{{ req.name }}</TableCell>
                <TableCell>{{ req.description }}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <p v-else class="text-sm text-muted-foreground">No requirements defined.</p>
        </div>

        <div v-if="submissions.length" class="space-y-2">
          <h3 class="text-sm font-semibold">Your Submissions</h3>
          <div class="flex flex-col gap-2">
            <a
              v-for="submission in submissions"
              :key="submission.id"
              :href="submission.link ?? '#'"
              target="_blank"
              rel="noopener noreferrer"
              class="truncate text-sm text-primary underline-offset-4 hover:underline"
            >
              {{ submission.link }}
              <Badge variant="secondary" class="ms-2">
                {{ formatDate(submission.created_on) }}
              </Badge>
            </a>
          </div>
        </div>
      </div>

      <DialogFooter v-if="detail" class="sm:justify-between">
        <Button
          v-if="sessionStore.currentUser?.admin"
          as-child
          variant="outline"
        >
          <RouterLink :to="`/app-definition/${detail.id}/update`">
            <Pencil data-icon="inline-start" />
            Edit
          </RouterLink>
        </Button>
        <div class="flex flex-wrap gap-2">
          <Button variant="secondary" as-child>
            <RouterLink :to="`/app-definition/${detail.id}/detail`">Open page</RouterLink>
          </Button>
          <Button @click="emit('addSubmission')">
            <Plus data-icon="inline-start" />
            Add Submission
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
