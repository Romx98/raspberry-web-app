<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import SocketIO from "socket.io-client";
const socketConnection = SocketIO("http://192.168.137.111:5000");

export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Waiting for server connection!"
    }
  },
  methods: {
    sendConnect() {
      socketConnection.on('connect', () => {
        socketConnection.emit('my event', {data: 'I\'m connected!'});
        console.log('I\'m connected!');
      })
    },
    closeConnect() {
      socketConnection.on('disconnect', () => {
        socketConnection.emit('my event', {data: 'I\'m disconnected!'});
        console.log('I\'m disconnected!');
      })
    }
  },
  created() {
    this.sendConnect();
  },
  mounted() {
    socketConnection.on("blue data", (message) => {
        this.msg = message.data;
        console.log(message);
      })
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
