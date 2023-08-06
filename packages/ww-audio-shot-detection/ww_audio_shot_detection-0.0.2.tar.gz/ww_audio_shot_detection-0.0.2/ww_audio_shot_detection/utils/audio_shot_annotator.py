import cv2
import math
import pandas as pd
from io import StringIO
from utils.annotator import Annotator, Window, Rect
from utils.rectangle import Rectangle

class AudioShotAnnotator(Annotator):
    def __init__(self):
        Annotator.__init__(self)
        
        self.frame_num = 0
        self.is_shot = False
        self.is_scored = False
        self.start_fnum = None
        # length of a time period around the shot to use 
        self.shot_len_sec = 4

    def annotate(self, file):
        with Window(file.LocalVidPath, self) as window:
            self.image, self.cap = window['image'], window['cap']
            if self.image is None:
                return

            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.duration = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.fps

            while True:
                self.frame_num += 1
                success, self.image = self.cap.read()
                if not success:
                    break
                if self.frame_num % 2 == 0:
                    continue
                
                self.show_frame()

                while True:
                    key = cv2.waitKey(0) & 0xFF
                    # mark is shot
                    if key == ord("s"):
                        self.is_shot = not self.is_shot
                    # mark shot is scored
                    if key == ord("S"):
                        self.is_scored = not self.is_scored
                    # confirm selection
                    elif key == ord("c"):
                        if self.is_shot:
                            curr_sec = self.frame_num / self.fps
                            start_sec = max(curr_sec - self.shot_len_sec / 2, 0)
                            end_sec = min(curr_sec + self.shot_len_sec / 2, self.duration)
                            self.data.append({
                                'start_sec': round(start_sec, 2),
                                'end_sec': round(end_sec, 2),
                                'scored': self.is_scored
                            })
                        self.is_shot, self.is_scored = False, False
                        break
                    # stop annotating
                    elif key == ord("e"):
                        file.Data.extend(self.data)
                        return True
                    self.show_frame()
            file.Data.extend(self.data)


    def show_frame(self):
        img = self.image.copy()
        if self.is_shot:
            cv2.putText(img, 'SELECTING', (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)
        if self.is_scored:
            cv2.putText(img, 'SCORED', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 8)
        cv2.imshow('frame', img)


    @staticmethod
    def build_csv_contents(file):
        keys = ('start_sec', 'end_sec', 'scored')
        keys_full = ('id',) + keys
        data = {key: list() for key in keys_full}
        for num , audio_data in enumerate(file.Data):
            data['id'].append(num)
            for key in keys:
                data[key].append(audio_data[key])

        df = pd.DataFrame(data=data)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index = False)

        return csv_buffer.getvalue()