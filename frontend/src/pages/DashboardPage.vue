<template>
  <q-page padding id="Dashboard">
    <q-dialog v-model="showPopup">
      <q-card>
        <q-card-section>
          <p>Заказ уже находится в исполнении, редактирование запрещено</p>
        </q-card-section>
      </q-card>
    </q-dialog>

    <div class="example-column-equal-width">
      <div class="column columnHeight">
        <div class="row">
          <div class="col-3 q-px-md backgroundStyle radius">
            <div class="col-auto">
              <q-scroll-area class="row-9 q-ma-md scrollArea">
                <div class="q-ma-md">
                  <q-btn class="q-my-sm order_button" v-for="button in buttons" :key="button.label" :label="button.label"
                    @click="button.onClick" />
                </div>
              </q-scroll-area>

              <div class="row-3 createButtons">
                <q-btn to="/order" class="settingsButton">Создать заказ</q-btn>

                <q-btn flat class="q-my-sm settingsButtonFlat" @click="sendChangeData()">Настройки</q-btn>
                <q-btn flat class="q-my-sm settingsButtonFlat" href="https://t.me/vladushked">Служба поддержки</q-btn>
              </div>
            </div>
          </div>

          <div class="col-9 q-px-xl backgroundStyle radius" v-if="showContent">
            <div class="row q-pt-md center">
              <div class="col-3">
                <q-btn class="orderSettings">
                  <q-icon name="radio_button_checked" :color="statusColor"></q-icon>
                  <div class="q-mx-sm">{{ statusText }}</div>
                </q-btn>
              </div>
              <div class="col-3">
                <q-btn @click="rickRoll()" icon="download" class="orderSettings">
                  <div class="q-mx-sm">Скачать отчёт</div>
                </q-btn>
              </div>
              <div class="col-3">
                <q-btn @click="downloadFileModel()" class="orderSettings" icon="view_in_ar">
                  <div class="q-mx-sm">Скачать 3D модель</div>
                </q-btn>
              </div>
              <div class="col-3">
                <q-btn icon="currency_ruble" class="orderSettings">
                  <div class="q-mx-sm">Цена: {{ priceContent }}</div>
                </q-btn>
              </div>
            </div>

            <div class="modelStyle q-pa-md">
              <model-ply class="modelStyle" :src="modelContent" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ModelPly } from "vue-3d-model";
import { ref, reactive, onMounted } from "vue";
import { getOrdersTEST } from "src/Common/api/todos";
import { apiAxios } from "boot/axios";
import { useQuasar } from "quasar";
import { useRouter } from "vue-router";
import { openURL } from "quasar";
import axios from "axios";

const router = useRouter();

const myData = ref([]);
const buttons = reactive([]);

const showContent = ref(false);
const showPopup = ref(false);
const modelContent = ref("");
const priceContent = ref("");
const statusText = ref("");
const statusColor = ref("");
const linkToModel = ref("");
const orderID = ref("");
const orderStatusRef = ref("");

// load data
const $q = useQuasar();
const data = ref(null);

function loadData() {
  return apiAxios.get("/api/orders/my/").then((response) => {
    data.value = response.data;
    return data.value;
  });
}

function sendChangeData() {
  if (orderID.value) {
    if (orderStatusRef.value !== "created") {
      showPopup.value = true
    } else {
      router.push({ path: '/change-order', query: { data: orderID.value } })
    }
  }
}

function goToLinkFile(response) {
  const url = window.URL.createObjectURL(response.data);
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = url;

  // Имя файла для загрузки
  let file_name = response.headers.get("Content-Disposition")
  file_name = file_name.split('filename=')[1]
  file_name = file_name.split(';')[0];
  file_name = file_name.replace(/"/g, '')
  a.download = file_name
  // Ссылка для загрузки
  document.body.appendChild(a);
  a.click();

  // Удаляем использованный url и ссылку
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

function setURLFileModel() {
  apiAxios({
    method: "get",
    url: `/api/orders/${orderID.value}/download_3d_model/`,
    responseType: "blob",
  })
    .then((response) => {
      const url = window.URL.createObjectURL(response.data);
      window.URL.revokeObjectURL(modelContent.value);
      modelContent.value = url
    })
    .catch((err) => {
    });
  // openURL(linkToModel.value);
}


function downloadFileModel() {
  apiAxios({
    method: "get",
    url: `/api/orders/${orderID.value}/download_3d_model/`,
    responseType: "blob",
  })
    .then((response) => {
      goToLinkFile(response)
    })
    .catch((err) => {
      openURL("404")
    });
}

function rickRoll() {
  apiAxios({
    method: "get",
    url: `/api/orders/${orderID.value}/download_report/`,
    responseType: "blob",
  })
    .then((response) => {
      goToLinkFile(response)
    })
    .catch((err) => {
      openURL("404")
    });
}

onMounted(async () => {
  const response = await loadData();
  myData.value = response;
  const numButtons = myData.value.length;

  // console.log(myData.value);
  // console.log(numButtons);

  for (let i = 0; i < numButtons; i++) {
    buttons.push({
      label: `Заказ ${i + 1}: ${myData.value[i].name}`,
      onClick: () => {
        // console.log(`Button ${i + 1} clicked`);
        // modelContent.value = myData.value[i].model;
        showContent.value = true;
        priceContent.value = myData.value[i].price;
        linkToModel.value = myData.value[i].model;
        orderID.value = myData.value[i].id;
        setURLFileModel()
        const order_status = myData.value[i].status;
        orderStatusRef.value = myData.value[i].status;
        if (order_status === "created") {
          statusText.value = "Создан";
          statusColor.value = "grey";
        } else if (order_status === "in_process") {
          statusText.value = "В процессе";
          statusColor.value = "orange";
        } else if (order_status === "completed") {
          statusText.value = "Выполнен";
          statusColor.value = "green";
        } else if (order_status === "canceled") {
          statusText.value = "Отменён";
          statusColor.value = "red";
        }
      },
    });
  }
});
</script>

<style lang="scss">
#Dashboard {
  .backgroundStyle {
    background-color: #dce9f5;
    outline-style: solid;
    outline-width: 10px;
    outline-color: white;
  }

  .order_button {
    width: 100%;
    border-radius: 20px;
    min-height: 60px;
  }

  .backgroundStyleD {
    background-color: #8fabc6;
  }

  .settingsButton {
    width: 100%;
    border-radius: 20px;
    min-height: 54px;
  }

  .orderSettings {
    border-radius: 20px;
    min-height: 44;
    width: 95%;
  }

  .settingsButtonFlat {
    width: 100%;
    border-radius: 20px;
    min-height: 36px;
  }

  .scrollArea {
    height: 440px;
  }

  .modelStyle {
    max-height: 60%;
    margin: 5px 5px 5px 5px;
  }

  .columnHeight {
    height: 200px;
  }

  .center {
    margin: auto;
    width: 80%;
  }

  .createButtons {
    margin-top: 35%;
  }
}
</style>
