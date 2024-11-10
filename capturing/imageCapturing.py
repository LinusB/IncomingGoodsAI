import os
import re
from ultralytics import YOLO
import cv2

script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'images')
save_dir2 = "./currentProcess"
save_dir3 = "IncomingGoodsAI/controlCenter/static"

# Verzeichnisse erstellen, falls sie nicht existieren
if not os.path.exists(save_dir2):
    os.makedirs(save_dir2)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
if not os.path.exists(save_dir3):
    os.makedirs(save_dir3)

def get_next_image_number(directory):
    existing_files = os.listdir(directory)
    numbers = [int(re.search(r'product_(\d+)\.jpg', f).group(1)) for f in existing_files if re.match(r'product_(\d+)\.jpg', f)]
    if numbers:
        return max(numbers) + 1  
    else:
        return 0 

frame_counter = get_next_image_number(save_dir)

model = YOLO('yolov5s.pt')

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("Kamera konnte nicht geöffnet werden")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("Fehler beim Einlesen des Bildes")
        break
    
    results = model(frame)

    if len(results[0].boxes) > 0:
        annotated_frame = results[0].plot()

        image_path = os.path.join(save_dir, f'product_{frame_counter}.jpg')
        image_path2 = os.path.join(save_dir2, 'product_captured.jpg')
        image_path3 = os.path.join(save_dir3, 'product_captured.jpg')
        raw_image_path = os.path.join(save_dir2, 'product_captured_raw.jpg')

        # Bilder speichern und überprüfen, ob der Vorgang erfolgreich war
        if cv2.imwrite(image_path, annotated_frame):
            print(f"Produkt erkannt und Bild gespeichert: {image_path}")
        else:
            print(f"Fehler beim Speichern des Bildes: {image_path}")

        if cv2.imwrite(image_path2, annotated_frame):
            print(f"Produkt erkannt und Bild gespeichert: {image_path2}")
        else:
            print(f"Fehler beim Speichern des Bildes: {image_path2}")

        if cv2.imwrite(image_path3, annotated_frame):
            print(f"Produkt erkannt und Bild gespeichert: {image_path3}")
        else:
            print(f"Fehler beim Speichern des Bildes: {image_path3}")

        if cv2.imwrite(raw_image_path, frame):
            print(f"Rohbild gespeichert: {raw_image_path}")
        else:
            print(f"Fehler beim Speichern des Rohbildes: {raw_image_path}")

        frame_counter += 1  
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("Skript erfolgreich beendet.")