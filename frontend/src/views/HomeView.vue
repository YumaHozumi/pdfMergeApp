<template>
  <v-app class="ma-0" fluid>
    <MyHeader></MyHeader>
    <!--appを指定するとcssのpostion: fixedが適用される-->
    <v-main>
      <v-container fluid>
        <v-row justify="center" class="my-5">
          <div v-show="!loading">
            <div id="dragDropArea">
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
              </div>
            </div>
            <button @click="uploadFile">送信</button>
          </div>
          <div v-show="loading">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </v-row>

        <v-row>
          <v-col cols="4" class="border" v-for="url in urls" :key="url">
            <v-card v-if="url.isPDF">
              <iframe :src="url.file"></iframe>
            </v-card>
            <v-img :src="url.file" v-else />
          </v-col>
        </v-row>
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
    };
  },
  methods: {
    selectedFile(e) {
      let files = e.target.files;
      console.log(files);
      this.images.push(...files);
      console.log(this.images.length);
      let regex = /\.pdf$/;
      for (let i = 0; i < files.length; i++) {
        let isPDF = regex.test(files[i].name); // isPDF is true
        let file = URL.createObjectURL(files[i]);
        this.urls.push({ file: file, isPDF: isPDF });
      }
    },
    async init() {
      this.images = [];
      this.encodeImg = [];
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
  },
};
</script>
