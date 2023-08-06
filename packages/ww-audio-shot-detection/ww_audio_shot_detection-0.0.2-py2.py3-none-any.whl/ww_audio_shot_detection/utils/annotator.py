import cv2
import pandas as pd
from io import StringIO
from collections import namedtuple

Point = namedtuple("Point", "x y")
Rect = namedtuple("Rect", "x1 y1 x2 y2")

class Annotator():
    def __init__(self):
        self.tmp_points = list()
        self.data = list()
        self.states = list()

    def process_user_actions(self):
        while True:
            key = cv2.waitKey(0) & 0xFF
            # reset selection
            if key == ord("r"):
                self.image = self.states.pop()
                if not self.states:
                    self.states.append(self.image.copy())
                if len(self.data):
                    self.data.pop()
            # confirm selection
            elif key == ord("c"):
                break
            elif key == ord("e"):
                return True

    def click_and_select(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.tmp_points.append(Point(x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            start_coords = self.tmp_points.pop()

            self.add_data(start_coords, x, y)

            self.states.append(self.image.copy())
            cv2.rectangle(self.image, start_coords, (x, y), (0, 255, 0), 2)
            cv2.imshow('frame', self.image)
    

class Window():
    def __init__(self, local_vid_path, event_manager):
        cv2.namedWindow('frame')
        self.cap = cv2.VideoCapture(local_vid_path)
        success, self.image = self.cap.read()
        if not success:
            print(f'Unable to read video: {local_vid_path}')
            return
        
        def click_and_select(event, x, y, flags, param):
            return event_manager.click_and_select(event, x, y, flags, param)

        cv2.setMouseCallback('frame', click_and_select)

        cv2.imshow('frame', self.image)

    def __enter__(self):
        (img_width, img_height) = cv2.getWindowImageRect('frame')[2:]
        return {'image': self.image, 'width': img_width, 'height': img_height, 'cap': self.cap}

    def __exit__(self, type, value, traceback):
        cv2.destroyAllWindows()
