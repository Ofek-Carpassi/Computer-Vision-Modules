import cv2
import numpy as np
import time
import MinimizedPoseEstimationModule as pm

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()

counter = 0
direction = 0 # 0 - up, 1 - down

pTime = 0

while True:
    success, img = cap.read()

    img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        """
        # Right arm
        detector.findAngle(img, 12, 14, 16)
        """
        # Left arm
        angle = detector.findAngle(img, 11, 13, 15)

        per = np.interp(angle, (197, 310), (0, 100))
        bar = np.interp(angle, (207, 310), (650, 100))

        # check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if direction == 0:
                counter += 0.5
                direction = 1
        if per == 0:
            color = (0, 255, 0)
            if direction == 1:
                counter += 0.5
                direction = 0

        # Draw Bar
        cv2.rectangle(img, (550, 100), (587, 375), (255, 255, 0), 4)
        cv2.rectangle(img, (550, int((bar / 2) + 50)), (587, 375), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (510, 88), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)

        # Draw curl count
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(counter)}', (0, 485), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (15, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()