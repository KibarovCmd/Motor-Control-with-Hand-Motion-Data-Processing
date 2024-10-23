import cv2
from ultralytics import YOLO
import math
import serial

model = YOLO("model.pt")

cap = cv2.VideoCapture(0)

print("When the camera is switched on, move your hand to the synchronized position.")
usb_port = input("Enter Port: ")  # USB-Uart Port
baud_rate = 9600

try:
    ser = serial.Serial(usb_port, baud_rate, timeout=1)
    print("Port O.")
except serial.SerialException as e:
    print("Port C")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Camera Was Not Opened!")
        break

    results = model(frame)

    for detection in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls_id = detection
        x1, y1, x2, y2, cls_id = int(x1), int(y1), int(x2), int(y2), int(cls_id)
        
        if cls_id == 0:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    thumb_tip_finger_x, thumb_tip_finger_y = int(), int()
    index_tip_finger_x, index_tip_finger_y = int(), int()

    for key_result in results:
        for index in range(key_result.keypoints.shape[1]):
            cx, cy = key_result.keypoints.cpu().xy.numpy()[0][index]
            cx, cy = int(cx), int(cy)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            if index == 8:
                index_tip_finger_x, index_tip_finger_y = cx, cy
            if index == 4:
                thumb_tip_finger_x, thumb_tip_finger_y = cx, cy

    cv2.line(frame, (thumb_tip_finger_x, thumb_tip_finger_y), (index_tip_finger_x, index_tip_finger_y), (0, 255, 0), 1)
    data_motor = str(int(math.sqrt((thumb_tip_finger_x - index_tip_finger_x) ** 2 + (thumb_tip_finger_y - index_tip_finger_y) ** 2)))
    data_motor += '\n'

    try:
        ser.write(data_motor.encode())
        print(data_motor)
        print("Data R")
    except Exception as e:
        print("Data W")

    cv2.imshow('YOLO Key Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('a'):
        print(y2 - y1)
        print(data_motor)

ser.close()
cap.release()
cv2.destroyAllWindows()
