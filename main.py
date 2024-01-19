import cv2
import pickle
import numpy as np
import cvzone

# Capture video
cap = cv2.VideoCapture('video.mp4')

# Load x and y coordinates file
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# Pre-define parking spots height
width, height = 69, 31


# preprocess image
def processing(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert image to gray
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)  # add gaussian blur to the image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 180,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,
                                         25, 16)
    kernel = np.ones((3,3), np.uint8)
    imgDilated = cv2.dilate(imgThreshold, kernel, iterations=1)  # dilate the image for easy pixel counting
    return imgDilated


# check space and change values based on availability
def checkspace(imgProc):

    freespacecount = 0  # track free spaces
    for pos in posList:
        x, y = pos
        imgcrop = imgProc[y:y+height, x:x+width]  # crop image to get each parking slot

        pixelscount = cv2.countNonZero(imgcrop)  # check pixels of each parkig slot

        # based on pixel count for each slot, change values
        if pixelscount < 700:
            color = (0, 255, 0)  # green for free space
            thickness = 5
            freespacecount += 1
        else:
            color = (0, 0, 255)  # red for parked
            thickness = 2

        # create a rectangle where the x and y points are with the changed values
        cv2.rectangle(img, pos, (x + width, y + height), color= color, thickness = thickness)
        # write pixel count inside the rectangles
        cvzone.putTextRect(img, str(pixelscount), (x, y+height-3), scale=1, thickness=2, offset=0,  colorR = color)

    # write the total free space count at the top
    cvzone.putTextRect(img, f'Free Space: {freespacecount}/{len(posList)}', (240,40), colorR = (0, 255, 0), scale=2, thickness = 3, offset = 5)


while True:
    # reset frame count when it reaches 0
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # read the image from video
    success, img = cap.read()

    # resize img to trained image size
    img = cv2.resize(img, (758, 986))

    # preprocess image
    procImg = processing(img)

    # create boxes, labels and change colors based on the preprocess image
    checkspace(procImg)

    # display the image which has been changed based on the previous working
    cv2.imshow('img', img)

    # exit when 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
