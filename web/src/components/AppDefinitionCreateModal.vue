<script setup lang="ts">
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
import { Textarea } from "@/components/ui/textarea";

interface Props {
  modelValue: boolean;
  /** Year-month key, e.g. "2026-09" */
  monthKey?: string | null;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  created: [id: number];
}>();

const form = reactive({
  name: "",
  description: "",
  start_date: "",
  due_date: ""
});

const canSubmit = computed(() =>
  Boolean(form.name.trim() && form.start_date && form.due_date)
);

const monthLabel = computed(() => {
  if (!props.monthKey) return "";
  const [year, month] = props.monthKey.split("-").map(Number);
  return new Date(year, month - 1, 1).toLocaleDateString(undefined, {
    month: "long",
    year: "numeric"
  });
});

watch(
  () => [props.modelValue, props.monthKey] as const,
  ([open, monthKey]) => {
    if (!open || !monthKey) return;
    const [year, month] = monthKey.split("-").map(Number);
    const start = new Date(year, month - 1, 1);
    const end = new Date(year, month, 0);
    form.name = "";
    form.description = "";
    form.start_date = toInputDate(start);
    form.due_date = toInputDate(end);
  }
);

function toInputDate(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function toApiDate(dateString: string) {
  return new Date(`${dateString}T00:00:00`).toISOString().replace("Z", "");
}

async function onSubmit() {
  if (!canSubmit.value) return;

  try {
    const data = await post("/app-definition/", {
      name: form.name.trim(),
      description: form.description.trim(),
      start_date: toApiDate(form.start_date),
      due_date: toApiDate(form.due_date)
    });
    emit("update:modelValue", false);
    emit("created", data.id);
  } catch (er) {
    console.error(er);
  }
}
</script>

<template>
  <Dialog :open="modelValue" @update:open="emit('update:modelValue', $event)">
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Create App{{ monthLabel ? ` — ${monthLabel}` : "" }}</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-2">
        <div class="grid gap-2">
          <Label for="create-name">Name</Label>
          <Input id="create-name" v-model="form.name" autofocus />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div class="grid gap-2">
            <Label for="create-start">Start Date</Label>
            <Input id="create-start" v-model="form.start_date" type="date" />
          </div>
          <div class="grid gap-2">
            <Label for="create-due">Due Date</Label>
            <Input id="create-due" v-model="form.due_date" type="date" />
          </div>
        </div>
        <div class="grid gap-2">
          <Label for="create-description">Description</Label>
          <Textarea id="create-description" v-model="form.description" class="min-h-24" />
        </div>
      </div>
      <DialogFooter>
        <Button variant="outline" @click="emit('update:modelValue', false)">Cancel</Button>
        <Button :disabled="!canSubmit" @click="onSubmit()">Create</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
