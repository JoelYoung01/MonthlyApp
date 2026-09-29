<script setup lang="ts">
import { Plus } from "@lucide/vue";
import { RouterLink } from "vue-router";
import { useSessionStore } from "@/stores/session";
import { AppDefinitionStatus, type AppDefinitionDashboard } from "@/types";
import { formatDate, get } from "@/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const sessionStore = useSessionStore();

const appDefinitions = ref<AppDefinitionDashboard[]>([]);

async function getAppDefinitions() {
  appDefinitions.value = await get(`/app-definition/`);
}
function isActive(def: AppDefinitionDashboard) {
  return def.status === AppDefinitionStatus.Active;
}

getAppDefinitions();
</script>

<template>
  <div class="mx-auto w-full max-w-7xl space-y-6 px-4 py-8">
    <div class="flex items-center justify-between gap-4">
      <h1 class="text-3xl font-semibold tracking-tight">App Definitions</h1>

      <Button v-if="sessionStore.currentUser?.admin" as-child>
        <RouterLink to="/app-definition/create">
          <Plus data-icon="inline-start" />
          Create New
        </RouterLink>
      </Button>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <RouterLink
        v-for="definition in appDefinitions"
        :key="definition.id"
        :to="`/app-definition/${definition.id}/detail`"
        class="block no-underline"
      >
        <Card class="h-full transition-colors hover:bg-muted/40">
          <CardHeader class="flex flex-row items-start justify-between gap-3 space-y-0">
            <div class="flex min-w-0 flex-1 items-center gap-2">
              <CardTitle class="truncate">{{ definition.name }}</CardTitle>
              <Badge v-if="isActive(definition)" variant="secondary">Active</Badge>
            </div>
            <span class="shrink-0 text-xs text-muted-foreground">
              {{ formatDate(definition.start_date, true) }} -
              {{ formatDate(definition.due_date, true) }}
            </span>
          </CardHeader>
          <CardContent>
            <CardDescription class="text-sm text-foreground/80">
              {{ definition.description }}
            </CardDescription>
          </CardContent>
        </Card>
      </RouterLink>
    </div>
  </div>
</template>
