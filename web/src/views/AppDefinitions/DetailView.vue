<script setup lang="ts">
import { Pencil, Plus, Trash2 } from "@lucide/vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import type { AppSubmission, AppDefinition } from "@/types";
import { ApiError, del, formatDate, get } from "@/utils";
import AppSubmissionModal from "@/components/AppSubmissionModal.vue";
import { onMounted } from "vue";
import { useSessionStore } from "@/stores/session";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";

const route = useRoute();
const router = useRouter();
const sessionStore = useSessionStore();

const detail = ref<AppDefinition>();
const submissions = ref<AppSubmission[]>();
const submitModalVisible = ref(false);

async function loadAppDefinition() {
  try {
    const url = `/app-definition/${route.params.app_definition_id}/`;
    detail.value = await get(url);
  } catch (er) {
    if ((er as ApiError).status === 404) {
      router.push("/definition-not-found");
    } else {
      console.error(er);
    }
  }
}

async function loadSubmissions() {
  try {
    const url = `/app-submission/${route.params.app_definition_id}/`;
    submissions.value = await get(url);
  } catch (er) {
    console.error(er);
  }
}

async function deleteSubmission(submissionId: number | string) {
  try {
    await del(`/app-submission/${submissionId}/`);
    await loadSubmissions();
  } catch (er) {
    console.error(er);
  }
}

onMounted(() => {
  loadAppDefinition();
  loadSubmissions();
});
</script>

<template>
  <div class="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-8">
    <Card>
      <CardHeader class="flex flex-row items-center justify-between gap-4 space-y-0">
        <CardTitle class="text-3xl">{{ detail?.name }}</CardTitle>
        <div class="flex shrink-0 flex-wrap items-center gap-2">
          <Button v-if="sessionStore.currentUser?.admin" as-child variant="secondary">
            <RouterLink :to="`/app-definition/${route.params.app_definition_id}/update`">
              <Pencil data-icon="inline-start" />
              Edit Definition
            </RouterLink>
          </Button>
          <Button @click="submitModalVisible = true">
            <Plus data-icon="inline-start" />
            Add Submission
          </Button>
        </div>
      </CardHeader>
    </Card>

    <Card>
      <CardContent class="grid gap-6 pt-6 sm:grid-cols-3">
        <div>
          <dt class="text-sm font-medium text-muted-foreground">Start Date</dt>
          <dd class="mt-1">{{ formatDate(detail?.start_date) }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-muted-foreground">Due Date</dt>
          <dd class="mt-1">{{ formatDate(detail?.due_date) }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-muted-foreground">Description</dt>
          <dd class="mt-1">{{ detail?.description }}</dd>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle>Requirements</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="req in detail?.requirements ?? []" :key="req.id">
              <TableCell>{{ req.name }}</TableCell>
              <TableCell>{{ req.description }}</TableCell>
            </TableRow>
            <TableRow v-if="detail?.requirements.length === 0">
              <TableCell colspan="2" class="text-muted-foreground">
                No requirements defined for this App.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

    <Card v-if="submissions?.length">
      <CardHeader>
        <CardTitle>Your Submissions</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Link</TableHead>
              <TableHead>Submitted On</TableHead>
              <TableHead class="w-12" />
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="submission in submissions" :key="submission.id">
              <TableCell>
                <a
                  class="text-primary underline-offset-4 hover:underline"
                  :href="submission.link ?? '/bad-link'"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ submission.link }}
                </a>
              </TableCell>
              <TableCell>{{ formatDate(submission.created_on) }}</TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="icon-sm"
                  class="text-destructive"
                  @click="deleteSubmission(submission.id)"
                >
                  <Trash2 />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>

  <AppSubmissionModal
    v-model="submitModalVisible"
    :definition="detail"
    @submit="loadSubmissions()"
  />
</template>
