import { ref } from "vue";
import { defineStore } from "pinia";
import { checkSessionToken, logout as logoutToken } from "@/utils/auth";

export const useSessionStore = defineStore("session", () => {
  const currentUser = ref(null);
  const access_token = ref(null);
  const loading = ref(false);

  async function checkSession() {
    if (loading.value) return;
    loading.value = true;
    const session = await checkSessionToken();

    if (session) {
      currentUser.value = session.user;
      access_token.value = session.access_token;
    } else {
      logout();
    }

    loading.value = false;
  }

  function logout() {
    logoutToken();
    access_token.value = null;
    currentUser.value = null;
  }

  checkSession();
  return { currentUser, checkSession, logout };
});
