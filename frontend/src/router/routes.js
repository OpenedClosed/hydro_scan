const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/IndexPage.vue") }],
  },
  {
    path: "/dashboard",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/DashboardPage.vue") },
    ],
  },

  {
    path: "/order",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/OrderPage.vue") }],
  },
  {
    path: "/change-order",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/ChangeOrderPage.vue") }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
  {
    path: "/auth",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/auth/LoginSection.vue"),
      },
      {
        path: "register",
        component: () => import("pages/auth/RegisterSection.vue"),
      },
    ],
  },
];

export default routes;
