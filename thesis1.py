import cv2
import numpy as np
import thesis2 as htm
import time
import mouse
from pynput.mouse import Controller
from win32api import GetSystemMetrics
import pyautogui

scroll = Controller()

delay = 0.3
wCam, hCam = 640, 480
frameR = 100
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = GetSystemMetrics(0), GetSystemMetrics(1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:3]
        x2, y2 = lmList[12][1:3]

    fingers = detector.fingersUp()

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 255, 0), 2)

    # MOVE CURSOR
    if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        
        mouse.move(wScr - clocX, clocY)
        plocX, plocY = clocX, clocY

    # HOLD
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        distance, img, lineInfo = detector.findDistance(8, 12, img)
        if distance < 40:
            mouse.press('left')
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (0, 0, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY

        if distance > 100:
            mouse.release('left')

    # LEFT CLICK
    elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        distanceLeft, img, lineInfo = detector.findDistance(4, 1, img)
        mouse.click(button='left')
        time.sleep(delay)

    # RIGHT CLICK
    elif fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        distanceRight, img, lineInfo = detector.findDistance(20, 17, img)
        mouse.click(button='right')
        time.sleep(delay)

    # DOUBLE CLICK
    elif fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        distanceClick, img, lineInfo = detector.findDistance(4, 8, img)
        if distanceClick < 40:
            mouse.double_click(button='left')
            time.sleep(delay)

    # SCROLL UP
    elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
        distanceUp, img, lineInfo = detector.findDistance(4, 12, img)
        if distanceUp < 40:
            scroll.scroll(0, 3)
            time.sleep(delay)

    # SCROLL DOWN
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
        distanceDown, img, lineInfo = detector.findDistance(4, 16, img)
        if distanceDown < 40:
            scroll.scroll(0, -3)
            time.sleep(delay)

    # ZOOM IN/OUT
    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        distanceZoom, img, lineInfo = detector.findDistance(4, 8, img)
        print(f"Zoom Distance: {distanceZoom}")
        
        if distanceZoom < 40:  # Zoom In
            print("ZOOM IN")
            pyautogui.hotkey('ctrl', '+')
            time.sleep(delay)
        elif distanceZoom > 80:  # Zoom Out
            print("ZOOM OUT")
            pyautogui.hotkey('ctrl', '-')
            time.sleep(delay)

    cv2.imshow("Virtual Mouse", img)
    k = cv2.waitKey(1)
    if k == 27:
        break