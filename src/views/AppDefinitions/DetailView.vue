<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import type { AppDefinition } from "@/types";
import { ApiError, del, formatDate, get } from "@/utils";
import AppSubmissionModal from "@/components/AppSubmissionModal.vue";
import { onMounted } from "vue";

const route = useRoute();
const router = useRouter();

const detail = ref<AppDefinition>();
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

async function deleteSubmission(submissionId: number | string) {
  try {
    await del(`/app-submission/${submissionId}/`);
    await loadAppDefinition();
  } catch (er) {
    console.error(er);
  }
}

onMounted(() => {
  loadAppDefinition();
});
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
      <v-btn prepend-icon="mdi-plus" color="success" @click="submitModalVisible = true"
        >Add Submission</v-btn
      >
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

    <v-card v-if="detail?.submissions.length" class="pa-3">
      <h3>Your Submissions</h3>
      <v-table>
        <thead>
          <tr>
            <th>Link</th>
            <th>Submitted On</th>
            <th class="action-col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="submission in detail?.submissions ?? []" :key="submission.id">
            <td>
              <a :href="submission.link ?? '/bad-link'" target="_blank">{{ submission.link }}</a>
            </td>
            <td>{{ formatDate(submission.created_on) }}</td>
            <td>
              <v-btn
                variant="text"
                color="red"
                icon="mdi-delete"
                @click="deleteSubmission(submission.id)"
              />
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>

  <AppSubmissionModal
    v-model="submitModalVisible"
    :definition="detail"
    @submit="loadAppDefinition()"
  />
</template>

<style scoped>
thead th {
  font-weight: bold !important;
}

.action-col {
  width: 0px;
}
</style>
