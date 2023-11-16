
import cv2
import pickle

width, height = 125,210

try:
    with open('sample2\car_Park_pos2', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('sample2\car_Park_pos2', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('sample2\photo2.png.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 3)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
    cv2.resizeWindow("Image", 800, 800)              # Resize window to specified dimensions
    cv2.imshow("Image", img)
    key = cv2.waitKey(10) & 0xFF
    if key == 27:  # 27 is the ASCII code for the 'Esc' key
        break
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(10)
