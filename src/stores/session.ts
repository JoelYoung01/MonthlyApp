import { ref } from "vue";
import { defineStore } from "pinia";

export const useSessionStore = defineStore("session", () => {
  const currentUser = ref(null);

  async function loginWithGoogle(payload: any) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/login-google/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
    currentUser.value = await response.json();
  }

  async function logout() {
    //
  }

  return { currentUser, loginWithGoogle, logout };
});
