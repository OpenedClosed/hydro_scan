<template>
  <q-layout id="mainLayout" view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="bg-background_color">
        <div
          @click="goIndex()"
          flat
          style="padding: 0; border: 0"
          class="q-ma-md q-gutter-sm logoStyle"
        >
          <img src="~assets/logo.png" style="max-height: 25px" />
        </div>

        <q-tabs outside-arrows mobile-arrows class="tabStyle" allign="left">
          <q-route-tab to="/" label="Главная" />
          <q-route-tab @click="checkLoginDashboard()" label="Личный кабинет" />
          <!-- <q-route-tab class="text-strike" to="" label="Проекты" />
          <q-route-tab class="text-strike" to="" label="О нас" />
          <q-route-tab class="text-strike" @click="goTeam()" label="Команда" />
          <q-route-tab class="text-strike" label="Контакты" /> -->
        </q-tabs>
        <div class="q-px-md buttonsMargin">
          <q-btn class="layoutButtonWide" @click="checkLogin()"
            >Оставить заявку</q-btn
          >
        </div>
        <div class="q-px-md">
          <q-btn @click="authAction()" class="layoutButton">{{
            buttonText
          }}</q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
    <q-footer elevated>
      <q-toolbar>
        <q-toolbar-title>Hydroscan</q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { EventBus, LocalStorage } from "quasar";
import { useRouter } from "vue-router";
import { defineComponent } from "vue";

const router = useRouter();
const buttonText = ref("");
function goTeam() {
  router.push("/").then(() => {
    $refs.teamRef.scrollIntoView({ behavior: "smooth" });
  });
}
function goIndex() {
  router.push({ path: "/" });
}
function authAction() {
  if (buttonText.value === "Выйти") {
    LocalStorage.remove("myString");
    checkButtons();
    router.push("/").then(() => {
      window.location.reload();
    });
  } else {
    router.push({ path: "/auth" });
  }
}
function checkLogin() {
  const token = LocalStorage.getItem("myString");
  if (token) {
    router.push({ path: "/order" });
  } else {
    router.push({ path: "/auth" });
  }
}
function checkLoginDashboard() {
  const token = LocalStorage.getItem("myString");
  if (token) {
    router.push({ path: "/dashboard" });
  } else {
    router.push({ path: "/auth" });
  }
}

function checkButtons() {
  const token = LocalStorage.getItem("myString");
  if (token) {
    buttonText.value = "Выйти";
  } else {
    buttonText.value = "Войти";
  }
}

onMounted(() => {
  checkButtons();
});
</script>

<style lang="scss">
#mainLayout {
  .layoutButton {
    border-radius: 20px;
    max-height: 52px;
  }
  .layoutButtonWide {
    border-radius: 20px;
    max-height: 52px;
    min-width: 200px;
  }
  .logoStyle {
    cursor: pointer;
  }
  .buttonsStyle {
    width: 160px;
  }

  .tabStyle {
    width: 90%;
    padding-right: auto;
    padding-left: auto;
  }
}
</style>
