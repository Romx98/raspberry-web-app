<template>
  <div class="hello">
    <h1>{{ this.msg }}</h1>
  </div>
</template>

<script>
import io from "socket.io-client"

export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Default value",
      socket: io("ws://localhost:5000", {
        transports: ["websocket"]
      })
    }
  },
  methods: {
    
    socketcall() {
      this.socket.on("MESSAGE", (socket) => {
        this.msg = socket;
        console.log(this.msg);
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
