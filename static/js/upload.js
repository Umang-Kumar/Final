var input = document.querySelector("#file-input");

document.querySelector("button").addEventListener("click", function () {
  input.click();
});

input.addEventListener("change", preview);
function preview() {
  var fileObject = this.files[0];
  var fileReader = new FileReader();
  fileReader.readAsDataURL(fileObject);
  fileReader.onload = function () {
    var result = fileReader.result;
    var img = document.querySelector("#preview");
    img.setAttribute("src", result);
  };
}

window.onload=function(){
    // -- put your code here
    const checkbox = document.getElementById("checkbox");

  checkbox.addEventListener("change" , ()=>{
    document.body.classList.toggle("dark");
    // console.log("hello");
  })

}