<script setup lang="ts">
import { Plus, Save, Trash2, X } from "@lucide/vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import type { AppDefinition } from "@/types";
import { onMounted } from "vue";
import { ApiError, del, get, post, put } from "@/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";

const route = useRoute();
const router = useRouter();

const detail = ref<AppDefinition>();
const form = reactive({
  id: null as number | null,
  name: "" as string,
  start_date: null as string | null,
  due_date: null as string | null,
  description: "" as string
});
const defaultReq = {
  id: null as number | null,
  name: "" as string,
  description: "" as string
};
const requirementForms = reactive<(typeof defaultReq)[]>([]);

const creating = computed(() => {
  return !route.params.app_definition_id;
});
const formValid = computed(() => {
  return Boolean(
    form.name.trim() &&
      form.start_date &&
      form.due_date &&
      requirementForms.every((req) => req.name.trim() && req.description.trim())
  );
});
const canSubmit = computed(() => {
  return formValid.value && requirementForms.length > 0;
});
const cancelTo = computed(() => {
  if (creating.value) return `/app-definition/list`;
  return `/app-definition/${route.params.app_definition_id}/detail`;
});

function addReq() {
  requirementForms.push({ ...defaultReq });
}
function delReq(index: number) {
  requirementForms.splice(index, 1);
}
function processDate(dateString: string | null) {
  if (!dateString) {
    return null;
  } else if (dateString.includes("T")) {
    if (!dateString.includes("Z")) dateString += "Z";
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  } else {
    return new Date(`${dateString}T00:00:00`).toISOString().replace("Z", "");
  }
}

function fillForm() {
  if (!detail.value) return;
  form.id = detail.value.id ?? null;
  form.name = detail.value.name ?? "";
  form.start_date = detail.value.start_date ?? null;
  form.due_date = detail.value.due_date ?? null;
  form.description = detail.value.description ?? "";

  for (const reqDetail of detail.value.requirements) {
    requirementForms.push({
      id: reqDetail.id ?? null,
      name: reqDetail.name ?? "",
      description: reqDetail.description ?? ""
    });
  }
}

async function loadAppDefinition() {
  try {
    detail.value = await get(`/app-definition/${route.params.app_definition_id}/`);
    fillForm();
  } catch (er) {
    if ((er as ApiError).status === 404) {
      router.push(`/definition-not-found`);
    } else {
      console.error(er);
    }
  }
}

async function save() {
  try {
    let appDefId = null;

    if (creating.value) {
      const data = await post("/app-definition/", form);
      appDefId = data.id;
    } else {
      const data = await put(`/app-definition/${route.params.app_definition_id}/`, form);
      appDefId = data.id;
    }

    const createRequirements = requirementForms
      .filter((reqForm) => !reqForm.id)
      .map((req) => post(`/requirement/`, { ...req, app_definition_id: appDefId }));

    const updateRequirements = requirementForms
      .filter((reqForm) => reqForm.id)
      .map((req) => put(`/requirement/${req.id}/`, req));

    const deleteRequirements =
      detail.value?.requirements
        .filter((reqDetail) => !requirementForms.some((reqForm) => reqForm.id === reqDetail.id))
        .map((req) => del(`/requirement/${req.id}/`)) ?? [];

    await Promise.all([...createRequirements, ...updateRequirements, ...deleteRequirements]);
    router.push(`/app-definition/${appDefId}/detail`);
  } catch (er) {
    console.error(er);
  }
}

onMounted(() => {
  if (!creating.value) {
    loadAppDefinition();
  }
});
</script>

<template>
  <form class="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-8" @submit.prevent="save()">
    <Card>
      <CardHeader class="flex flex-row items-center justify-between gap-4 space-y-0">
        <CardTitle class="text-3xl">
          {{ creating ? "Create New" : "Update" }} App Definition
        </CardTitle>
        <div class="flex shrink-0 flex-wrap items-center gap-2">
          <Button variant="outline" as-child type="button">
            <RouterLink :to="cancelTo">
              <X data-icon="inline-start" />
              Cancel
            </RouterLink>
          </Button>
          <Button type="submit" :disabled="!canSubmit">
            <Save data-icon="inline-start" />
            Save Changes
          </Button>
        </div>
      </CardHeader>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle>Details</CardTitle>
      </CardHeader>
      <CardContent class="grid gap-6 md:grid-cols-3">
        <div class="grid gap-2">
          <Label for="name">Name</Label>
          <Input id="name" v-model="form.name" required />
        </div>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="start-date">Start Date</Label>
            <Input
              id="start-date"
              type="date"
              required
              :model-value="processDate(form.start_date) ?? ''"
              @update:model-value="form.start_date = processDate(String($event))"
            />
          </div>
          <div class="grid gap-2">
            <Label for="due-date">Due Date</Label>
            <Input
              id="due-date"
              type="date"
              required
              :model-value="processDate(form.due_date) ?? ''"
              @update:model-value="form.due_date = processDate(String($event))"
            />
          </div>
        </div>
        <div class="grid gap-2">
          <Label for="description">Description</Label>
          <Textarea id="description" v-model="form.description" class="min-h-28" />
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardHeader class="flex flex-row items-end justify-between gap-4 space-y-0">
        <CardTitle>Requirements</CardTitle>
        <Button type="button" size="sm" @click="addReq()">
          <Plus data-icon="inline-start" />
          Add Requirement
        </Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead class="w-12" />
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="(reqForm, i) in requirementForms" :key="i">
              <TableCell>
                <Input v-model="reqForm.name" required />
              </TableCell>
              <TableCell>
                <Input v-model="reqForm.description" required />
              </TableCell>
              <TableCell>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon-sm"
                  class="text-destructive"
                  @click="delReq(i)"
                >
                  <Trash2 />
                </Button>
              </TableCell>
            </TableRow>
            <TableRow v-if="requirementForms.length === 0">
              <TableCell colspan="3">
                <Button type="button" @click="addReq()">
                  <Plus data-icon="inline-start" />
                  Add Requirement
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </form>
</template>
