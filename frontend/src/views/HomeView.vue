<template>
  <input type="file" @change="selectedFile" multiple />
  <button @click="uploadFile">送信</button>
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
      for (let i = 0; i < this.images.length; i++) {
        let reader = await new FileReader();
        reader.readAsDataURL(this.images[i]);
        console.log("Completed Encode");
        await new Promise(
          (resolve) =>
            (reader.onload = () => {
              resolve();
              let val = reader.result.replace(/data:.*\/.*;base64,/, "");
              this.encodeImg.push(val);
            })
        );
      }
      await axios
        .post("/merge", this.encodeImg, this.headers)
        .then((response) => {
          this.books = response.data;
        })
        .catch((e) => {
          console.log(e);
        });
      await this.init();
    },
  },
};
</script>
