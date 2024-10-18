let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");


menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})

function startCapture() {
    fetch('/start_capture')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert(data.message);
            } else {
                alert("Fehler: " + data.message);
            }
        })
        .catch(error => {
            console.error('Fehler beim Starten der Aufnahme:', error);
        });
}