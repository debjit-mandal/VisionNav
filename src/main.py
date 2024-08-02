import cv2
import asyncio
from src.object_detection import ObjectDetection
from src.tts import TextToSpeech
from src.slam import SLAM
from src.navigation import Navigation
from src.bluetooth import Bluetooth

def main():
    od = ObjectDetection("data/yolo/yolov3.cfg", "data/yolo/yolov3.weights", "data/yolo/coco.names")
    tts = TextToSpeech()
    slam = SLAM()
    nav = Navigation()
    bt = Bluetooth()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = od.detect_objects(frame)

        slam.update(frame)
        position = slam.get_position()

        nav_message = nav.navigate(detections)
        tts.speak(nav_message)

        for detection in detections:
            x, y, w, h = detection['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, detection['label'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    loop = asyncio.get_event_loop()
    beacon_data = loop.run_until_complete(bt.get_beacon_data())
    print(beacon_data)

if __name__ == "__main__":
    main()
