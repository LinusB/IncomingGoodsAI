import cv2
import os
import re
from ultralytics import YOLO

script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'images')
save_dir2 = "./currentProcess"
if not os.path.exists(save_dir2):
    os.makedirs(save_dir2)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def get_next_image_number(directory):
    existing_files = os.listdir(directory)
    numbers = [int(re.search(r'product_(\d+)\.jpg', f).group(1)) for f in existing_files if re.match(r'product_(\d+)\.jpg', f)]
    if numbers:
        return max(numbers) + 1  
    else:
        return 0 

frame_counter = get_next_image_number(save_dir)

model = YOLO('yolov5s.pt')

camera = cv2.VideoCapture(0)

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
        image_path2 = os.path.join(save_dir2, f'product_captured.jpg')
        raw_image_path = os.path.join(save_dir2, f'product_captured_raw.jpg')
        cv2.imwrite(image_path, annotated_frame)
        cv2.imwrite(image_path2, annotated_frame)
        cv2.imwrite(raw_image_path, frame)
        print(f"Produkt erkannt und Bild gespeichert: {image_path}")
        frame_counter += 1  
        break  


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("Skript erfolgreich beendet.")