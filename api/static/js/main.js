var socket = io();

$(document).ready(function(){ 
  socket.on('socket_to_client', function(msg) {
      console.log(msg.data)
  });
})

function emitSocket() {
  socket.emit("socket_to_server", {"data": "hello server"})
}