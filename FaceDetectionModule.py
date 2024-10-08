import cv2
import mediapipe as mp
import time

class FaceDetector:
    def __init__(self, minDetectionCon = 0.75, modelSelection = 0):
        self.minDetectionCon = minDetectionCon
        self.modelSelection = modelSelection

        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findFaces(self, img, draw=True, drawLength = 22, drawThickness = 3, drawThicknessRectangle = 1):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxes = []

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                bboxes.append([id, bbox, detection.score])

                if draw:
                    img = self.fancyDraw(img, bbox, drawLength, drawThickness, drawThicknessRectangle)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)

        return img, bboxes

    def fancyDraw(self, img, bbox, l, t, rt):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(img, bbox, (255, 0, 255), rt)

        # Top Left - x, y
        cv2.line(img, (x, y), (x+l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y+l), (255, 0, 255), t)

        # Top Right - x1, y
        cv2.line(img, (x1, y), (x1-l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y+l), (255, 0, 255), t)

        # Bottom Left - x, y1
        cv2.line(img, (x, y1), (x+l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1-l), (255, 0, 255), t)

        # Bottom Right - x1, y1
        cv2.line(img, (x1, y1), (x1-l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1-l), (255, 0, 255), t)

        return img

def example():
    cap = cv2.VideoCapture('Videos/3.mp4')
    pTime = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()

        img, bboxes = detector.findFaces(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Image', cv2.resize(img, (1280, 720), interpolation=cv2.INTER_CUBIC))

        # Instead of img for videos use: cv2.resize(img, (1280, 720), interpolation=cv2.INTER_CUBIC

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    example()