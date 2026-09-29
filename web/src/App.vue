<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from "vue-router";
import { Home, List } from "@lucide/vue";
import AccountButton from "./components/AccountButton.vue";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";

const route = useRoute();

const title = import.meta.env.VITE_APP_TITLE;

const mainClass = computed(() =>
  cn("flex-1", route.meta.useShadedBackground ? "bg-muted/40" : undefined)
);
</script>

<template>
  <div class="relative flex min-h-svh flex-col bg-background text-foreground">
    <header class="sticky top-0 z-40 border-b bg-primary text-primary-foreground shadow-sm">
      <div class="mx-auto flex h-14 w-full max-w-7xl items-center gap-2 px-4">
        <RouterLink
          class="me-4 text-lg font-semibold tracking-tight text-primary-foreground no-underline"
          to="/"
        >
          {{ title }}
        </RouterLink>

        <Button
          variant="ghost"
          as-child
          class="text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
        >
          <RouterLink to="/app-definition/list">
            <List data-icon="inline-start" />
            Definitions
          </RouterLink>
        </Button>

        <Button
          variant="ghost"
          as-child
          class="text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
        >
          <RouterLink to="/">
            <Home data-icon="inline-start" />
            Home
          </RouterLink>
        </Button>

        <div class="ms-auto">
          <AccountButton />
        </div>
      </div>
    </header>

    <main :class="mainClass">
      <RouterView />
    </main>

    <Toaster />
  </div>
</template>
