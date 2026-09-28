import { ref } from "vue";
import { defineStore } from "pinia";
import { AuthLoginEvent, checkSessionToken } from "@/utils";

export const TOKEN_STORAGE_KEY = "access_token";

interface CurrentUser {
  id: number;
  username: string;
  email: string;
  display_name: string;
  admin: boolean;
  disabled: boolean;
  avatar_url?: string;
}

export const useSessionStore = defineStore("session", () => {
  const access_token = ref<string | null>(localStorage.getItem(TOKEN_STORAGE_KEY));
  const currentUser = ref<CurrentUser | null>(null);
  const loading = ref(true);

  let checkPromise: Promise<void> | null = null;

  async function checkSession() {
    if (checkPromise) return checkPromise;

    checkPromise = (async () => {
      loading.value = true;
      access_token.value = localStorage.getItem(TOKEN_STORAGE_KEY);

      if (access_token.value === null) {
        logout();
        loading.value = false;
        return;
      }

      const session = await checkSessionToken(access_token.value);

      if (session) {
        currentUser.value = session.user;
        access_token.value = session.access_token;
      } else {
        logout();
      }

      loading.value = false;
    })();

    return checkPromise;
  }

  function logout() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    access_token.value = null;
    currentUser.value = null;
    checkPromise = null;
  }

  window.addEventListener(AuthLoginEvent, ((event: CustomEvent) => {
    localStorage.setItem(TOKEN_STORAGE_KEY, event.detail.access_token);
    access_token.value = event.detail.access_token;
    currentUser.value = event.detail.user;
    loading.value = false;
  }) as EventListener);

  checkSession();

  return { currentUser, loading, checkSession, logout };
});
