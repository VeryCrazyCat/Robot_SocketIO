var socket = io();

$(document).ready(function(){ 
  socket.on('nodemcu_status', function(msg) {
    console.log(msg)
      changeStatusDisplay(msg.data)
  });
  socket.on('annotated_image_output', function(msg) {
    let img = document.querySelector(".photo-output")
    img.src = `data:image/png;base64,${msg["data"]}`;
  });
})

function toggleLED() {
    socket.emit("nodemcu_action", {"action": 1})
    // 1 -> LED toggle
}

function sendSignal(signal) {
  socket.emit("nodemcu_action", {"action": signal})
  // 1 -> LED toggle
}


function changeStatusDisplay(msg) {
    const stateDisplay = document.querySelector(".status-display")
    stateDisplay.innerHTML = msg
}