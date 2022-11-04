from datetime import datetime
import os
from PIL import Image
import cv2


frameWidth = 640
frameHeight = 480
minArea = 500
color = (255, 0, 255)
nPlateCascade = cv2.CascadeClassifier(
    "Resources/haarcascade_russian_plate_number.xml")

# не рабочий способ подрубить камеру
# cap = cv2.VideoCapture(1)

# подрубаем видео-камеру
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # captureDevice = camera
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

is_shot = False
gifs_created = False
final_images = []


while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)

    # делаем поиск номера
    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Car plate", (x, y - 5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)

            imgPlace = img[y:y + h, x:x + w]
            cv2.imshow("Place", imgPlace)

            # сохранение картинок
            dir_for_save_images = "./plates"
            if not os.path.exists(dir_for_save_images):
                os.mkdir(dir_for_save_images)
            print(str(datetime.now())[12:-1])
            path = f'{dir_for_save_images}/{str(datetime.now())[20:-1]}.jpg'
            cv2.imwrite(path, imgPlace)
            frame = Image.open(path)
            final_images.append(frame)

    cv2.imshow("Result", img)

    # делаем надпись
    print("создании гифки")
    im1 = Image.new("RGBA", (200, 200))
    dir_for_save_gifs = "./gifs"
    im1.save(f'{dir_for_save_gifs}/{str(datetime.now())[20:-1]}.gif', save_all=True, append_images=final_images,
             duration=100, loop=0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
