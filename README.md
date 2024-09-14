# Image Classification using Google Gemini 1.5 Flash

## Ziel

Dieser Branch implementiert eine Lösung zur Klassifizierung von Produkten anhand von Bildern und der Zuordnung einer entsprechenden Zollnummer (HS-Code). Die Bildklassifikation erfolgt über die Google Gemini 1.5 Flash API. Das Hauptziel ist es, den Produktklassifizierungsprozess zu automatisieren und die zugehörige HS-Nummer (Zollnummer) sowie weitere relevante Informationen, wie Ursprungsland und Gewicht, in einer strukturierten Excel-Datei bereitzustellen.

## Features

	• 	Bildklassifizierung: Automatische Erkennung des Produkts anhand eines hochgeladenen Bildes.
	•	HS-Code Zuordnung: Basierend auf der Klassifikation wird die entsprechende HS-Nummer (aus Spalte ‘CN8’ eines zugehörigen PDF-Dokuments) ermittelt.
	•	Excel-Generierung: Die Ergebnisse werden in einer Excel-Tabelle mit den folgenden Spalten gespeichert:
	•	Intrastat-Nummer (HS-Code)
	•	Ursprungsland
	•	Gewicht
	•	Kategorieaufteilung: Die Excel-Datei wird in 21 Unterabschnitte basierend auf Produktkategorien unterteilt.

## Ordnerstruktur
	•	./images: Hier werden die zu klassifizierenden Bilder abgelegt.
	•	./data: Hier befinden sich die PDF-Dokumente mit den relevanten HS-Codes.
	•	./results: Hier werden die generierten Excel-Dateien gespeichert.


## Nutzung

1. Bild und PDF hochladen:
	•	Platziere das Bild im Verzeichnis ./images.
	•	Platziere das zugehörige PDF im Verzeichnis ./data.
2.	Führe das Skript zur Klassifikation und HS-Code-Zuordnung aus:
	>	imageClassification.py
3.	Die generierte Excel-Datei wird im Ordner ./results abgelegt.
