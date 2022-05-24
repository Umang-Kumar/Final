document.querySelector("#selection").addEventListener("click", function () {
  imageUpload.click();
});

const imageUpload = document.getElementById('imageUpload');

//Connect to flask server port
var socket = io(namespace='/addUser/');

Promise.all([
  faceapi.nets.faceRecognitionNet.loadFromUri('http://127.0.0.1:5000/static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('http://127.0.0.1:5000/static/models'),
  faceapi.nets.ssdMobilenetv1.loadFromUri('http://127.0.0.1:5000/static/models')
]).then(start)

async function start() {
  const container = document.createElement('div')
  const preview1 = document.getElementById('preview');
  container.style.position = 'relative'
  preview1.append(container)
  // const labeledFaceDescriptors = await loadLabeledImages()
  // const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6)
  let image
  let canvas
  // document.body.append('Loaded')
  imageUpload.addEventListener('change', async () => {
    if (image) image.remove()
    if (canvas) canvas.remove()
    image = await faceapi.bufferToImage(imageUpload.files[0])
    container.append(image)
    canvas = faceapi.createCanvasFromMedia(image)
    canvas.classList.add('canvas');
    container.append(canvas)
    const displaySize = { width: image.width, height: image.height }
    faceapi.matchDimensions(canvas, displaySize)
    const detections = await faceapi.detectAllFaces(image).withFaceLandmarks().withFaceDescriptors()
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    console.log(resizedDetections);
    socket.emit('user',{
      data: resizedDetections
    })
    // const results = resizedDetections.map(d => faceMatcher.findBestMatch(d.descriptor))
    // results.forEach((result, i) => {
    //   const box = resizedDetections[i].detection.box
    //   const drawBox = new faceapi.draw.DrawBox(box, { label: result.toString() })
    //   drawBox.draw(canvas)
    // })
  })
}