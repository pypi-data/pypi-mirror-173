#!/usr/bin/env python3

# TODO
# look for a ball when has motion only
# remove non moving detections (e.g time count)
# use only 2 hoops

import argparse
import asyncio
import csv
import cv2
import time
from copy import copy
import hashlib
import imutils
import numpy as np
from os.path import exists, join
from detector import HoopDetector, BallDetector
from keras_retinanet.utils.image import preprocess_image, resize_image
from utils import download_model, download_file_async, Rectangle, get_frame_by_index, show_images, resize_rect
import librosa as lr
from scipy.signal import find_peaks
import subprocess
import math

WIDTH = 1920
PATH_TO_HOOP_MODEL = 'keras-retinanet/hoop/resnet101_27_09.h5'
PATH_TO_BALL_MODEL = 'keras-retinanet/small_05_15.h5'
MODELS_BUCKET = 'wingwarp-nn-models'
PATH_TO_DATA_FOLDER = './data'
MIN_SCORE = 0.5

class Hoop():
    max_hoop_id = 1

    def __init__(self, coords, params):
        xmin, ymin, xmax, ymax = coords
        self.coords = tuple(coords)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        
        self.resize_ratio = params.hoop_resize_ratio
        self.frame_width = params.frame_width
        self.frame_height = params.frame_height
        self.max_shot_dist = params.max_shot_dist
        self.ball_detection_threshold = params.ball_detection_threshold
        self.watch_back_sec = params.watch_back_sec
        self.fps = params.fps
        self.is_debug = params.is_debug

        self.id = self.max_hoop_id
        Hoop.max_hoop_id += 1

        self.search_area = resize_rect(self.coords, self.resize_ratio, self.frame_width, self.frame_height)
        
        self.shot_start_frame = None
        self.next_min_detection_frame = None
        self.shots = dict()
        self.result_shots = list()
        self.prev_shot_fnum = None

    def __str__(self):
        return f'hoop: {self.id}, coords: {self.xmin}, {self.ymin}, {self.xmax}, {self.ymax}'

    def __sub__(self, other):
        c1x, c1y = self.xmin + (self.xmax - self.xmin) / 2, self.ymin + (self.ymax - self.ymin) / 2
        c2x, c2y = other.xmin + (other.xmax - other.xmin) / 2, other.ymin + (other.ymax - other.ymin) / 2
        return ((c1x - c2x) ** 2 + (c1y - c2y) ** 2) ** 1/2

    def print(self, msg):
        if not self.is_debug:
            return
        print(msg)

    def draw(self, frame):
        cv2.rectangle(frame, (self.xmin, self.ymin), (self.xmax, self.ymax), (255, 0, 0), 4)
        cv2.putText(frame, str(self.id), (self.xmin, self.ymin), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

    def ready_for_detection(self, fnum):
        return self.next_min_detection_frame is None or self.next_min_detection_frame <= fnum

    def needs_detection(self):
        return len(self.shots) > 0

    def reset(self):
        self.shot_start_frame = None
        self.next_min_detection_frame = None
        self.shots = dict()
        self.prev_shot_fnum = None

    def get_area_for_detection(self, frame):
        xmin, ymin, xmax, ymax = self.search_area
        return frame[ymin:ymax, xmin:xmax]

    def get_shots(self):
        return list(self.result_shots)

    def get_dist_to_prev_shot(self, fnum):
        if not self.result_shots:
            return 0
        return fnum - self.result_shots[-1][0] * self.fps

    def add_ball(self, ball, fnum, scale, debug_frame=None):
        if self.prev_shot_fnum is None:
            self.prev_shot_fnum = fnum
        self.print(f'Trying to add ball: {str(self)}, ball: {ball}, fnum: {fnum}')
        self.print(f'shot_start_frame: {self.shot_start_frame}, dist to prev: {fnum - self.prev_shot_fnum}')
        if self.shot_start_frame and fnum - self.prev_shot_fnum > self.max_shot_dist:
            self.print(f'Resetting as prev shot was detected more than {self.max_shot_dist} frames')
            self.reset()

        self.prev_shot_fnum = fnum

        if not self.shot_start_frame:
            self.shot_start_frame = fnum

        if len(self.shots) >= self.ball_detection_threshold:
            if self._shot_moves():
                self.print(f'Adding ball')
                self.result_shots.append((self.shot_start_frame / self.fps, fnum / self.fps))
                self.reset()
                self.next_min_detection_frame = fnum + self.watch_back_sec * self.fps
                self.print(f'next_min_detection_frame: {self.next_min_detection_frame}, res_shots: {self.result_shots}')
            else:
                self.print(f'The ball is not moving - not adding it')
                self.reset()

        self.shots[fnum] = convert_by_scale(ball, scale)
        if debug_frame is not None:
            xmin, ymin, xmax, ymax = self.search_area
            res_debug_frame = debug_frame[ymin:ymax, xmin:xmax]
            cv2.putText(res_debug_frame, f'{int(fnum)}, {self.id}', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            cxmin, cymin, cxmax, cymax = self.shots[fnum]
            cv2.rectangle(res_debug_frame, (cxmin, cymin), (cxmax, cymax), (255, 0, 0), 4)
                    
            return res_debug_frame

    def _shots_differ(self, shot1, shot2):
        print(f'shot1: {shot1}, shot2: {shot2}')
        diff = tuple(abs(c2 - c1) > self.ball_detection_threshold / 3 for (c1, c2) in zip(shot1, shot2))
        print(f'shots_differ: {any(diff)}')
        return any(diff)

    def _shot_moves(self):
        print(f'shots: {self.shots}')
        frames = list(self.shots.keys())
        moving_shots = 0
        shots_num = len(frames)
        for i in range(shots_num):
            if not i:
                continue
            if self._shots_differ(self.shots[frames[i]], self.shots[frames[i-1]]):
                moving_shots += 1
            print(f'moving_shots: {moving_shots}, shots_num: {shots_num}')
        return moving_shots >= shots_num / 3


class ShotDetector():
    def __init__(self, **params):
        self.hoop_backbone_name = params.get('hoop_backbone_name', 'resnet101')
        self.ball_backbone_name = params.get('ball_backbone_name', 'resnet50')
        
        if params.get('hoop_detector'):
            self.hoop_detector = params['hoop_detector']
            self.ball_detector = params['ball_detector']
        else:
            min_score = params.get('min_score', MIN_SCORE)
            self.hoop_detector = HoopDetector(
                params['hoop_model_path'], min_score, self.hoop_backbone_name
            )
            self.ball_detector = HoopDetector(
                params['ball_model_path'], min_score, self.ball_backbone_name
            )
        
        self.watch_back_sec = params.get('watch_back_sec', 5)
        self.applause_segments = self._prepare_applause_segments(params['applause_segments'])
        self.curr_segment = self.applause_segments.pop()
        self.visualize = params.get('visualize', False)
        self.is_notebook = params.get('is_notebook', False)
        self.debug_frames = list()
        self.shots = dict()

        self.path_to_data_folder = params.get('path_to_data_folder', PATH_TO_DATA_FOLDER)
        self.name = params['name']
        self.vid_path = params['path_to_video']
        self.cap = cv2.VideoCapture(self.vid_path)
        self.frame_width =  min(WIDTH, self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) - 1)
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 1
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fnum = 1
        self.back_sub = cv2.createBackgroundSubtractorMOG2()
        self.hoop_resize_ratio = params.get('hoop_resize_ratio', 0.5)
        self.background_look_back_frames = params.get('background_look_back_frames', 20)
        self.is_debug = params.get('is_debug', False)
        self.do_not_override_res = params.get('do_not_override_res', False)
        self.csv_path = f"{self.path_to_data_folder}/{self.name}_audio_shot_detection.csv"
        self.max_fnum = None
        if params.get('max_sec', None):
            self.max_fnum = int(params['max_sec'] * self.fps)

        # num of balls to detect in order to consider an interval a shot
        self.ball_detection_threshold = params.get('ball_detection_threshold', 10)
        # max distance between detected shots to be considered ok
        self.max_shot_dist = params.get('max_shot_dist', 5)

        self.hoops = list()
        self.shots = list()

    def print(self, msg):
        if not self.is_debug:
            return
        print(msg)

    def _prepare_applause_segments(self, applause_segments):
        res_segments = list()
        for i in range(len(applause_segments)):
            segment = applause_segments[i]
            if not i: 
                res_segments.append(segment)
                continue
            curr_start_sec = segment[0]
            prev_end_sec = res_segments[-1][1]
            if curr_start_sec - prev_end_sec < self.watch_back_sec:
                res_segments[-1] = (res_segments[-1][0], segment[1])
                continue
            res_segments.append(segment)
        res_segments.reverse()
        return res_segments

    def _build_frame_for_detection(self, apply_back_sub=True, resize=None, frame=None):
        if frame is None:
            frame = self.frame
        if apply_back_sub:
            mask = self.back_sub.apply(frame)
            mask = cv2.dilate(mask, None)
            mask = cv2.GaussianBlur(mask, (15, 15),0)
            _,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            anded_frame = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            anded_frame = frame
        image = preprocess_image(anded_frame)
        if resize is not None:
            processed_frame, scale = resize_image(anded_frame, min_side=resize)
        else:
            processed_frame, scale = resize_image(anded_frame)

        return processed_frame, anded_frame, scale

    def filter_hoops(self):
        if len(self.hoops) > 4:
            return
        res = list()
        for i in range(len(self.hoops)):
            for j in range(i + 1, len(self.hoops)):
                res.append((i, j, self.hoops[i] - self.hoops[j]))
        res_sorted = sorted(res, key=lambda tup: tup[2], reverse=True)
        best_pair = res_sorted[0]
        hoop1, hoop2 = self.hoops[best_pair[0]], self.hoops[best_pair[1]]
        self.hoops = [hoop1, hoop2]

    def find_hoops(self):
        predicted_hoops = self.hoop_detector.process_frame(self.frame)
        if predicted_hoops is None:
            return False

        for hoop_num, hoop in enumerate(predicted_hoops[0]):
            self.hoops.append(Hoop(hoop, self))

        if self.visualize:
            hoop_frame = self.frame.copy()
            for hoop in self.hoops:
                self.print(hoop)
                hoop.draw(hoop_frame)
            self.debug_frames.append(hoop_frame)

        self.filter_hoops()
        if self.visualize:
            hoop_frame = self.frame.copy()
            for hoop in self.hoops:
                self.print(hoop)
                hoop.draw(hoop_frame)
            self.debug_frames.append(hoop_frame)

        return True

    def show(self):
        if not self.visualize:
            return
        
        self.print(self.shots)
        
        if self.is_notebook:
            for i in range(0, len(self.debug_frames), 10):
                try:
                    show_images(self.debug_frames[i:i + 10])
                except Exception as e:
                    pass
            return

        for frame in self.debug_frames:
            cv2.imshow("debug_frame", frame)
            key = cv2.waitKey(0)
            while key not in [ord('q'), ord('k')]:
                key = cv2.waitKey(0)
            if key == ord('q'):
                break

    def _has_enough_shot_detections(self):
        for hoop_num, balls_detected in self.balls_detected_num.items():
            if balls_detected >= self.ball_detection_threshold:
                return True, hoop_num
        return False, None

    def _reset_hoop_data(self):
        for hoop in self.hoops:
            hoop.reset()

    def get_curr_segment_fnums(self):
        start_sec, end_sec = self.curr_segment
        return int(start_sec * self.fps), int(end_sec * self.fps)

    def get_next_detection_fnum(self):
        start_fnum, end_fnum = self.get_curr_segment_fnums()
        next_detection_fnum = start_fnum - self.background_look_back_frames
        if next_detection_fnum <= self.fnum:
            return None
        return next_detection_fnum

    def _run_detection(self):
        start_fnum, end_fnum = self.get_curr_segment_fnums()
        self.print(f'Checking if run detection, fnum: {self.fnum}, start_fnum: {start_fnum}, end_fnum: {end_fnum}')
        if self.fnum < start_fnum:
            return False, [], self.get_next_detection_fnum()
        if self.fnum > end_fnum:
            need_detection = [hoop for hoop in self.hoops if hoop.ready_for_detection(self.fnum) and hoop.needs_detection()]
            if need_detection:
                return True, need_detection, None
            self._reset_hoop_data()
            if self.applause_segments:
                self.curr_segment = self.applause_segments.pop()
            return False, [], self.get_next_detection_fnum()
        
        hoops_ready_for_detection = [hoop for hoop in self.hoops if hoop.ready_for_detection(self.fnum)]
        return len(hoops_ready_for_detection) > 0, hoops_ready_for_detection, None

    def _find_shots(self, scale, anded_frame, hoops_need_detection):
        for hoop in hoops_need_detection:
            area_for_detection = hoop.get_area_for_detection(anded_frame)
            _processed_frame, _orig_background_sub_frame, _scale = self._build_frame_for_detection(frame=area_for_detection, apply_back_sub=False, resize=200)
            predicted_cropped_balls = self.ball_detector.process_frame(_processed_frame)
            if predicted_cropped_balls is not None:
                balls_num = len(predicted_cropped_balls[0])
                self.print(f'Found {balls_num} balls on frame: {self.fnum} on hoop {hoop}, balls: {predicted_cropped_balls[0]}')
                debug_frame = None
                if self.visualize:
                    debug_frame = self.frame.copy()
                if balls_num == 1:
                    res_debug_frame = hoop.add_ball(predicted_cropped_balls[0][0], self.fnum, _scale, debug_frame=debug_frame)
                    self.debug_frames.append(res_debug_frame)

    def _add_shots(self):
        shots = list()
        for hoop in self.hoops:
            hoop_shots = hoop.get_shots()
            for start, end in hoop_shots:
                start, end = round(start, 2), round(end, 2)
                shots.append((start, end, hoop.coords))
        res_shots = sorted(shots, key=lambda tup: tup[0])
        final_shots = list()
        for i in range(len(res_shots)):
            shot = res_shots[i]
            if not i: 
                final_shots.append(shot)
                continue
            curr_start_sec = shot[0]
            prev_end_sec = final_shots[-1][1]
            if curr_start_sec - prev_end_sec < 5:
                final_shots[-1] = (final_shots[-1][0], shot[1], shot[2])
                continue
            final_shots.append(shot)
        self.shots = final_shots

    def write_shots(self):
        self._add_shots()
        res = list()
        for num, detection in enumerate(self.shots):
            res.append({
                'id': num,
                'start_sec': detection[0],
                'end_sec': detection[1],
                'hoop_coords': detection[2],
            })
        
        with open(self.csv_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=('id', 'start_sec', 'end_sec', 'hoop_coords'))
            writer.writeheader()
            for data in res:
                writer.writerow(data)

    @staticmethod
    def build_video(vid_path, name, shots, path_to_data_folder='./data', max_sec=None):
        cap = cv2.VideoCapture(vid_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        debug_path = f"{path_to_data_folder}/{name}_audio_shot_debug.mp4"
        print(debug_path)
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        writer = cv2.VideoWriter(
            debug_path, fourcc, int(fps), (width, height)
        )
        frame_width =  min(WIDTH, cap.get(cv2.CAP_PROP_FRAME_WIDTH) - 1)
        scale = width / frame_width
        fnum = 0
        next_shot = None
        shots = list(shots)
        shots.reverse()
        success, image = cap.read()
        while success:
            fsec = fnum / fps
            if max_sec is not None and fsec > max_sec:
                break
            frame = image.copy()
            cv2.putText(frame, f'frame {str(fnum)}', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)

            if next_shot is None and shots:
                next_shot = shots.pop()

            is_shot = False
            if next_shot is not None:
                next_shot_start, next_shot_end, hoop_coords = next_shot
                is_shot = next_shot_start <= fsec and next_shot_end >= fsec
                if fsec > next_shot_end:
                    next_shot = None

            if is_shot:
                print('Is shot')
                xmin, ymin, xmax, ymax = convert_by_scale(hoop_coords, 1 / scale)
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)

            fnum += 1
            success, image = cap.read()
            writer.write(frame)
        cap.release()
        writer.release()

    def detect(self):
        if self.do_not_override_res and exists(self.csv_path):
            print('Csv file exists, terminating')
            return

        ret, self.frame = self.cap.read()
        if not ret:
            self.print(f'Unable to read video')
            return
        self.frame = imutils.resize(self.frame, width=WIDTH)
        processed_frame, anded_frame, scale = self._build_frame_for_detection()

        found_hoops = self.find_hoops()
        if not found_hoops:
            self.print("No hooops found")
            return

        while True:
            if not self.curr_segment:
                self._add_shots()
                self.print("Got to the final segment")
                break

            run_detection, hoops_to_use, next_fnum_to_use = self._run_detection()
            self.print(f'run_detection: {run_detection}, next_fnum_to_use: {next_fnum_to_use}, hoops_to_use: {hoops_to_use}')
            if next_fnum_to_use is not None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, next_fnum_to_use)
                self.fnum = next_fnum_to_use
                continue

            ret, self.frame = self.cap.read()
            if not ret:
                break
            self.frame = imutils.resize(self.frame, width=WIDTH)
            self.fnum += 1
            if self.max_fnum is not None and self.fnum >= self.max_fnum:
                self.print('Reached max frame, terminating')
                break

            # self.print(f'Processing frame {self.fnum}')

            if not run_detection:
                # self.print(f'No detection needed')
                processed_frame, anded_frame, scale = self._build_frame_for_detection()
                continue
            
            hoops_need_detection = [hoop for hoop in self.hoops if hoop.ready_for_detection(self.fnum) and hoop.needs_detection()]
            if self.fnum % 2 == 0:
                if not hoops_need_detection:
                    processed_frame, anded_frame, scale = self._build_frame_for_detection()
                    continue
                hoops_to_use = hoops_need_detection

            # self.print(f'Running detection for hoops: {"   ".join([str(h) for h in hoops_to_use])}')
            self._find_shots(scale, anded_frame, hoops_to_use)

            processed_frame, anded_frame, scale = self._build_frame_for_detection()
        self._add_shots()
        self.write_shots()
        self.print(f'Detection is finished')


