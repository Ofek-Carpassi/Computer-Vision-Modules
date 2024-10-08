import cv2
import mediapipe as mp
import time

class FaceMesh:
    def __init__(self, mode = False, maxFaces = 1, refine = False, detCon = 0.5, trackCon = 0.5, thick = 1, circRad = 1):
        self.mode = mode
        self.maxFaces = maxFaces
        self.refine = refine
        self.detCon = detCon
        self.trackCon = trackCon

        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.mode, self.maxFaces, self.refine, self.detCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=thick, circle_radius=circRad)

    def mesh(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        faces = []

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)

                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    # Can do the same for z
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    #cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                    face.append([x, y])
                faces.append(face)

        return img, faces

def example():
    cap = cv2.VideoCapture(0) # Capture video from camera
    pTime = 0
    faceMesh = FaceMesh()

    while True:
        success, img = cap.read()

        img, faces = faceMesh.mesh(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Image', img)
        # Instead of img for videos use: cv2.resize(img, (1280, 720), interpolation=cv2.INTER_CUBIC

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    example()