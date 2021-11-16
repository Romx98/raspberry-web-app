<template>
  <div class="hello">
    <h1 v-if="isConnect">{{ msg }}</h1>
  </div>
</template>

<script>
import SocketIO from "socket.io-client";
const socketConnection = SocketIO("http://192.168.137.111:8000");

export default {
  name: "HelloWorld",
  data() {
    return {
      isConnect: false,
      msg: "Default value"
    }
  },
  methods: {

    socketconnect() {
      socketConnection.on("connect-data", (socket) => {
        this.msg = socket.data;
        console.log(this.msg);
      })
    },
    socketlistener() {
      socketConnection.on("blue-data", (socket) => {
        this.msg = socket.data;
        console.log(this.msg);
      })
    }
  },
  created() {
    this.socketlistener();
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
