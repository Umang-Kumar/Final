const video = document.getElementById("video");

Promise.all([
  faceapi.nets.faceRecognitionNet.loadFromUri('http://127.0.0.1:5000/static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('http://127.0.0.1:5000/static/models'),
  faceapi.nets.ssdMobilenetv1.loadFromUri('http://127.0.0.1:5000/static/models')
]).then(start);

function start() {
  //Requesting permission from chrome to access webcam
  navigator.getUserMedia(
    { video:{} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )

  recognizeFaces();
}

async function recognizeFaces() {
  const labeledDescriptors = await loadLabeledImages();
  const faceMatcher = new faceapi.FaceMatcher(labeledDescriptors, 0.6);

  video.addEventListener("play", () => {
    //Creating a canvas to add overlay video
    const canvas = faceapi.createCanvasFromMedia(video);
    canvas.classList.add("canvas");
    document.body.append(canvas);
    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(async () => {
      const detections = await faceapi
        .detectAllFaces(video)
        .withFaceLandmarks()
        .withFaceDescriptors();

      const resizedDetections = faceapi.resizeResults(detections, displaySize);

      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

      const results = resizedDetections.map((d) => {
        return faceMatcher.findBestMatch(d.descriptor);
      });
      results.forEach((result, i) => {
        const box = resizedDetections[i].detection.box;
        const drawBox = new faceapi.draw.DrawBox(box, {
          label: result.toString(),
        });
        drawBox.draw(canvas);
      });
    }, 100);
  });
}

function loadLabeledImages() {
  
  const labels = ["57_Gal", "55_Alo", "56_Umang", "58_Kristen", "53_Emma"];

  // const labels = [];
  // let matching = async function(){
  //   let match = await fetch('/arrayOfFiles/');
  //   let data = await match.json();
  //   return data.data;
  // }
    
  // matching().then(item => {
  //   for (let index = 0; index < item.length; index++) {
  //     labels.push(item[index]["name"]);
  //   }
  //   // console.log(labels);
  // })

  // console.log(labels);
  return Promise.all(
      labels.map(async (label)=>{
        console.log(label)
        
          const descriptions = []
          for(let i=1; i<2; i++) {
              const img = await faceapi.fetchImage(`http://127.0.0.1:5000/static/labeled_images/${label}/${i}.jpg`)
              const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor()
              // console.log(label + i + JSON.stringify(detections))
              descriptions.push(detections.descriptor)
          }
          // document.body.append(label+' Faces Loaded | ')
          return new faceapi.LabeledFaceDescriptors(label, descriptions)
      })
  )
}