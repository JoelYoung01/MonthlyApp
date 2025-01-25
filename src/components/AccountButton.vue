<script setup lang="ts">
import GoogleLoginButton from "./GoogleLoginButton.vue";

const dialogVisible = ref(false);
const view = ref<"signin" | "signup" | "account">("signin");
const title = computed(() => {
  if (view.value === "signin") return "Sign In";
  else if (view.value === "signup") return "Sign Up";
  else return "Account";
});

function logout() {
  google.accounts.id.revoke("joeleyoung01@gmail.com");
}
</script>

<template>
  <v-btn variant="text" icon>
    <v-icon icon="mdi-account" />

    <v-dialog v-model="dialogVisible" activator="parent" max-width="300">
      <v-card>
        <v-card-title class="text-center">{{ title }}</v-card-title>
        <v-card-text v-if="view === 'signup'">
          <div class="d-flex justify-center">
            <GoogleLoginButton view="signup" />
          </div>
        </v-card-text>
        <v-card-text v-else-if="view === 'signin'">
          <div class="d-flex justify-center">
            <GoogleLoginButton view="signin" />
          </div>
        </v-card-text>
        <v-card-text v-else-if="view === 'account'">
          <div class="d-flex justify-center">
            <v-btn color="primary" @click="logout">Sign Out</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<style scoped></style>
