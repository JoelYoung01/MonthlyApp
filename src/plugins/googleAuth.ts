import type { InjectionKey, Reactive } from "vue";

type CredResponseHandler = (response: google.accounts.id.CredentialResponse) => void;

interface AccountsConfig {
  loaded: boolean;
  credResponseHandler: CredResponseHandler;
}

export const googleAccountsConfigKey = Symbol() as InjectionKey<Reactive<AccountsConfig>>;

const defaultOptions = {
  prompt: true as boolean
};

/**
 * Docs for js API:
 * https://developers.google.com/identity/gsi/web/reference/js-reference
 */
export function install(app: any, options = defaultOptions) {
  const config = reactive({
    loaded: false,
    credResponseHandler: () => {
      console.debug("Login Attempted");
    }
  });
  app.provide(googleAccountsConfigKey, config);

  // @ts-expect-error This exists, trust me bro (https://developers.google.com/identity/gsi/web/reference/js-reference#onGoogleLibraryLoad)
  window.onGoogleLibraryLoad = () => {
    google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      auto_select: true,
      callback: config.credResponseHandler,
      login_uri: import.meta.env.VITE_GOOGLE_REDIRECT_URL,
      use_fedcm_for_prompt: true
    });

    config.loaded = true;

    if (options.prompt) {
      google.accounts.id.prompt();
    }
  };

  setTimeout(() => {
    if (!config.loaded) {
      console.error(
        "Google Library is still not loaded after 5 seconds, something is probably wrong. Did you add the cdn script?"
      );
    }
  }, 5000);
}
