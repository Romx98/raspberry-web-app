<template>
  <div class="hello">
    <h1>{{ original_msg }}</h1>
    <h2>{{ mutable_msg }}</h2>
  </div>
</template>

<script>
import SocketIO from "socket.io-client";
const socketIO = SocketIO("http://192.168.137.111:5000");

export default {
  name: "HelloWorld",
  data() {
    return {
      original_msg: 'Defaul value!',
      mutable_msg: ''
    }
  },
  methods: {
    connectionMsg() {
      socketIO.on('connect', () => {
        console.log('Connected to the server!');
      })
    },
    messageData() {
      socketIO.on('blue-data', (resp) => {
        this.original_msg = resp.original;
        this.mutable_msg = resp.mutable;
        console.log(resp);
      })
    }
  },
  created() {
    this.connectionMsg();
  },
  mounted() {
    this.messageData();
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
