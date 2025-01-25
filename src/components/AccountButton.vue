<script setup lang="ts">
import { useSessionStore } from "@/stores/session";
import GoogleLoginButton from "./GoogleLoginButton.vue";

const sessionStore = useSessionStore();

const dialogVisible = ref(false);
const title = computed(() => {
  if (sessionStore.currentUser) return "Account";
  else return "Sign In";
});

function logout() {
  sessionStore.logout();
}
</script>

<template>
  <v-btn variant="text" icon>
    <v-icon icon="mdi-account" />

    <v-dialog v-model="dialogVisible" activator="parent" max-width="300">
      <v-card>
        <v-card-title class="text-center">{{ title }}</v-card-title>
        <v-card-text v-if="sessionStore.currentUser">
          <div class="d-flex flex-column align-center">
            <v-avatar :image="sessionStore.currentUser.avatar_url" size="75" class="mb-2" />
            {{ sessionStore.currentUser.display_name }}
            <v-btn color="primary" class="mt-4" @click="logout">Sign Out</v-btn>
          </div>
        </v-card-text>
        <v-card-text v-else>
          <div class="d-flex justify-center">
            <GoogleLoginButton />
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<style scoped></style>
