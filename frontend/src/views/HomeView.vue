<template>
  <v-app class="ma-0" fluid>
    <MyHeader></MyHeader>
    <!--appを指定するとcssのpostion: fixedが適用される-->
    <v-main>
      <v-container fluid>
        <v-row justify="center" class="my-5">
          <div v-show="!loading">
            <div
              id="dragDropArea"
              @dragenter="dragEnter"
              @drop.prevent="dropFile"
              @dragover.prevent
            >
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
        <p>{{ images.length }}</p>

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

<style src="../assets/style.css"></style>

<script>
import axios from "axios";
import MyHeader from "../components/MyHeader.vue";

export default {
  components: {
    MyHeader,
  },
  data() {
    return {
      books: "",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      images: [],
      encodeImg: [],
      loading: false,
      urls: [],
      isPush: false,
      draggingItem: null,
      isError: false,
      id: 0,
    };
  },
  methods: {
    selectedFile(e) {
      this.isPush = true;
      let files = e.target.files;
      this.pushfiles(files);
    },
    async init() {
      this.isPush = false;
      this.images = [];
      this.encodeImg = [];
      this.urls = [];
      console.log("init");
    },
    async uploadFile() {
      this.loading = true;
      for (let i = 0; i < this.images.length; i++) {
        let reader = await new FileReader();
        //画像をbase64に変換する
        reader.readAsDataURL(this.images[i]);
        console.log("Completed Encode");
        await new Promise(
          (resolve) =>
            (reader.onload = () => {
              resolve();
              this.encodeImg.push(reader.result);
            })
        );
      }
      await axios
        .post("/merge", this.encodeImg, this.headers)
        .then((response) => {
          this.loading = false;
          console.log(response);
          if (response.data !== null) {
            //レスポンスがnullでないなら
            //画像を保存
            let a = document.createElement("a");
            a.href = "data:application/pdf;base64," + response.data;
            a.download = this.random() + ".pdf";
            a.click();
            a.remove();
          }
        })
        .catch((e) => {
          console.log(e);
        });
      await this.init();
    },
    random() {
      //ランダムなファイル名を生成するための文字列生成用ファンクション
      let chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      let rand_str = "";
      for (var i = 0; i < 10; i++) {
        rand_str += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return rand_str;
    },
    dragEnter() {
      console.log("test");
    },
    dropFile(event) {
      this.isPush = true;
      console.log(this.isPush);
      let files = event.dataTransfer.files;
      this.pushfiles(files);
    },
    pushfiles(files) {
      if(!this.isImage(files)) {
        this.isError = true;
        return;
      }
      this.images.push(...files);
      let regex = /\.pdf$/;
      for (let i = 0; i < files.length; i++) {
        let isPDF = regex.test(files[i].name); // isPDF is true
        let file = URL.createObjectURL(files[i]);
        this.urls.push({ id: this.id, file: file, isPDF: isPDF });
        this.id++;
      }
      this.isError = false;
    },
    dragStartItem(index, e) {
      this.draggingItem = index;
      e.dataTransfer.effectAllowed = "move";
      e.target.style.opacity = 0.5;
    },
    dragEnterItem(index) {
      if (index == this.draggingItem) return;
      const deleteElement = this.urls.splice(this.draggingItem, 1)[0];
      const imageDelete = this.images.splice(this.draggingItem, 1)[0];
      this.urls.splice(index, 0, deleteElement);
      this.images.splice(index, 0, imageDelete);
      this.draggingItem = index;
    },
    dragOverItem(e) {
      e.dataTransfer.dropEffect = "move";
    },
    dragEndItem(e) {
      e.target.style.opacity = 1;
      this.draggingItem = null;
      console.log(this.urls);
      console.log(this.images);
    },
    isImage(files) {
      let regex = /\.(pdf|jpeg|jpg|png)$/;
      for(let i = 0; i < files.length; i++){
        let isImg = regex.test(files[i].name);
        console.log(isImg + "test");
        if(!isImg) return false;
      }
      return true;
    }
  },
};
</script>
