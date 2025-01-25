import { ref } from "vue";
import { defineStore } from "pinia";

const TOKEN_STORAGE_KEY = "access_token";

export const useSessionStore = defineStore("session", () => {
  const currentUser = ref(null);
  const access_token = ref(null);
  const loading = ref(false);

  async function checkSession() {
    if (loading.value) return;
    loading.value = true;
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/auth/verify-session/?access_token=${token}`
        );
        if (!response.ok) throw new Error("Recieved Non-200 response code while verifying session");
        const { user, access_token } = await response.json();
        currentUser.value = user;
        access_token.value = access_token;
      } catch (er) {
        logout();
      }
    }
    loading.value = false;
  }

  async function loginWithGoogle(payload: any) {
    if (loading.value) return;
    loading.value = true;
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/login-google/`, {
        method: "POST",
        body: JSON.stringify(payload)
      });
      const { user, access_token } = await response.json();

      localStorage.setItem(TOKEN_STORAGE_KEY, access_token);
      currentUser.value = user;
      access_token.value = access_token;
    } catch (er) {
      console.error(er);
      logout();
    }
    loading.value = false;
  }

  function logout() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    access_token.value = null;
    currentUser.value = null;
  }

  checkSession();
  return { currentUser, checkSession, loginWithGoogle, logout };
});
