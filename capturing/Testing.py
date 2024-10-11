import cv2
from ultralytics import YOLO

# YOLO-Modell laden
model = YOLO('yolov5s.pt')  # YOLOv5 pre-trained model

# Kamera initialisieren
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kamera konnte nicht geöffnet werden")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("Fehler beim Einlesen des Bildes")
        break
    
    # YOLOv5 Objekterkennung auf dem Frame
    results = model(frame)

    # Ergebnisse rendern (Zeichnen von Bounding Boxes)
    annotated_frame = results[0].plot()

    # Zeige den Frame mit den erkannten Objekten
    cv2.imshow('YOLOv5', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()