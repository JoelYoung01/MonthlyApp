<script setup lang="ts">
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
  <template v-if="sessionStore.loading">
    <h2 class="mt-5 text-center">Checking your session...</h2>
    <div class="d-flex justify-center mt-3">
      <v-progress-circular color="primary" indeterminate />
    </div>
  </template>
  <div v-else class="d-flex flex-column align-center mt-10 ga-4">
    <h2>Sign in to continue</h2>
    <GoogleLoginButton />
  </div>
</template>

<style scoped></style>
