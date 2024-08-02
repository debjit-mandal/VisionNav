import cv2
import numpy as np

class ObjectDetection:
    def __init__(self, config_path, weights_path, names_path):
        self.net = cv2.dnn.readNet(weights_path, config_path)
        with open(names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_objects(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        boxes, confidences, class_ids = [], [], []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        detections = []
        if len(indices) > 0:
            for i in indices:
                i = i[0] if isinstance(i, (list, np.ndarray)) else i
                box = boxes[i]
                detections.append({
                    "class_id": class_ids[i],
                    "confidence": confidences[i],
                    "box": box,
                    "label": self.classes[class_ids[i]]
                })
        else:
            print("No detections found")

        return detections
