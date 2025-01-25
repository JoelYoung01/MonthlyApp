export const TOKEN_STORAGE_KEY = "access_token";

export async function checkSessionToken() {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/auth/verify-session/?access_token=${token}`
      );
      if (!response.ok) throw new Error("Recieved Non-200 response code while verifying session");
      return await response.json();
    } catch (er) {
      logout();
    }
  }
}

export async function loginWithGoogle(payload: any) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/login-google/`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload)
    });
    const { access_token } = await response.json();

    localStorage.setItem(TOKEN_STORAGE_KEY, access_token);
  } catch (er) {
    console.error(er);
  }
}

export function logout() {
  //   localStorage.removeItem(TOKEN_STORAGE_KEY);
}
