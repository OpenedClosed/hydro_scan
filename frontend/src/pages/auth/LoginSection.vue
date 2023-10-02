<template>
  <q-page id="loginPage">
    <q-toolbar class="text-white bg-primary">
      <q-toolbar-title> Вход </q-toolbar-title>
    </q-toolbar>

    <q-scroll-area class="form-style">
      <div class="q-pa-md q-gutter-md">
        <!-- <div class="text-center">Register and get extra features!</div> -->

        <q-input
          type="email"
          v-model="email"
          :error="hasErrorEmail"
          :error-message="errorEmail"
          outlined
          stack-label
          label="E-mail"
        >
          <template v-slot:append>
            <!-- <q-icon name="close"></q-icon> -->
          </template>
        </q-input>
        <q-input
          :type="isPwd ? 'password' : 'text'"
          v-model="password"
          :error="hasErrorPassword"
          :error-message="errorPassword"
          outlined
          stack-label
          label="Пароль"
        >
          <template v-slot:append>
            <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
            />
          </template>
        </q-input>



        <q-dialog v-model="showPopup">
          <q-card>
            <q-card-section>
              <div v-for="(value, key) in errorMessage.value" :key="key">
                {{ key }}: {{ value }}
              </div>
            </q-card-section>
          </q-card>
        </q-dialog>

        <div>
          <q-btn
            @click="sendComponentData()"
            color="black"
            label="Войти"
            size="lg"
            class="full-width"
          ></q-btn>
          <div class="q-px-md q-mt-xl text-center">
            <div class="q-mb-md no-account">У вас ещё нет аккаунта?</div>
            <q-btn to="/auth/register" color="primary" outline rounded
              >Зарегистрируйтесь здесь!</q-btn
            >
          </div>
        </div>
      </div>
    </q-scroll-area>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { apiAxios } from "boot/axios";
import { LocalStorage } from "quasar";

import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { defineComponent } from "vue";

const $q = useQuasar();

const router = useRouter();

const password = ref("");
const email = ref("");
const tokenData = ref("");
const errorMessage = ref("");
const errorEmail = ref("");
const errorPassword = ref("");
const showPopup = ref(false);
const hasErrorEmail = ref(false);
const hasErrorPassword = ref(false);
const isPwd = ref(true);

function sendLoginInfo(data) {
  return apiAxios.post("/api/auth/token/login/", data).then((response) => {
    tokenData.value = response.data;
    return tokenData.value;
  });
}

function sendComponentData() {
  const data = {
    password: password.value,
    email: email.value,
  };
  apiAxios
    .post("/api/auth/token/login/", data)
    .then((response) => {
      tokenData.value = response.data.auth_token;
      LocalStorage.set("myString", tokenData.value);

      router.push("/dashboard").then(() => {
        window.location.reload();
      });
    })
    .catch((err) => {
      if (err.response) {
        // The client was given an error response (5xx, 4xx)
        // console.log(err.response.data);
        // console.log(err.response.status);
        // console.log(err.response.headers);
        errorMessage.value = err.response.data;

        errorEmail.value = "";
        errorPassword.value = "";
        hasErrorEmail.value = false;
        hasErrorPassword.value = false;

        if (err.response.data["detail"] === "Страница не найдена.") {
          hasErrorEmail.value = true;
          errorEmail.value = "Вы не зарегистрированы";
        }
        if (errorMessage.value.email) {
          hasErrorEmail.value = true;
          errorEmail.value = errorMessage.value.email[0];
        }
        if (errorMessage.value.password) {
          hasErrorPassword.value = true;
          if (typeof errorMessage.value.password === "string") {
            errorPassword.value = errorMessage.value.password;
          } else {
            errorPassword.value = errorMessage.value.password[0];
          }
        }

        // showPopup.value = true;
      } else if (err.request) {
        // The client never received a response, and the request was never left
      } else {
      }
    });
}

// console.log(tokenData.value)
// if (typeof tokenData.value !== 'string') {
//   showPopup.value = true;
// } else {
//   LocalStorage.set('authtoken', tokenData.value)
//   router.push({ path: '/' })
// }

// console.log(LocalStorage.getItem('authtoken'))
</script>

<style lang="scss">
#loginPage {
  .form-style {
    margin: 0 auto;
    height: 80vh;
    max-width: 500px;
  }
  .no-account {
    font-size: 17px;
  }
}
</style>
