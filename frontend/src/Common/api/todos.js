import { apiAxios } from "boot/axios";


export function todoList() {
  return apiAxios.get("/todos");
}
export function sendInformation(data) {
  return apiAxios.post("/form", data);
}

export function sendOrder(data) {
  return apiAxios.post("/api/orders/", data);
}
export function sendInfoForPrice(data) {
  return apiAxios.post("/1/price-calculation", data);
}
export function sendLoginInfo(data) {
  return apiAxios.post("/api/auth/token/login/", data);
}
// Вот этим мы отправляем инфу для регистрации
export function sendRegistrationInfo(data) {
  return apiAxios.post("/api/users/", data);
}

export function getOrders(id) {
  return apiAxios.get(`/${id}/all-orders`);
}
export function getOrdersTEST(id) {
  return apiAxios.get(`/posts`)
  .then((response) => {
    data.value = response.data
  });
}
export function getCalculatedPrice(id) {
  return apiAxios.get(`/1/price-calculation`);
}
export function getInfpAboutOrder(id) {
  return apiAxios.get(`/1/{order_id}/get-info`);
}
export function getLoginConfirmation(id) {
  return apiAxios.get(`/login/confirmation`);
}
export function getRegistrationConfirmation(id) {
  return apiAxios.get(`/register/confirmation`);
}

export function todoItem(id) {
  return apiAxios.get(`/todos/${id}`);
}
