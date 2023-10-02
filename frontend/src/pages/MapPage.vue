<template>
  <q-btn @click="loadData()">Кнопочка</q-btn>
  <q-btn @click="getLocal()">ТКЕТЕТ</q-btn>
  <p>{{ data }}</p>
</template>
<script setup>
import add from "add";
import { apiAxios } from "boot/axios";
import { ref, reactive, onMounted } from "vue";
import { LocalStorage } from "quasar";

function getLocal() {
  // console.log("Token local");
  const myString = LocalStorage.getItem("myString");
  // console.log(myString);
}

const data = ref(null);

function loadData() {
  return apiAxios.get("/api/orders/my/").then((response) => {
    data.value = response.data;
    return data.value;
  });
}
</script>
