<script setup lang="ts">
import { useSessionStore } from "@/stores/session";
import { useRouter } from "vue-router";

const sessionStore = useSessionStore();
const router = useRouter();

const dialogVisible = ref(false);

function logout() {
  sessionStore.logout();
  dialogVisible.value = false;
  router.push("/login");
}
</script>

<template>
  <v-btn v-if="sessionStore.currentUser" variant="text" icon>
    <v-avatar>
      <v-img alt="Profile Image" :src="sessionStore.currentUser.avatar_url">
        <template #placeholder>
          <v-icon class="text-white h-100" icon="mdi-account" size="large" />
        </template>
      </v-img>
    </v-avatar>

    <v-dialog v-model="dialogVisible" activator="parent" max-width="300">
      <v-card>
        <v-card-title class="text-center">Account</v-card-title>
        <v-card-text>
          <div class="d-flex flex-column align-center">
            <v-avatar size="75" class="mb-2">
              <v-img alt="Profile Image" :src="sessionStore.currentUser.avatar_url">
                <template #placeholder>
                  <v-icon icon="mdi-account-circle" size="75" />
                </template>
              </v-img>
            </v-avatar>
            {{ sessionStore.currentUser.display_name }}
            <v-btn color="primary" class="mt-4" @click="logout">Sign Out</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<style scoped></style>
