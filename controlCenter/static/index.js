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

document.addEventListener('DOMContentLoaded', function() {
    // Event-Listener für den Start Capture Button
    document.getElementById('start-capture').addEventListener('click', function() {
        // Eingabefelder validieren
        const origin = document.getElementById('herkunftsland').value.trim();
        const destination = document.getElementById('zielland').value.trim();
        const weight = document.getElementById('gewicht').value.trim();

        // Liste der gültigen Länder und Landeskürzel
        const validCountries = ["DE", "FR", "CZ", "GB", "CN", "IN", "LB", "IRQ", "IRN", "UKR",
                                "Deutschland", "Frankreich", "Tschechien", "Großbritannien", "China", "Indien", "Libanon", "Irak", "Iran", "Ukraine"];

        if (!origin || !destination || !weight) {
            alert("Bitte füllen Sie alle Felder aus.");
            return;
        }

        if (!validCountries.includes(origin) || !validCountries.includes(destination)) {
            alert("Bitte geben Sie gültige Länder oder Landeskürzel ein.");
            return;
        }

        // Eingabefelder ausblenden
        document.getElementById('input-fields').style.display = 'none';
        // Daten an den Server senden
        fetch('/start_capture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                origin: origin,
                destination: destination,
                weight: weight
            })
        })
        .then(response => response.json())
        .then(data => console.log('Start Capture ausgelöst', data))
        .catch(error => console.error('Error:', error));
        
    });

    // Event-Listener für den Bildanzeigen-Button
    document.getElementById('view-image').addEventListener('click', function() {
        document.getElementById('image-overlay').style.display = 'flex';
    });
});

// Funktion zum Schließen des Bild-Overlays
function closeImageOverlay() {
    document.getElementById('image-overlay').style.display = 'none';
}

// Funktion zum Schließen des Bild-Overlays
function closeImageOverlay() {
    document.getElementById('image-overlay').style.display = 'none';
}

// Basis-URL vom Server bereitgestellt und im JavaScript verfügbar
function downloadMonthlyReport() {
    var selectedMonth = document.getElementById("month").value;
    if (selectedMonth) {
        // Erzeuge die vollständige URL für den Download
        window.location.href = "download_report/" + selectedMonth;
    } else {
        alert("Bitte einen Monat auswählen.");
    }
}

