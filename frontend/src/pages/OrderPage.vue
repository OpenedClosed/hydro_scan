<template>
  <q-page padding id="orderPage">
    <q-form @submit="sendComponentData()">
      <div class="q-pa-xl backgroundStyle">
        <div class="q-mb-md">
          <h3>Создание заказа</h3>
        </div>


        <q-dialog v-model="showPopup">
          <q-card>
            <q-card-section>

              <p>Ошибка: {{errorMessgage}}</p>
            </q-card-section>
          </q-card>
        </q-dialog>

        <div class="q-my-md">
          <h5>Название заказа:</h5>
          <q-input
            outlined
            type="text"
            v-model="name_text"
            :rules="[(val) => !!val || 'Введите название заказа!']"
          ></q-input>
        </div>

        <div class="q-my-md">
          <h5>Выберите услуги:</h5>
        </div>

        <div class="q-my-md">
          <q-option-group
            :options="service_options"
            type="radio"
            v-model="service_group"
          />
        </div>

        <div class="q-my-md">
          <h5>Укажите местоположение объекта:</h5>
          <div id="map" class="mapStyle"></div>
        </div>

        <div class="q-my-md">
          <h5>Выберите характеристики объекта:</h5>
          <q-option-group
            :options="characteristics_options"
            type="checkbox"
            v-model="characteristics_group"
          />
          <!-- <q-input
            outlined
            type="text"
            v-model="optinal_characteristics_text"
          ></q-input> -->
        </div>

        <div class="q-my-md">
          <h5>Площадь обследования:</h5>
          <q-input
            outlined
            type="number"
            v-model="surface_of_research_text"
            label="кв.м."
            :rules="[(val) => !!val || 'Введите площадь обследования!']"
          ></q-input>
        </div>

        <div class="q-my-md">
          <h5>Мутность воды:</h5>
          <q-input
            outlined
            type="number"
            v-model="water_turbidity_text"
            label="метр(-ов) видимости"
            :rules="[(val) => !!val || 'Введите мутность воды!']"
          ></q-input>
        </div>

        <div class="q-my-md">
          <h5>Скорость течения в области исследования:</h5>
          <q-input
            outlined
            type="number"
            v-model="flow_text"
            label="м/с"
            :rules="[(val) => !!val || 'Введите скорость течения!']"
          ></q-input>
        </div>

        <div class="q-my-md">
          <h5>Выберите характеристики дна:</h5>
          <q-option-group
            :options="bottom_options"
            type="checkbox"
            v-model="bottom_group"
          />
          <!-- <q-input outlined v-model="bottom_optional_selection_text"></q-input> -->
        </div>

        <div class="q-my-md">
          <h5>Желаемые сроки проведения:</h5>
          <p>{{ deadline_date }}</p>
          <div class="q-pa-md">
            <q-date v-model="deadline_date" landscape mask="YYYY-MM-DD" />
          </div>
        </div>

        <!-- <div class="q-my-md">
          <h5>Количество объектов:</h5>
          <q-input
            outlined
            type="number"
            v-model="quantity_text"
            label="шт."
            :rules="[(val) => !!val || 'Введите количество объектов!']"
          ></q-input>
        </div> -->

        <div class="q-my-md">
          <h5>Дополнительное описание объекта(-ов):</h5>
          <q-input
            outlined
            v-model="additional_description_text"
            :rules="[(val) => !!val || 'Введите дополнительное описание!']"
          ></q-input>
        </div>
        <div>
          <q-btn @click="showPrice()" class="q-my-md"
            >Рассчитать примерную стоимость</q-btn
          >
        </div>
        <div v-if="showContent">
          <h5>Примерная стоимость:</h5>
          <h3>~ {{ priceDisplay }} руб.</h3>
        </div>
        <div>
          <q-btn type="submit">Оформить заказ</q-btn>
        </div>
      </div>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import { apiAxios } from "boot/axios";
import { useRouter } from "vue-router";
import { debounce } from "quasar";
import { onMounted } from "vue";
import L, { latLng, marker } from "leaflet";

import "leaflet/dist/leaflet.css";
import { date } from "quasar";
import { Dialog } from 'quasar'


const router = useRouter();
const optinal_characteristics_text = ref("");
const surface_of_research_text = ref("");
const water_turbidity_text = ref("");
const flow_text = ref("");
const deadline_date = ref(date.formatDate(Date.now(), "YYYY-MM-DD"));
const quantity_text = ref("");
const additional_description_text = ref("");
const bottom_optional_selection_text = ref("");
const name_text = ref("");
const priceDisplay = ref("");
const errorMessgage = ref("");
const showPopup = ref(false);
const showContent = ref(false);


const service_group = ref("underwater");
const characteristics_group = ref(["pier"]);
const bottom_group = ref(["muddy"]);
var latitude = 0.0;
var longitude = 0.0;


function checkOrder(){
  var date1 = date.formatDate(Date.now(), "YYYY-MM-DD")
  var date2 = date.formatDate(deadline_date.value, "YYYY-MM-DD")
  const diffInDays = date.getDateDiff(date2, date1, 'days')

  if(name_text.value === "" || surface_of_research_text.value === "" || water_turbidity_text.value === "" || flow_text.value === "" || additional_description_text.value === "" ){
    errorMessgage.value = "Вы не заполнили форму до конца"
    showPopup.value = true
    return false
  }
  if (latitude === 0.0 || longitude === 0.0){
    errorMessgage.value = "Выберите точку на карте"
    showPopup.value = true
    return false
  }
  if (characteristics_group.value.length === 0){
    errorMessgage.value = "Характеристики объекта выбраны некорректно"
    showPopup.value = true
    return false
  }
  if (bottom_group.value.length === 0 ){
    errorMessgage.value = "Характеристики дна выбраны некорректно"
    showPopup.value = true
    return false
  }
  if (diffInDays <= 0   && bottom_group.value){
    errorMessgage.value = "Дата введена некорректно"
    showPopup.value = true
    return false
  }
  return true
}

