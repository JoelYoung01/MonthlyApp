<script setup lang="ts">
import { LoaderCircle } from "@lucide/vue";
import GoogleLoginButton from "@/components/GoogleLoginButton.vue";
import { useSessionStore } from "@/stores/session";
import { useRoute, useRouter } from "vue-router";

const sessionStore = useSessionStore();
const router = useRouter();
const route = useRoute();

watch(
  () => sessionStore.currentUser,
  (value) => {
    if (!value) return;

    const redirect = Array.isArray(route.query.redirectUrl)
      ? route.query.redirectUrl[0]
      : route.query.redirectUrl;
    if (typeof redirect === "string" && redirect.startsWith("/")) {
      router.push(redirect);
    } else {
      router.push("/");
    }
  },
  {
    immediate: true
  }
);
</script>

<template>
  <div class="mx-auto flex w-full max-w-md flex-col items-center px-4 py-16">
    <template v-if="sessionStore.loading">
      <h2 class="mb-4 text-center text-xl font-semibold">Checking your session...</h2>
      <LoaderCircle class="size-8 animate-spin text-primary" />
    </template>
    <div v-else class="flex flex-col items-center gap-4">
      <h2 class="text-xl font-semibold">Sign in to continue</h2>
      <GoogleLoginButton />
    </div>
  </div>
</template>
