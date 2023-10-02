import { boot } from "quasar/wrappers";
import axios from "axios";

import { LocalStorage } from "quasar";
// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const apiAxios = axios.create({
  // baseURL: "https://jsonplaceholder.typicode.com",
  // baseURL: "https://webhook.site/611514f4-8c39-4921-ad13-859eab9f65fc",
  // baseURL: "https://jsonplaceholder.typicode.com",
  baseURL: "",
});

if (localStorage.getItem("myString")) {
  apiAxios.interceptors.request.use(
    (config) => {
      const myString = LocalStorage.getItem("myString");
      if (myString) {
        config.headers["Authorization"] = `Token ${myString}`;
        // console.log("token ok");
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
      // console.log("token err");
    }
  );
}

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$apiAxios = apiAxios;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { apiAxios };
