//Fetching Video frame from HTML
const video = document.getElementById('video');

//Connect to flask server port
var socket = io(namespace='/video/');
//Join to the connect socket in Flask server to test connection
socket.on('connect', function() {
  console.log("SOCKET CONNECTED")
  socket.send("User has connected.");
})

//Requesting permission from chrome to access webcam
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
// Load the models from the Models folder
Promise.all([
    faceapi.loadFaceLandmarkModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadFaceRecognitionModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadTinyFaceDetectorModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadFaceLandmarkModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadFaceLandmarkTinyModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadFaceRecognitionModel('http://127.0.0.1:5000/static/models'),
    faceapi.loadFaceExpressionModel('http://127.0.0.1:5000/static/models'),
])
    .then(startVideo)
    .catch(err => console.error(err));


//Fuction which starts streaming of webcam data and creates stream object
function startVideo() {
  console.log("access");
  navigator.getUserMedia(
    {
      video: {}
    },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
  console.log("streaming");
}

video.addEventListener('play', () => {
    //Creating a canvas to add overlay image
      const canvas = faceapi.createCanvasFromMedia(video);
      canvas.classList.add('canvas');
      document.body.append(canvas);
      const displaySize = { width: video.width, height: video.height};
      faceapi.matchDimensions(canvas, displaySize);
    
    //Asynchronusly get detections from the video Stream
      setInterval(async () => {
        const detections = await faceapi
          .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()) //Face Detectors
          .withFaceLandmarks()  // Get cordinates of landmarks
          .withFaceExpressions();  //Get Face Expression confidence values
        // console.log(detections[0].alignedRect)
    //Send The Data to the flask Backend on each async detection
        socket.emit( 'my event', {
            data: detections
        })
    // Resize and Display the detections on the video frame using canvas
        const resizedDetections = faceapi.resizeResults(detections, displaySize);
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height );
        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
    //Printing the detection coordinates
        // console.log(detections);
        // socket.send({data: detections});
      }, 100)
  }
)
