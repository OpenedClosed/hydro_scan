<template>
  <q-page id="loginPage">
    <q-toolbar class="text-white bg-primary">
      <q-toolbar-title> Регистрация </q-toolbar-title>
    </q-toolbar>

    <q-scroll-area class="form-style">
      <div class="q-pa-md q-gutter-md">
        <!-- <div class="text-center q-m-xs">Зарегистрируйтесь для получения!</div> -->

        <q-input
          v-model="username"
          :error="hasErrorUsername"
          :error-message="errorUsername"
          outlined
          stack-label
          label="Username"
        >
          <template v-slot:append>
            <!-- <q-icon name="close"></q-icon> -->
          </template>
        </q-input>
        <q-input v-model="last_name" outlined stack-label label="Фамилия">
          <template v-slot:append>
            <!-- <q-icon name="close"></q-icon> -->
          </template>
        </q-input>
        <q-input v-model="first_name" outlined stack-label label="Имя">
          <template v-slot:append>
            <!-- <q-icon name="close"></q-icon> -->
          </template>
        </q-input>
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

        <div class="q-px-md q-pb-lg">
          <div class="row justify-end q-pt-md">
            <q-btn
              size="lg"
              class="full-width"
              color="black"
              label="Зарегистрироваться"
              @click.prevent="sendComponentData()"
            />
          </div>
        </div>
      </div>
    </q-scroll-area>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import { apiAxios } from "boot/axios";
import { useRouter } from "vue-router";
import { LocalStorage } from "quasar";

const router = useRouter();
const username = ref("");
const email = ref("");
const first_name = ref("");
const last_name = ref("");
const password = ref("");
const errorMessage = ref("");
const responseData = ref(null);
const hasErrorUsername = ref(false);
const hasErrorEmail = ref(false);
const hasErrorPassword = ref(false);
const isPwd = ref(true);
const errorUsername = ref("");
const errorEmail = ref("");
const errorPassword = ref("");
const tokenData = ref(null);

function sendRegistrationInfo(data) {

  return apiAxios
    .post("/api/users/", data)
    .then((response) => {
      responseData.value = response.data;


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

      return responseData.value;
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
        errorUsername.value = "";
        hasErrorEmail.value = false;
        hasErrorPassword.value = false;
        hasErrorUsername.value = false;
        if (errorMessage.value.username) {
          hasErrorUsername.value = true;
          errorUsername.value = errorMessage.value.username[0];
        }
        if (errorMessage.value.email) {
          hasErrorEmail.value = true;
          errorEmail.value = errorMessage.value.email[0];
        }
        if (errorMessage.value.password) {
          hasErrorPassword.value = true;
          errorPassword.value = errorMessage.value.password[0];
        }
      } else if (err.request) {
        // The client never received a response, and the request was never left
      } else {
        router.push({ path: "/auth" });
      }
    });
}

function sendComponentData() {
  isPwd.value = true
  const data = {
    username: username.value,
    email: email.value,
    first_name: first_name.value,
    last_name: last_name.value,
    password: password.value,
  };

  errorMessage.value = sendRegistrationInfo(data);
}
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
