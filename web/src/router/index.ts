import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import NotFound from "@/views/NotFound.vue";
import LoginView from "@/views/LoginView.vue";
import { useSessionStore } from "@/stores/session";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView
    },
    {
      path: "/login",
      name: "Login",
      component: LoginView,
      meta: {
        noAuthReq: true
      }
    },
    {
      path: "/app-definition",
      children: [
        {
          path: "list",
          name: "AppDefinitionList",
          component: () => import("@/views/AppDefinitions/ListView.vue")
        },
        {
          path: "create",
          name: "AppDefinitionCreate",
          meta: {
            useShadedBackground: true
          },
          component: () => import("@/views/AppDefinitions/UpdateView.vue")
        },
        {
          path: ":app_definition_id(\\d+)",
          children: [
            {
              name: "AppDefinitionDetail",
              path: "detail",
              meta: {
                useShadedBackground: true
              },
              component: () => import("@/views/AppDefinitions/DetailView.vue")
            },
            {
              path: "update",
              name: "AppDefinitionUpdate",
              meta: {
                useShadedBackground: true
              },
              component: () => import("@/views/AppDefinitions/UpdateView.vue")
            }
          ]
        }
      ]
    },
    {
      path: "/:pathMatch(.*)*",
      name: "notFound",
      component: NotFound
    }
  ]
});

router.beforeEach(async (to) => {
  const sessionStore = useSessionStore();
  await sessionStore.checkSession();

  if (to.meta.noAuthReq) {
    if (to.name === "Login" && sessionStore.currentUser) {
      const redirect = Array.isArray(to.query.redirectUrl)
        ? to.query.redirectUrl[0]
        : to.query.redirectUrl;
      return typeof redirect === "string" && redirect.startsWith("/") ? redirect : "/";
    }
    return true;
  }

  if (!sessionStore.currentUser) {
    return `/login?redirectUrl=${encodeURIComponent(to.fullPath)}`;
  }
});

export default router;
