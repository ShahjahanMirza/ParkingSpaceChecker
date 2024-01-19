import pickle
import cv2

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError as e:
    posList = []

width, height = 69, 31


def mouseclick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:  # add point where left button clicked
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:  # remove the points
        for ind, pos in enumerate(posList):
            x1, y1 = pos
            if (x1 < x < (x1+width)) and (y1 < y < (y1+height)):
                posList.pop(ind)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)  # save the points in file f (points file)


while True:
    img = cv2.imread('ParkingLot.PNG')

    for pos in posList:
        cv2.rectangle(img, pos,  (pos[0] + width, pos[1]+height), (0, 0, 255), 2)

    cv2.imshow('img', img)
    cv2.setMouseCallback('img', mouseclick)  # takes in displayed image name, returns events, x, y, flags, params

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
