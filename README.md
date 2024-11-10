# Wareneingang - Automatische Produkterkennung und Intrastat-Nummer-Zuweisung

## Ziel

Dieses Projekt zielt darauf ab, den Prozess der Wareneingangserfassung zu automatisieren, indem Produkte anhand von Bildern automatisch klassifiziert werden. Die Klassifikation erfolgt mithilfe einer Künstlichen Intelligenz (KI) und weist den Produkten die entsprechende Intrastat-Nummer (HS-Code) zu. Die Bedienung erfolgt über eine Web-Oberfläche (WebUI), die eine einfache Handhabung und Verwaltung des Prozesses ermöglicht.

## Features

	• 	Automatische Produkterkennung: Die Produkte werden anhand eines Bildes klassifiziert. Hierbei werden die Bilddaten durch die KI verarbeitet, um das Produkt einer bestimmten Kategorie zuzuweisen.
	•	Intrastat-Nummer Zuordnung: Basierend auf der Produktklassifikation wird die entsprechende Intrastat-Nummer (HS-Code) automatisch ermittelt und zugeordnet.
	•	WebUI: Die Benutzeroberfläche ermöglicht eine einfache Bedienung des Systems, einschließlich der Uploads der Bilddateien und der Anzeige der Klassifikationsergebnisse.
	•	Erstellung einer Ergebnistabelle: Die Ergebnisse werden in einer strukturierten Tabelle angezeigt, die die Intrastat-Nummer, das Ursprungsland und das Gewicht des Produkts enthält.

## Ausführung des Codes

Um den Code auszuführen und das System zu starten, folge diesen Schritten:

	1.	Admin Dashboard starten:
	•	Navigiere zum Ordner controlCenter und starte die Datei handling.py:
		> python controlCenter/handling.py
	•	Dadurch wird ein lokaler Webserver mit Flask gestartet, der das Admin-Dashboard als Benutzeroberfläche bereitstellt. Das Dashboard kann über einen Webbrowser aufgerufen werden, typischerweise unter http://localhost:5000.

	2.	Kameraauswahl anpassen (optional):
	•	Falls eine andere Kamera verwendet werden soll, kann die Konfiguration in der Datei capturing/imageCapturing.py angepasst werden.
	•	Bearbeite hierfür Zeile 31, um die gewünschte Kameraquelle anzugeben.

	3.	Systemzugriff über das Dashboard:
	•	Im Dashboard können alle Funktionen des Projekts genutzt werden, einschließlich der automatischen Produkterkennung und der Zuordnung der Intrastat-Nummern.
