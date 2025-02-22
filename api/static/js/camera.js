var socket = io();

$(document).ready(function(){ 
  socket.on('socket_to_client', function(msg) {
      console.log(msg.data)
  });
})

function emitSocket() {
  socket.emit("socket_to_server", {"data": "hello server"})
}

//Gets canvas context (otherwise it is empty)
var canvas = document.querySelector('.canvas');
var context = canvas.getContext('2d');


let video = document.querySelector(".video_input")
video.width = 400
video.height = 300

let photo = document.querySelector(".photo")


if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({video: true})
  .then(function (stream) {
    video.srcObject = stream;
    video.play;
  })
  .catch(function (errormsg) {
    console.log(errormsg)
  })

  const inputFPS = 1;
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