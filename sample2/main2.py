import cv2
import pickle
import cvzone
import numpy as np

# Video feed
#cap = cv2.VideoCapture('pexels-oleh-shtohryn-5587732 (2160p).mp4')
cap = cv2.VideoCapture('sample2\production_id_3858833 (2160p).mp4')
with open('sample2\car_Park_pos2', 'rb') as f:
    posList = pickle.load(f)

width, height = 125,210


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 2170:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
    cv2.resizeWindow("Image", 1080, 1080)
    cv2.imshow("Image", img)
    key = cv2.waitKey(10) & 0xFF
    if key == 27:  # 27 is the ASCII code for the 'Esc' key
        break

# Resize the images for proper display
    #imgBlurDisplay = cv2.resize(imgBlur, (600, 400))  # Adjust the size as needed
    #imgMedianDisplay = cv2.resize(imgMedian, (600, 400))

    #cv2.imshow("ImageBlur", imgBlurDisplay)
    #cv2.imshow("ImageThres", imgMedianDisplay)
    #imgMedianDisplay = cv2.resize(imgDilate, (200, 100))
    #cv2.imshow("ImageDilate", imgDilate)