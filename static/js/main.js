var alertWrapper = document.querySelector(".alert")
var alertClose = document.querySelector(".alert__close")

console.log("inside js..")

if(alertWrapper){
    console.log("alert close...")
    alertClose.addEventListener("click", () => {
        alertWrapper.style.display = 'none';
    })
}