function initiateData() {


  const data = {
    characteristic_group: characteristics_group.value,
    bottom_group: bottom_group.value,
    name: name_text.value,
    service_group: service_group.value,
    map_latitude: latitude,
    map_longitude: longitude,
    research_surface: surface_of_research_text.value,
    water_turbidity: water_turbidity_text.value,
    flow: flow_text.value,
    deadline: deadline_date.value + "T00:00:00+03:00",
    additional_description: additional_description_text.value,
    status: "created",
    // model: "tinker.ply", // Не нужно так как в backend ставиться модель по умолчанию
    // name: "Офигенное обследование",
    // author: "Вася Пупкин",
    // id: 1,
    // service_group: service_group.value,
    // map_latitude: latitude,
    // map_longitude: longitude,
    // characteristics_group: characteristics_group.value,
    // object_optional_selection_text: optinal_characteristics_text.value,
    // research_surface: surface_of_research_text.value,
    // water_turbidity: water_turbidity_text.value,
    // flow: flow_text.value,
    // bottom_group: bottom_group.value,
    // bottom_optional_selection_text: bottom_optional_selection_text.value,
    // deadline: deadline_date.value,
    // created: date.formatDate(Date.now(), "YYYY/MM/DD"),
    // quantity: quantity_text.value,
    // additional_description: additional_description_text.value,
    // cost: "222",
  };
  return data;
}


function initializeMapAndLocator() {
  var map = L.map("map", {
    attributionControl: false,
    doubleClickZoom: false,
  });

  L.tileLayer(
    "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      maxZoom: 19,
      attributionControl:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      id: "streets-v12",
      accessToken:
        "pk.eyJ1IjoiYm9id2F0Y2hlcngiLCJhIjoiY2xiMGwwZThrMWg3aTNwcW1mOGRucHh6bSJ9.kNHlmRqkRSxYNeipcKkJhw",
    }
  ).addTo(map);

  const customIcon = L.icon({
    iconUrl: "pin.png",
    iconSize: [64, 64],
    iconAnchor: [32, 64],
    popupAnchor: [-3, -76],
  });

  var marker;

  map.on("dblclick", (event) => {
    if (marker) {
      marker.remove();
    }
    marker = L.marker(event.latlng, { icon: customIcon }).addTo(map);

    const latlng = marker.getLatLng();
    // console.log(latlng.lat, latlng.lng);
    latitude = latlng.lat;
    longitude = latlng.lng;
  });
  // map.on("dblclick", (event) => {
  //   const marker = L.marker(event.latlng).addTo(map);
  //   markers.push(marker);
  //   console.log(markers);

  // });

  map.locate({ setView: true, maxZoom: 40, watch: true, timeout: 60000 });

  // function onLocationFound(e) {
  //   console.log(e.latlng)
  //   var radius = e.acuracy / 2;
  //   L.marker(e.latlng).addTo(map)
  //   .bindPopup("You are within " + radius + " meters from this point").openPopup();
  //   L.circle(e.latlng, radius).addTo(map);
  //   }

  // map.on('locationfound', onLocationFound);

  //   L.Control.Search({
  //   url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
  //   jsonpParam: 'json_callback',
  //   propertyName: 'display_name',
  //   propertyLoc: ['lat','lon'],
  //   marker: L.circleMarker([0,0],{radius:30}),
  //   autoCollapse: true,
  //   autoType: false,
  //   minLength: 2
  // }).addTo(map);
}

onMounted(() => {
  initializeMapAndLocator();
});

function showPrice() {
  if (checkOrder()){
    const data = initiateData();
    apiAxios.post("/api/orders/price_count/", data).then((response) => {
      priceDisplay.value = response.data.price;
      showContent.value = true;
    });
  }
}


function sendOrder(data) {
  apiAxios.post("/api/orders/", data).then(
    router.push("/dashboard").then(() => {
      window.location.reload();
    })
  );
}

function sendComponentData() {
  if (checkOrder()){
    const data = initiateData();
    // console.log(JSON.stringify(data));
    sendOrder(data);
  }
}

const service_options = [
  { label: "Осмотр подводной части объека", value: "underwater" },
  { label: "Осмотр надводной части объека", value: "surface" },
  { label: "Создание 3D-модели объекта", value: "3d-model" },
  { label: "Составление отчета об осмотре", value: "report" },
  { label: "Автоматический поиск дефектов", value: "defects" },
  { label: "Создание отчета о дефектах", value: "deffects-report" },
];
const characteristics_options = [
  { label: "Пирс", value: "pier" },
  { label: "Причал", value: "big_pier" },
  { label: "Опоры мостов", value: "brige_supports" },
  { label: "Корабль", value: "ship" },
  { label: "Баржа", value: "barge" },
  { label: "Катер", value: "boat" },
  { label: "Другое", value: "another" },
];
const bottom_options = [
  { label: "Илистое", value: "muddy" },
  { label: "Щебень", value: "gravel" },
  { label: "Песок", value: "sand" },
  { label: "Другое", value: "another" },
];
</script>

<style lang="scss">
#orderPage {
  .mapStyle {
    width: 100%;
    height: 500px;
    z-index: 1;
  }
  .backgroundStyle {
    background-color: #dce9f5;
  }
}
</style>
