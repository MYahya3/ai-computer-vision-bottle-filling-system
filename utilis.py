import cv2
import numpy as np

# To make detections and get required outputs
def YOLO_Detection(model, frame, conf=0.10, mode = "track"):
    # Perform inference on an image
    if mode == "track":
        results = model.track(frame, conf=conf, iou = 0.5, classes = [39])
        # Extract bounding boxes, classes, names, and confidences
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()
        ids = results[0].boxes.id.tolist()
        return boxes, classes, names, confidences, ids

    elif mode == "pred":
        results = model.predict(frame, conf=conf, classes = [39])
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()
        return boxes, classes, names, confidences

## Draw YOLOv8 detections function
def label_detection(frame, text, left, top, bottom, right, tbox_color=(30, 155, 50), fontFace=1, fontScale=0.8,
                    fontThickness=1):
    # Draw Bounding Box
    cv2.rectangle(frame, (int(left), int(top)), (int(bottom), int(right)), tbox_color, 1)
    # Draw and Label Text
    textSize = cv2.getTextSize(text, fontFace, fontScale, fontThickness)
    text_w = textSize[0][0]
    text_h = textSize[0][1]
    y_adjust = 10
    cv2.rectangle(frame, (int(left), int(top) - text_h - y_adjust), (int(left) + text_w + y_adjust, int(top)),
                  tbox_color, -1)
    cv2.putText(frame, text, (int(left) + 5, int(top) - 5), fontFace, fontScale, (255, 255, 255), fontThickness,
                cv2.LINE_AA)

def drawPolygons(frame, points_list, detection_points=None, polygon_color_inside=(30, 205, 50),
                 polygon_color_outside=(30, 50, 180), alpha=0.5, occupied_polygons = int):

    for area in points_list:
        # Reshape the flat tuple to an array of shape (4, 1, 2)
        area_np = np.array(area, np.int32)
        if detection_points:
            is_inside = any(cv2.pointPolygonTest(area_np, pt, False) >= 0 for pt in detection_points)
        else:
            is_inside = False
        color = polygon_color_inside if is_inside else polygon_color_outside
        if is_inside:
            occupied_polygons += 1

    return frame, occupied_polygons
