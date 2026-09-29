<script setup lang="ts">
import type { AppDefinitionDashboard } from "@/types";
import { post } from "@/utils";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Props {
  modelValue: boolean;
  definition?: AppDefinitionDashboard;
}
const props = defineProps<Props>();
const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  submit: [];
}>();

const form = reactive({
  link: "" as string
});
const validForm = computed(() => Boolean(form.link.trim()));

function resetForm() {
  form.link = "";
}

async function onSubmit() {
  if (!props.definition || !validForm.value) return;

  try {
    const payload = {
      link: form.link,
      app_definition_id: props.definition.id
    };

    await post(`/app-submission/`, payload);
    resetForm();
    emit("update:modelValue", false);
    emit("submit");
  } catch (er) {
    console.error(er);
  }
}
</script>

<template>
  <Dialog :open="modelValue" @update:open="emit('update:modelValue', $event)">
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Create Submission</DialogTitle>
      </DialogHeader>
      <div class="grid gap-2 py-2">
        <Label for="app-link">App Link</Label>
        <Input id="app-link" v-model="form.link" placeholder="https://..." />
      </div>
      <DialogFooter>
        <Button variant="outline" @click="emit('update:modelValue', false)">Cancel</Button>
        <Button :disabled="!validForm" @click="onSubmit()">Submit</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
