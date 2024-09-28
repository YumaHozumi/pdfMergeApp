<template>
  <v-app class="ma-0" fluid>
    <MyHeader></MyHeader>
    <v-main>
      <v-container fluid>
        <v-row justify="center" class="my-5">
          <div v-show="!loading">
            <div id="dragDropArea" @drop.prevent="dropFile" @dragover.prevent>
              <div class="drag-drop-inside">
                <p class="drag-drap-info">ここにファイルをドロップ</p>
                <p>または</p>
                <p class="drag-drop-buttons">
                  <input
                    type="file"
                    @change="selectedFile"
                    multiple
                    accept="image/png,image/jpeg,application/pdf,image/jpg"
                  />
                </p>
                <v-expand-transition>
                  <v-layout class="error-msg" v-if="isError">
                    <v-icon left color="red">mdi-alert-circle</v-icon>
                    <span>pdf/png/jpeg/jpgのみ使用できます</span>
                  </v-layout>
                </v-expand-transition>
              </div>
            </div>
            <v-btn @click="uploadFile" class="my-3" color="blue" v-if="isPush">
              Upload
              <v-icon right dark>mdi-cloud-upload</v-icon>
            </v-btn>
          </div>
          <div v-show="loading">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </v-row>

        <TransitionGroup name="items-list" v-if="isPush">
          <v-row key="row">
            <v-col
              cols="4"
              class="border"
              v-for="(url, index) in urls"
              :key="url.id"
              draggable="true"
              @dragstart="dragStartItem(index, $event)"
              @dragenter="dragEnterItem(index)"
              @dragover.stop.prevent="dragOverItem"
              @dragend.stop.prevent="dragEndItem"
            >
              <v-icon class="close" @click="deleteFile(index)"
                >mdi-trash-can-outline</v-icon
              >
              <v-card v-if="url.isPDF">
                <iframe :src="url.file"></iframe>
              </v-card>
              <v-img :src="url.file" v-else />
            </v-col>
          </v-row>
        </TransitionGroup>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import MyHeader from '@/components/MyHeader.vue';

const headers = { "Content-Type": "multipart/form-data" };
const images = ref([]);
const encodeImg = ref([]);
const loading = ref(false);
const urls = ref([]);
const isPush = ref(false);
const draggingItem = ref(null);
const isError = ref(false);
const id = ref(0);

const selectedFile = (e) => {
  isPush.value = true;
  let files = e.target.files;
  pushfiles(files);
};

const resetInput = () => {
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.value = '';
  }
};

const init = async () => {
  isPush.value = false;
  images.value = [];
  encodeImg.value = [];
  urls.value = [];
  
  console.log("init");
};

const uploadFile = async () => {
  loading.value = true;

  for (let i = 0; i < images.value.length; i++) {
    let reader = new FileReader();
    reader.readAsDataURL(images.value[i]);
    console.log("Completed Encode");
    await new Promise((resolve) => {
      reader.onload = () => {
        resolve();
        encodeImg.value.push(reader.result);
      };
    }).catch(console.error);
  }
  await axios
    .post("/merge", encodeImg.value, headers)
    .then((response) => {
      loading.value = false;
      if (response.data !== null) {
        let a = document.createElement("a");
        a.href = "data:application/pdf;base64," + response.data;
        a.download = random() + ".pdf";
        a.click();
        a.remove();
      }
    })
    .catch((e) => {
      console.log(e);
    });
  await init();
  resetInput();
};

const random = () => {
  let chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let rand_str = "";
  for (var i = 0; i < 10; i++) {
    rand_str += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return rand_str;
};

const dropFile = (event) => {
  isPush.value = true;
  let files = event.dataTransfer.files;
  pushfiles(files);
};

const pushfiles = (files) => {
  if (!isImage(files)) {
    isError.value = true;
    return;
  }
  images.value.push(...files);
  let regex = /\.pdf$/;
  for (let i = 0; i < files.length; i++) {
    let isPDF = regex.test(files[i].name);
    let file = URL.createObjectURL(files[i]);
    urls.value.push({ id: id.value, file: file, isPDF: isPDF });
    id.value++;
  }
  isError.value = false;
};

const dragStartItem = (index, e) => {
  draggingItem.value = index;
  e.dataTransfer.effectAllowed = "move";
  e.target.style.opacity = 0.5;
};

const dragEnterItem = (index) => {
  if (index == draggingItem.value) return;
  const deleteElement = urls.value.splice(draggingItem.value, 1)[0];
  const imageDelete = images.value.splice(draggingItem.value, 1)[0];
  urls.value.splice(index, 0, deleteElement);
  images.value.splice(index, 0, imageDelete);
  draggingItem.value = index;
};

const dragOverItem = (e) => {
  e.dataTransfer.dropEffect = "move";
};

const dragEndItem = (e) => {
  e.target.style.opacity = 1;
  draggingItem.value = null;
};

const isImage = (files) => {
  let regex = /\.(pdf|jpeg|jpg|png)$/;
  for (let i = 0; i < files.length; i++) {
    let isImg = regex.test(files[i].name);
    if (!isImg) return false;
  }
  return true;
};

const deleteFile = (index) => {
  urls.value.splice(index, 1);
  images.value.splice(index, 1);
};
</script>

<style src="@/assets/style.css"></style>
