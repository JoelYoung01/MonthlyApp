<script setup lang="ts">
import { Home } from "@lucide/vue";
import { RouterLink } from "vue-router";
import { Button } from "@/components/ui/button";
</script>

<template>
  <div class="mx-auto flex w-full max-w-7xl flex-col items-center px-4 py-16 text-center">
    <h1 class="text-3xl font-semibold tracking-tight">404 - Not Found</h1>
    <p class="mb-6 mt-2 text-muted-foreground">The page you are looking for cannot be found!</p>
    <Button as-child>
      <RouterLink to="/">
        <Home data-icon="inline-start" />
        Go Home
      </RouterLink>
    </Button>
  </div>
</template>
