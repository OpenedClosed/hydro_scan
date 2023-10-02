<template>
  <q-page id="indexPage" img-class="flex flex-top">
    <q-img alt="Quasar logo" src="~assets/3d-model.jpg" img-class="imageStyle">
      <div
        class="caption no-background absolute-center no-back text-subtitle1 text-center"
      >
        <h3>ПОДВОДНЫЕ ОСМОТРОВЫЕ РАБОТЫ</h3>
        <h5>быстрее чем водолазы и с подробным отчетом</h5>
        <div>
          <q-btn class="buttonStyle" @click="checkLogin()" color="blue-4"
            >Заказать</q-btn
          >
        </div>
      </div>
    </q-img>

    <div class="center">
      <div class="text-center">
        <h3>Услуги</h3>
        <p>Возможны дополнительные услуги по договоренности</p>
      </div>

      <div class="row">
        <div class="q-pa-md col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <q-avatar class="avatarStyle">
              <q-icon size="9em" name="visibility"></q-icon>
            </q-avatar>

            <div class="text-center">
              <h5>3D сканирование</h5>
              <p>
                С помощью подводного аппарата, оснащенного камерой высокого
                разрешения, производится съемка объекта. После обработки данных,
                получается 3D модель объекта.
              </p>
            </div>
          </q-card>
        </div>

        <div class="q-pa-md  col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <q-avatar class="avatarStyle">
              <q-icon size="9em" name="heart_broken"></q-icon>
            </q-avatar>
            <div class="text-center">
              <h5>Дефектоскопия</h5>
              <p>
                Специальная нейросеть анализирует полученную 3D модель и выдает
                отчет о наличии дефектов.
              </p>
            </div>
          </q-card>
        </div>

        <div class="q-pa-md col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <q-avatar class="avatarStyle">
              <q-icon size="9em" name="map"></q-icon>
            </q-avatar>
            <div class="text-center">
              <h5>Координаты</h5>
              <p>
                3D модель будет привязана к предпочитаемой системе координат.
              </p>
            </div>
          </q-card>
        </div>
        <div class="q-pa-md bordered col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <q-avatar class="avatarStyle">
              <q-icon
                size="9em"
                name="file_present
                "
              ></q-icon>
            </q-avatar>
            <div class="text-center">
              <h5>Отчеты по ГОСТ</h5>
              <p>
                Отчеты о проведении работ и результаты их выполнения
                подготавливаются в соответствии с ГОСТ
              </p>
            </div>
          </q-card>
        </div>
      </div>
    </div>

    <div class="greyBackground">
      <div class="center">
      <div class="text-center">
        <h3>Продукты</h3>
      </div>

      <div class="row">
        <div class="q-pa-md col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <div>
              <q-img src="~assets\project_cousteau_3_thumb.webp"></q-img>
            </div>
            <div class="text-center">
              <h6>«Кусто 3»</h6>
              <p>Автономный подводный аппарат</p>
            </div>
          </q-card>
        </div>
        <div class="q-pa-md col-sm-12 col-md-4 items-start q-gutter-md">
          <q-card flat>
            <div>
              <q-img src="~assets\project_hydroscan_rov_thumb.webp"></q-img>
            </div>
            <div class="text-center">
              <h6>«Гидроскан»</h6>
              <p>Телеуправляемый подводный аппарат</p>
            </div>
          </q-card>
        </div>
      </div>
      </div>
    </div>

      <div class="center text-center q-my-xl">
        <h3>О КОМПАНИИ</h3>
        <p class="q-mb-xl">Чем мы занимаемся</p>
        <p>Мы предоставляем заказчику услуги по осмотру и сканированию подводных объектов (дно судна, гидротехнические сооружения, нефте/газодобывающие вышки), выдаем отчет об осмотре в удобном для заказчика формате - 3д модель, ортофотоплан, изображения с привязкой к месту, оформленным согласно установленным истандартам.</p>
      </div>

  <div class="greyBackground">
    <div class="center q-px-lg q-py-md">
      <q-timeline :layout="layout" color="secondary">
        <q-timeline-entry heading>
          <h3>ИСТОРИЯ КОМПАНИИ</h3>
        </q-timeline-entry>

        <q-timeline-entry
          title="УНМЦ Гидронавтика"
          subtitle="2019-2022"
          side="left"
        >
          <div>
            <q-avatar class="q-my-md" size="210px">
              <q-img src="~assets\hydro.webp"></q-img>
            </q-avatar>

            <p>
              Команда проекта сформировалась в УНМЦ Гидронавтика в МГТУ им.
              Н.Э.Баумана. Мы занимались разработкой автономных и
              телеуправляемых подводных аппаратов, ездили на международные
              соревнования и занимали призовые места. Весной 2022 года
              зародилась идея проекта «Гидроскан».
            </p>
          </div>
        </q-timeline-entry>

        <q-timeline-entry
          title="Выиграли грант «Студенческий стартап»"
          subtitle="2022"
          side="left"
        >
          <div>
            <q-avatar class="q-my-md" size="210px">
              <q-img src="~assets\fpi.webp"></q-img>
            </q-avatar>

            <p>
              Осенью 2022 года мы выиграли грант «Студенческий стартап» и начали
              работу над проектом. Закупили большинство необходимых компонентов
              и начали разработку аппарата.
            </p>
          </div>
        </q-timeline-entry>
        <q-timeline-entry
          title="Создание ООО «Гидроскан»"
          subtitle="2023"
          side="left"
        >
          <div>
            <q-avatar class="q-my-md" size="210px">
              <q-img src="~assets\logo_inverted.webp"></q-img>
            </q-avatar>

            <p>Зимой 2023 года мы зарегистрировали компанию «Гидроскан».</p>
          </div>
        </q-timeline-entry>
        <q-timeline-entry
          title="Разрабатываем «Гидроскан»"
          subtitle="2023"
          side="left"
        >
          <div>
            <q-avatar class="q-my-md" size="210px">
              <q-img src="~assets\project_hydroscan_rov_thumb.webp"></q-img>
            </q-avatar>

            <p>
              Мы активно ведем разработку нашего собственного телеуправляемого
              подводного аппарата «Гидроскан». С помощью него мы будем выполнять
              сканирование под водой.
            </p>
          </div>
        </q-timeline-entry>
        <q-timeline-entry title="Будущее" side="left"> </q-timeline-entry>
      </q-timeline>
    </div>
  </div>
    <div class="center lastStyle" ref="teamRef">
      <div class="text-center">
        <h3>Наша команда</h3>
      </div>

      <div class="row">
        <div class="q-pa-md col-sm-12 col-md-3 items-start q-gutter-md">
          <q-card flat>
            <div class="center">
              <q-avatar class="avatarStyle">
                <q-img src="~assets\grisha.webp"></q-img>
              </q-avatar>
            </div>
            <div class="text-center">
              <h5>Григорий Старых</h5>
              <p>Генеральный директор</p>
              <q-btn style="" round dense href="https://t.me/grishafv">
                <q-icon name="send" />
              </q-btn>
            </div>
          </q-card>
        </div>
        <div class="q-pa-md col-sm-12 col-md-3 items-start q-gutter-md">
          <q-card flat>
            <div class="center">
              <q-avatar class="avatarStyle">
                <q-img src="~assets\nikita.webp"></q-img>
              </q-avatar>
            </div>
            <div class="text-center">
              <h5>Никита Михненко</h5>
              <p>Главный конструктор</p>
              <q-btn style="" round dense href="https://t.me/kilop7890">
                <q-icon name="send" />
              </q-btn>
            </div>
          </q-card>
        </div>
        <div class="q-pa-md col-sm-12 col-md-3 items-start q-gutter-md">
          <q-card flat>
            <div class="center">
              <q-avatar class="avatarStyle">
                <q-img src="~assets\dima.webp"></q-img>
              </q-avatar>
            </div>
            <div class="text-center">
              <h5>Дмитрий Затекин</h5>
              <p>Главный электронщик</p>
              <q-btn style="" round dense href="https://t.me/dimchazty">
                <q-icon name="send" />
              </q-btn>
            </div>
          </q-card>
        </div>
        <div class="q-pa-md col-sm-12 col-md-3 items-start q-gutter-md">
          <q-card flat>
            <div class="center">
              <q-avatar class="avatarStyle">
                <q-img src="~assets\vlad.webp"></q-img>
              </q-avatar>
            </div>
            <div class="text-center">
              <h5>Владислав Плотников</h5>
              <p>Главный программист</p>
              <q-btn style="" round dense href="https://t.me/vladushked">
                <q-icon name="send" />
              </q-btn>
            </div>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import { LocalStorage } from "quasar";

const router = useRouter();
function checkLogin() {
  const token = LocalStorage.getItem("myString");
  if (token) {
    router.push({ path: "/order" });
  } else {
    router.push({ path: "/auth" });
  }
}
defineComponent({
  name: "IndexPage",
});
</script>
<style lang="scss">
#indexPage {
  .imageStyle {
    width: 100%;
    max-height: 1000px;
  }
  .no-background {
    background: none;
  }
  .buttonStyle {
    width: 240px;
    font-size: 24px;
  }
  .cardStyle {
    width: 33%;
  }
  .center {
    width: 60%;
    margin-right: auto;
    margin-left: auto;
  }
  .no-outline {
    outline: none;
  }
  .avatarStyle {
    width: 100%;
    height: 100%;
  }
  .lastStyle {
    margin-bottom: 220px;
  }
  .greyBackground{
    background-color: #F7F7F7;
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
  }
}
</style>
