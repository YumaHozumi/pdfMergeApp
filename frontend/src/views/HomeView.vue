<template>
  <div v-show="!loading">
    <input type="file" @change="selectedFile" multiple />
    <button @click="uploadFile">送信</button>
  </div>
  <div v-show="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      books: "",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      images: [],
      encodeImg: [],
      loading: false,
    };
  },
  methods: {
    selectedFile(e) {
      let files = e.target.files;
      console.log(files);
      this.images.push(...files);
      console.log(this.images.length);
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
