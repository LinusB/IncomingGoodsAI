let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");


menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})

const socket = io();

socket.on('status_update', function(data) {
    const reportBody = document.getElementById('report-body');
    const messageElement = document.createElement('div');
    messageElement.className = 'items';

    const message = data.message;

    // Nur spezifische Meldungen verarbeiten
    const validMessages = [
        "Speed: ",
        "Produkt erkannt und Bild gespeichert: ",
        "Uploaded file ",
        "Product: ",
        "Infrastat-Nummer: ",
        "Bildaufnahme und Klassifizierung erfolgreich"
    ];

    if (validMessages.some(validMessage => message.startsWith(validMessage))) {
        // Spezielle Verarbeitung für Infrastat-Nummer
        if (message.startsWith("Infrastat-Nummer: ")) {
            const [number, description] = message.replace('Infrastat-Nummer: ', '').split(', Beschreibung: ');
            messageElement.innerHTML = `
                <div><strong>Infrastat-Nummer:</strong> ${number}</div>
                <div><strong>Beschreibung:</strong> ${description}</div>
            `;
        } else {
            messageElement.innerHTML = `<div class="items">${message}</div>`;
        }
        reportBody.appendChild(messageElement);

        // Zeige den "Bild anzeigen" Button an, wenn der Prozess erfolgreich abgeschlossen ist
        if (message === "Bildaufnahme und Klassifizierung erfolgreich") {
            document.getElementById('view-image').style.display = 'flex';
        }
    }
});

// Event-Listener für den Start Capture Button
// Event-Listener für den Start Capture Button
document.getElementById('start-capture').addEventListener('click', function() {
    if (document.getElementById('view-image').style.display === 'flex') {
        location.reload();
    }
    fetch('/start_capture')
        .then(() => console.log('Start Capture ausgelöst'))
        .catch(error => console.error('Error:', error));
});

// Event-Listener für den Bildanzeigen-Button
document.getElementById('view-image').addEventListener('click', function() {
    document.getElementById('image-overlay').style.display = 'flex';
});

// Funktion zum Schließen des Bild-Overlays
function closeImageOverlay() {
    document.getElementById('image-overlay').style.display = 'none';
}

document.getElementsByID('start-capture').addEventListener('click', function() {

        location.reload();
});