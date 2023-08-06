import cv2
import pandas as pd
from io import StringIO
from collections import namedtuple
from ww_audio_shot_detection.utils.annotator import Annotator, Window, Rect

class HoopAnnotator(Annotator):
    def annotate(self, file):
        with Window(file.LocalVidPath, self) as window:
            self.image, self.img_width, self.img_height = window['image'], window['width'], window['height']
            if self.image is None:
                return
            self.states.append(self.image.copy())    

            self.process_user_actions()

        file.Data.extend(self.data)

    def add_data(self, start_coords, x, y):
        self.data.append(Rect(start_coords.x / self.img_width, start_coords.y / self.img_height, x / self.img_width, y / self.img_height))
    
    @staticmethod
    def build_csv_contents(file):
        data = {key: list() for key in ('id',) + Rect._fields}
        for num, rect in enumerate(file.Data):
            data['id'].append(num)
            for key in Rect._fields:
                data[key].append(getattr(rect, key))

        df = pd.DataFrame(data=data)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index = False)

        return csv_buffer.getvalue()