def convert_by_scale(init_box, scale):
    box = np.array(init_box)
    box_scaled = box / scale
    res = box_scaled[:4]
    xmin, ymin, xmax, ymax = res
    return (int(xmin), int(ymin), int(xmax), int(ymax))


def get_applause_segments(path_to_video, name, folder='./data', min_peak_height=0.3, max_peak_dist=10000, min_seg_len_sec=2):
    audio_file = f"{folder}/{name}.wav"
    if not exists(audio_file):
        subprocess.call(
            ["ffmpeg", "-y", "-i", path_to_video, audio_file], 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

    y, sr = lr.load(audio_file)
    audio_len = lr.get_duration(filename=audio_file)
    points_per_sec = len(y) / audio_len
    peaks, _ = find_peaks(y, height=min_peak_height)
    segments = list()
    is_segment = False
    seg_start = None
    for i in range(len(peaks)):
        if not i:
            continue
        peak = peaks[i]
        dist_to_prev_peak = peak - peaks[i-1]
        if dist_to_prev_peak > max_peak_dist:
            if is_segment and (peaks[i-1] - seg_start) / points_per_sec >= min_seg_len_sec:
                segments.append((seg_start, peaks[i-1]))
            is_segment = False
            seg_start = None
            continue
        is_segment = True
        if not seg_start:
            seg_start = peak
    if is_segment and (peaks[-1] - seg_start) / points_per_sec >= min_seg_len_sec:
        segments.append((seg_start, peaks[-1]))

    return [(seg_start / points_per_sec, seg_end / points_per_sec) for seg_start, seg_end in segments]


def get_models(
        path_to_hoop_model=PATH_TO_HOOP_MODEL, path_to_ball_model=PATH_TO_BALL_MODEL, models_bucket=MODELS_BUCKET
    ):
    return {
        'ball_model_path': download_model(models_bucket, path_to_ball_model),
        'hoop_model_path': download_model(models_bucket, path_to_hoop_model)
    }


async def prepare_video(video_url, path_to_vid=None, path_to_data_folder=PATH_TO_DATA_FOLDER):
    path_to_video = path_to_vid
    name = None
    if not path_to_video:
        name = hashlib.md5(video_url.encode('utf-8')).hexdigest()
        path_to_video = join(path_to_data_folder, f'{name}.mp4')
        if not exists(path_to_video):
            await download_file_async(video_url, path_to_video)
    if not name:
        name = path_to_video.split('/')[-1].split('.')[0]
    
    applause_segments = get_applause_segments(path_to_video, name)
    return {
        'path_to_video': path_to_video,
        'name': name,
        'applause_segments': applause_segments
    }


async def process_video(common_params, video_url, path_to_video=None, path_to_data_folder=PATH_TO_DATA_FOLDER):
    vid_params = await prepare_video(video_url, path_to_vid=path_to_video, path_to_data_folder=path_to_data_folder)
    vid_params = {
        **common_params,
        **vid_params
    }
    shot_detector = ShotDetector(**vid_params)
    shot_detector.detect()
    shot_detector.show()

    return f'{path_to_data_folder}/{vid_params["name"]}_audio_shot_detection.csv'


async def main(path_to_hoop_model, path_to_ball_model, models_bucket, min_score, local_vid_path, video_url, path_to_data_folder, visualize, is_notebook):
    params = get_models(
        path_to_hoop_model=path_to_hoop_model, path_to_ball_model=path_to_ball_model, models_bucket=models_bucket
    )
    params = {
        **params,
        'min_score': min_score,
        'visualize': visualize,
        'is_notebook': is_notebook,
        'path_to_data_folder': path_to_data_folder
    }
    await process_video(params, video_url, path_to_video=local_vid_path, path_to_data_folder=path_to_data_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect shots using both audio and image')
    parser.add_argument('--path_to_hoop_model', default=PATH_TO_HOOP_MODEL, help='path to model in models bucket')
    parser.add_argument('--path_to_ball_model', default=PATH_TO_BALL_MODEL, help='path to model in models bucket')
    parser.add_argument('--models_bucket', default=MODELS_BUCKET, help='name of a bucket with models')
    parser.add_argument('--path_to_vid', default=None, help='local path to video')
    parser.add_argument('--video_url', help='url of a video for shots tracking')
    parser.add_argument('--min_score', default=MIN_SCORE, help='minimum score of predicted box to use')
    parser.add_argument('--path_to_data_folder', default=PATH_TO_DATA_FOLDER, help='path to data folder')
    parser.add_argument('-v', action='store_true', help='visualize')
    parser.add_argument('-n', action='store_true', help='set true if run in notebook')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.path_to_hoop_model, args.path_to_ball_model, args.models_bucket, float(args.min_score), args.path_to_vid, args.video_url, args.path_to_data_folder, args.v, args.n))
