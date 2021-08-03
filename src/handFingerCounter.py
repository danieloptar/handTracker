from cv2 import cv2
import time
import os
import handTracker as ht

class FingerCounter:
    def set_cam_settings(self):
        # Cam settings
        wCam, hCam = 1280, 720
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)

    def set_finger_images(self):
        # Finger count images
        folderPath = "images"
        myList: 'list[str]' = os.listdir(folderPath)
        self.fingerCountList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            self.fingerCountList.append(image)

    def set_cam_detector(self):
        self.pTime = 0
        self.detector = ht.handDetector(detectionCon=0.8)
        self.tipIds = [4, 8, 12, 16, 20]

    def handFingerCounter(self):
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                fingers = []
                # Thumb
                if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # All Fingers
                for id in range(1, 5):
                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                totalFingers = fingers.count(1)
                print(totalFingers)
                
                # image in corner
                h, w, c = self.fingerCountList[totalFingers - 1].shape
                img[0:h, 0:w] = self.fingerCountList[totalFingers - 1]
                cv2.rectangle(img, (20, 225), (170, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 25)
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (1000, 700), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 0), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        
if __name__ == "__main__":
    f = FingerCounter()
    f.set_cam_settings()
    f.set_finger_images()
    f.set_cam_detector()
    try:
        f.handFingerCounter()
    except KeyboardInterrupt:
        pass
        