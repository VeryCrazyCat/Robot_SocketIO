var socket = io();

$(document).ready(function(){ 
  socket.on('socket_to_client', function(msg) {
      console.log(msg.data)
  });
  socket.on('annotated_image_output', function(msg) {
    let img = document.querySelector(".photo-output")
    img.src = `data:image/png;base64,${msg["data"]}`;
  });
  socket.on('image_data_return', function(msg) {
    let p = document.querySelector(".data-return")
    p.innerHTML = msg["data"]
  });
})

function emitSocket() {
  socket.emit("socket_to_server", {"data": "hello server"})
}

//Gets canvas context (otherwise it is empty)
var canvas = document.querySelector('.canvas');
var context = canvas.getContext('2d');


let video = document.querySelector(".video_input")
video.width = 640
video.height = 360

let photo = document.querySelector(".photo")


if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({
    video: {
      facingMode: "environment"
    },
    width: {
      min: 640,
      ideal: 640,
      max: 720
    },
    height: {
      min: 360,
      ideal: 360,
      max: 480
    }
  })
  .then(function (stream) {
    video.srcObject = stream;
    video.play;
  })
  .catch(function (errormsg) {
    console.log(errormsg)
  })

  const inputFPS = 2;
  setInterval(() => {
    const width = video.videoWidth; // Use videoWidth for actual dimensions
    const height = video.videoHeight;

    canvas.width = width; // Set canvas width to video width
    canvas.height = height; // Set canvas height to video height


    context.drawImage(video, 0, 0, width, height);

    var data = canvas.toDataURL('image/jpeg', 0.5);
    photo.src = data;
    context.clearRect(0, 0, width, height);
    socket.emit('socket_to_image_processor', data);
  }, 1000/inputFPS)
}


