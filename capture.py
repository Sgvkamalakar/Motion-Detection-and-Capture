import os
import cv2
from datetime import datetime
import time
def capture_motion():
    script_directory = os.path.join(os.getcwd(), "results")
    if not os.path.exists(script_directory):
        os.makedirs(script_directory)
    print('Capturing starts soon....')
    print('Waiting for 📸 to turn on....')
    time.sleep(0.5)
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    _, frame1 = video.read()
    print('📸 turned on ')
    time.sleep(1)
    while True:
        _, frame2 = video.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_path = os.path.join(script_directory, f"motion_captured_{timestamp}.jpg")
            cv2.imwrite(image_path, frame2)
            print('Motion captured')
        frame1 = frame2
        cv2.imshow("Motion Detection", frame2)
        if cv2.waitKey(1) == ord('q') :
            break
    video.release()
    cv2.destroyAllWindows()
capture_motion()