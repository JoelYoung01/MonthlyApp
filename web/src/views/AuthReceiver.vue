<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { LoaderCircle } from "@lucide/vue";
import { Button } from "@/components/ui/button";

const route = useRoute();
const longWait = ref(false);
const somethingWrong = ref(false);
const message = computed<string>(() => {
  let msg = `Signing you in with ${route.meta.authType}...`;
  if (longWait.value) {
    msg = `Still signing in with ${route.meta.authType}...`;
  }

  return msg;
});

onMounted(() => {
  setTimeout(() => {
    longWait.value = true;
  }, 5000);

  setTimeout(() => {
    somethingWrong.value = true;
  }, 15000);
});
</script>

<template>
  <div class="mx-auto flex w-full max-w-7xl flex-col items-center px-4 py-16 text-center">
    <template v-if="somethingWrong">
      <h2 class="mb-4 text-xl font-semibold">
        It seems something has gone wrong while trying to sign in.
      </h2>
      <Button as-child>
        <RouterLink to="/login">Try Again</RouterLink>
      </Button>
    </template>
    <template v-else>
      <h2 class="mb-4 text-xl font-semibold">{{ message }}</h2>
      <LoaderCircle class="size-8 animate-spin text-primary" />
    </template>
  </div>
</template>
