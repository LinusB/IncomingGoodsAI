import cv2

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            print(f'Kamera {index} ist verfügbar')
            arr.append(index)
        cap.release()
        index += 1
    return arr

available_cameras = list_cameras()
print(f"Verfügbare Kameras: {available_cameras}")