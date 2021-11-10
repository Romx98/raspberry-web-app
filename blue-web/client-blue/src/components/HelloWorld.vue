<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import axios from "axios"
import io from "socket.io-client"

export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Default value",
      socket: io("ws://localhost:5000", {
        transports: ['websocket']
      })
    }
  },
  methods: {
    getMessage() {
      const path = "/message";
      axios.get(path)
        .then((resp) => {
          this.msg = resp;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    socketcall() {
      this.socket.on('MESSAGE', () => {
        this.getMessage()
      })
    }
  },
 
  mounted() {
    this.socketcall();
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
