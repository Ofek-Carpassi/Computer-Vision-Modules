# Computer-Vision-Modules

Modules built for computer vision using MediaPipe and OpenCV.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Modules](#modules)
  - [Face Detection](#face-detection)
  - [Face Mesh](#face-mesh)
  - [Hand Tracking](#hand-tracking)
  - [Pose Estimation](#pose-estimation)
- [Usage](#usage)
- [License](#license)

## Introduction

This repository contains various modules for computer vision tasks, leveraging the power of MediaPipe and OpenCV. These modules can be used for face detection, face mesh, hand tracking, and pose estimation.

## Installation

To use these modules, you need to have Python installed along with the required libraries. You can install the dependencies using pip:

```sh
pip install opencv-python mediapipe
```
## Modules
### Face Detection
The face detection module is implemented in `FaceDetectionModule.py`. It uses the MediaPipe Face Detection model to detect faces in an image or video stream.

### Face Mesh
The face mesh module is implemented in `FaceMeshModule.py`. It uses the MediaPipe Face Mesh model to detect facial landmarks in an image or video stream.

### Hand Tracking
The hand tracking module is implemented in `HandTrackingModule.py`. It uses the MediaPipe Hand Tracking model to detect hands in an image or video stream.

### Pose Estimation
The pose estimation module is implemented in `PoseEstimationModule.py`. It uses the MediaPipe Pose Estimation model to detect human poses in an image or video stream.

## Usage
Each module can be imported and used in your Python code. Here is an example of how to use the face detection module:

```python
import cv2
import FaceDetectionModule as fd

cap = cv2.VideoCapture(0)

face_detector = fd.FaceDetector()

while True:
    success, img = cap.read()

    img = face_detector.find_faces(img)

    cv2.imshow("Face Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.