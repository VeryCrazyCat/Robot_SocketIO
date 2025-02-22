var socket = io();

$(document).ready(function(){ 
  socket.on('nodemcu_status', function(msg) {
    console.log(msg)
      changeStatusDisplay(msg.data)
  });
})

function toggleLED() {
    socket.emit("nodemcu_action", {"action": 1})
    // 1 -> LED toggle
}

function changeStatusDisplay(msg) {
    const stateDisplay = document.querySelector(".status-display")
    stateDisplay.innerHTML = msg
}