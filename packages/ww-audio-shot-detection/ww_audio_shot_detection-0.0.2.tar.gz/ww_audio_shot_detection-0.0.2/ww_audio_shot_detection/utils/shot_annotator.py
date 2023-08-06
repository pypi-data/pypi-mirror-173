import cv2
import pandas as pd
from io import StringIO
from ww_audio_shot_detection.utils.annotator import Annotator, Window, Rect
from ww_audio_shot_detection.utils.rectangle import Rectangle

class ShotAnnotator(Annotator):
    def __init__(self):
        Annotator.__init__(self)
        
        self.frame_num = 0

    def annotate(self, file):
        with Window(file.LocalVidPath, self) as window:
            self.image, self.img_width, self.img_height, self.cap = window['image'], window['width'], window['height'], window['cap']
            if self.image is None:
                return
            self.states.append(self.image.copy())    

            while True:
                self.frame_num += 1
                success, self.image = self.cap.read()
                if not success:
                    break
                if self.frame_num % 2 == 0:
                    continue
                
                cv2.imshow('frame', self.image)

                cancel = self.process_user_actions()
                if cancel:
                    break

        result_data = self.build_result_data()
        print(result_data)
        file.Data.extend(result_data)

    def add_data(self, start_coords, x, y):
        shot_made = False
        key = cv2.waitKey(0) & 0xFF
        if key == ord("Y"):
            shot_made = True
        
        self.data.append({
            'frame_num': self.frame_num,
            'x1': start_coords.x / self.img_width,
            'y1': start_coords.y / self.img_height,
            'x2': x / self.img_width,
            'y2': y / self.img_height,
            'shot_made': shot_made
        })

    def build_result_data(self):
        data = self.data
        if not data:
            return list()
        
        assert len(data) % 2 == 0

        if len(data) == 2:
            return [self.build_res_line(data[0], data[1])]

        result_data = list()
        while True:
            found_intersections = False
            first_box = self.data.pop(0)
            first_rect = Rectangle(*tuple(first_box[k] for k in Rect._fields))
            for num, second_box in enumerate(self.data):
                second_rect = Rectangle(*tuple(second_box[k] for k in Rect._fields))
                if first_rect & second_rect:
                    start_frame, end_frame = min(first_box['frame_num'], second_box['frame_num']), max(first_box['frame_num'], second_box['frame_num'])
                    result_data.append(self.build_res_line(first_box, second_box))
                    self.data.pop(num)
                    found_intersections = True
                    break
            if not self.data:
                return result_data
            
            assert found_intersections

    def build_res_line(self, first_box, second_box):
        start_frame, end_frame = min(first_box['frame_num'], second_box['frame_num']), max(first_box['frame_num'], second_box['frame_num'])
        return {
            'start_frame': start_frame, 'end_frame': end_frame, 'shot_made': first_box['shot_made'] or second_box['shot_made'],
            **{k: first_box[k] for k in Rect._fields}
        }

    @staticmethod
    def build_csv_contents(file):
        keys = ('start_frame', 'end_frame') + Rect._fields + ('shot_made',)
        keys_full = ('id',) + keys
        data = {key: list() for key in keys_full}
        for num, rect in enumerate(file.Data):
            data['id'].append(num)
            for key in keys:
                data[key].append(rect[key])

        df = pd.DataFrame(data=data)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index = False)

        return csv_buffer.getvalue()

