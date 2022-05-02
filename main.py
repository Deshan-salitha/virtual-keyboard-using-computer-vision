#Start Date : 2021/09/21
#Auther : Deshan Wickramaarachchi
#Tutorial : https://www.youtube.com/watch?v=jzXZVFqEE2I

import cv2
import mediapipe as mp
import cvzone.HandTrackingModule
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import  cvzone
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon = 0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = " "

#def drawAll(img, buttonList):
#    for button in buttonList:
#        x, y = button.pos
#        w, h = button.size
#        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 100, 0), cv2.FILLED)
#        cv2.putText(img, button.text, (x + 5, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#    return img

def drawAll(img, buttonList):
    imgnew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos

        cvzone.cornerRect(imgnew, (button.pos[0],button.pos[1],button.size[0], button.size[1]),20, rt=0)
        cv2.rectangle(imgnew, button.pos, (x + button.size[0], y+ button.size[1]), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgnew, button.text, (x + 40, y + 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgnew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgnew, 1 - alpha, 0)[mask]
    return out



class Button():
    def __init__(self, pos, text, size=[65, 75]):
        self.pos = pos
        self.text = text
        self.size = size



buttonList = []
#myButton = Button([100,100], "Q")
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] <x+w and y <lmList[8][1]<y+h :
                cv2.rectangle(img, button.pos, (x + w, y + h), (175,0,175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 5, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8,12, img, draw=False)

                print(l)
                #when clicked
                if l<30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 252, 124), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 5, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.35)

    cv2.rectangle(img, (50, 350), (700, 450), (0, 252, 124), cv2.FILLED)
    cv2.putText(img, finalText, (60, 450), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)