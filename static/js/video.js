const video = document.getElementById("video");


const sendBtn=document.getElementById("sendData");



let attendanceObj={};

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
  const labeledDescriptors =await loadLabeledImages();
  const faceMatcher =  new faceapi.FaceMatcher(labeledDescriptors, 0.6);

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

      
        attendanceObj[result._label]=false;
        // document.body.append(result._label," is Present")
        
        drawBox.draw(canvas);
      });
    }, 100);
  });
}

// console.log(attendanceObj)


const labels = [];
let matching = async function(){
  let match = await fetch('/arrayOfFiles/');
  let data = await match.json();
  // console.log(data.data)
  return data.data;
}
    

matching().then(item => {
  for (let index = 0; index < item.length; index++) {
   
    labels.push(item[index].name);
    attendanceObj[item[index].name]=true;
   
  }
})


function loadLabeledImages() { 

  return Promise.all(
      
      labels.map(async (label)=>{
        
          const descriptions = []
          for(let i=1; i<2; i++) {
              const img = await faceapi.fetchImage(`http://127.0.0.1:5000/static/labeled_images/${label}/${i}.jpg`) || 
              await faceapi.fetchImage(`http://127.0.0.1:5000/static/labeled_images/${label}/${i}.jpeg`) || 
              await faceapi.fetchImage(`http://127.0.0.1:5000/static/labeled_images/${label}/${i}.png`);
              const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor()
              // console.log(label + i + JSON.stringify(detections))
              descriptions.push(detections.descriptor)
          }
          // document.body.append(label+' Faces Loaded | ')
          return new faceapi.LabeledFaceDescriptors(label, descriptions)
      })
  )
}



labels.map((item)=>{
  console.log(item);
  attendanceObj[item]=true;
})
sendBtn.addEventListener("click",()=>{
  console.log(attendanceObj);
  JSON.stringify(attendanceObj);
  console.log(JSON.stringify(attendanceObj));
  document.getElementById("attendance").value = JSON.stringify(attendanceObj);
})


window.onload=function(){
    // -- put your code here
    const checkbox = document.getElementById("checkbox");

  checkbox.addEventListener("change" , ()=>{
    document.body.classList.toggle("dark");
    // console.log("hello");
  })

}