import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import NotFound from "@/views/NotFound.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
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

export default router;
