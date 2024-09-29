import cv2
import os

save_dir = './captured_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Kamera initialisieren (index 0 = erste Kamera)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kamera konnte nicht geöffnet werden")
    exit()

def product_detected(frame):

    return True

frame_counter = 0
while True:
    ret, frame = camera.read()
    
    if not ret:
        print("Fehler beim Einlesen des Bildes")
        break
    
    if product_detected(frame):
        image_path = os.path.join(save_dir, f'product_image_{frame_counter}.jpg')
        cv2.imwrite(image_path, frame)
        print(f"Bild gespeichert: {image_path}")
        frame_counter += 1
    
    # Live-Video
    cv2.imshow('Kamera Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()