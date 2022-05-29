window.onload=function(){
    // -- put your code here
    const checkbox = document.getElementById("checkbox");

checkbox.addEventListener("change" , ()=>{
    document.body.classList.toggle("dark");
    // console.log("hello");
})

}