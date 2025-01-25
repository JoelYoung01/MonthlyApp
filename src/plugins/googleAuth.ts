import type { InjectionKey, Ref } from "vue";

export const googleAccountsLoadedKey = Symbol() as InjectionKey<Ref<boolean>>;

function handleCredentialResponse(response: google.accounts.id.CredentialResponse) {
  console.debug(response);
}

/**
 * Docs for js API:
 * https://developers.google.com/identity/gsi/web/reference/js-reference
 */
export function install(app: any) {
  const loaded = ref(false);
  app.provide(googleAccountsLoadedKey, loaded);
  const checkGoogleAccounts = setInterval(() => {
    if (typeof google !== "undefined" && google?.accounts?.id) {
      clearInterval(checkGoogleAccounts);

      google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        auto_select: true,
        callback: handleCredentialResponse,
        login_uri: import.meta.env.VITE_GOOGLE_REDIRECT_URL,
        use_fedcm_for_prompt: true
      });

      loaded.value = true;
    }
  }, 100);

  setTimeout(() => {
    clearInterval(checkGoogleAccounts);
    new Error("Timeout: google.accounts.id is not defined after 5 seconds.");
  }, 5000);
}
