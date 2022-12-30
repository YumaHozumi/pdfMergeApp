<template>
  <input type="file" @change="selectedFile" multiple />
  <button @click="uploadFile">送信</button>
</template>

<script>
//import axios from "axios";

export default {
  data() {
    return {
      books: "",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      images: [],
    };
  },
  methods: {
    selectedFile(e) {
      let files = e.target.files;
      this.images.push(...files);
    },
    uploadFile() {
      let reader = FileReader();

      reader.readAsDataURL(this.images[0]);
      reader.onload = () => {
        var val = reader.result.replace(/data:.*\/.*;base64,/, '');
        console.log(val);
      };
      // this.images.forEach((file, index) => {
      //   formData.append("files[" + index + "]", file);
      // });
      // axios
      //   .post("/merge", formData, this.headers)
      //   .then((response) => {
      //     this.books = response.data;
      //     console.log(response);
      //   })
      //   .catch((e) => {
      //     console.log(e);
      //   });
    },
  },
};
</script>
