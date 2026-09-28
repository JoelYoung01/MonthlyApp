import { loginWithGoogle } from "@/utils";
import type { InjectionKey, Ref } from "vue";

export const googleAccountsLoadedKey = Symbol() as InjectionKey<Ref<boolean>>;

/**
 * Docs for js API:
 * https://developers.google.com/identity/gsi/web/reference/js-reference
 */
export function install(app: any) {
  const loaded = ref(false);
  app.provide(googleAccountsLoadedKey, loaded);

  // @ts-expect-error This exists, trust me bro (https://developers.google.com/identity/gsi/web/reference/js-reference#onGoogleLibraryLoad)
  window.onGoogleLibraryLoad = () => {
    google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      auto_select: false,
      callback: loginWithGoogle
    });

    loaded.value = true;
  };

  setTimeout(() => {
    if (!loaded.value) {
      console.error(
        "Google Library is still not loaded after 5 seconds, something is probably wrong. Did you add the cdn script?"
      );
    }
  }, 5000);
}
