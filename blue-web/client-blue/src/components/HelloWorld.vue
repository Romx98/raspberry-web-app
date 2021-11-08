<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "HelloWorld",
  data() {
    return {
      msg: 'Default value'
    }
  },
  methods: {
    getMessage() {
      const path = "/message";
      axios.get(path)
        .then((resp) => {
          this.msg = resp.data.msg;
        })
        .catch((err) => {
          console.error(err);
        })
        .finally(() => {
          setTimeout(this.getMessage(), 1000);
        });
    }
  },
  created() {
    this.msg = "Hallo";
    this.getMessage();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
