import argparse
import csv
from os import path
import os.path
from os.path import isfile, join, exists
from bisect import bisect_left
from os import listdir
import requests
import hashlib
from ww_audio_shot_detection.config import base_s3_url, path_to_shot_frames
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION = 'us-west-2'
BOTO3_PARAMS = {'region_name': REGION, 'aws_access_key_id': AWS_ACCESS_KEY_ID, 'aws_secret_access_key': AWS_SECRET_ACCESS_KEY}
REGION = 'us-west-2'

def create_md5_sig(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_file(url, local_file_path, with_heartbeat=True):
    # NOTE the stream=True parameter below
    print("with with_heartbeat")
    with requests.get(url, stream=True) as r:
        with open(local_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=51200): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #yield chunk


def get_files_in_dir(dir_name):
    return [f for f in listdir(dir_name) if isfile(join(dir_name, f))]


def func_not_found():
    print("func_not_found")

class Frame:
    def __init__(self, fnum, x, y, size, is_occluded):
        self.fnum = fnum
        self.x = x
        self.y = y
        self.size = size
        self.is_occluded = is_occluded

class PreciseFrame:
    def __init__(self,fnum, x,y,w,h, auto=True):
        self.fnum = int(fnum)
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.auto = auto

    @property
    def auto_str(self):
    	return "1" if self.auto else "0"

class FrameSet:
    def __init__(self, csv_path, scaler=1, ftype="precise"):
        assert(ftype in ["precise", "big"])
        self.ftype = ftype
        self.frames = {}
        self.scaler=scaler
        self.csv_path = csv_path
        if not path.exists(csv_path):
            directory, _ = os.path.split(csv_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            self.curr_index = -1
            return

        with open(csv_path, newline='') as csvfile:
            for row in csvfile:
                try:
                    deserialize_func = getattr(self,"_deserialize_" + self.ftype, func_not_found)
                    frame = deserialize_func(row)
                    self.frames[frame.fnum] = frame
                except Exception as e:
                    print("excpetion", e)

        if self.frames:
            self.curr_index = max(self.frames.keys())


    def __iter__(self):
    	for fnum, frame in self.frames.items():
    		yield fnum, frame

    def __setitem__(self, idx, frame):
        self.frames[idx] = frame

    def __getitem__(self, idx):
        if idx not in self.frames:
            return None
        return self.frames[idx]

    def __delitem__(self,  idx):
    	if idx in self.frames:
    		del self.frames[idx]


    def write(self):
        recorded_frames = self.frames.keys()
        max_frame = max(recorded_frames)
        min_frame = min(recorded_frames)
        header_func = getattr(self,"_header_" + self.ftype, func_not_found)
        print("header", header_func())
        row_func = getattr(self,"_get_" + self.ftype + "_row", func_not_found) 
        with open(self.csv_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=header_func())
            writer.writeheader()
            writer = csv.writer(file)
            for idx, f in self.frames.items():
                writer.writerow(row_func(f))

        print("File saved to %s" % self.csv_path)

    """
    Frame parsing funcs
    """
    def _deserialize_precise(self, csv_row):
        row = [float(r) for r in csv_row.split(",")]
        auto_det = True if len(row) == 6 and row[5] == "1" else False
        return PreciseFrame(int(row[0]), row[1] * self.scaler, row[2] * self.scaler, row[3] * self.scaler, row[4] * self.scaler)

    def _get_precise_row(self, pf):
        return [pf.fnum,pf.x/self.scaler, pf.y/self.scaler, pf.w/self.scaler, pf.h/self.scaler, pf.auto_str]

    def _header_precise(self):
        return ["frame", "x", "y", "w", "h", "auto"]

    def _deserialize_big(self, csv_row):
        row = [float(r) for r in csv_row.split(",")]
        is_occluded = True if row[4] == 1 else False
        return Frame(int(row[0]), 
            int(max(0, int(row[1])) * self.scaler), 
            int(max(int(row[2]), 0) * self.scaler), 
            int(int(row[3]) * self.scaler), 
            is_occluded)

    def _get_big_row(self, bf):
        return [bf.fnum,bf.x/self.scaler, bf.y/self.scaler, bf.size/self.scaler, int(bf.is_occluded)]

    def _header_big(self):
        return ["frame", "x", "y", "boundSize", "occluded"]



def find_idx(x, arr):
    i = bisect_left(arr, x)
    if i != len(arr) and arr[i] == x:
        return True, i
    elif 0 <= i < len(arr):
    	return False, i
    else:
    	print("i", i)
    	return False, None

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def download_model(models_bucket, path_to_model_in_bucket, local_path=None):
    model_url = base_s3_url % models_bucket + path_to_model_in_bucket
    local_model_path = local_path or path_to_model_in_bucket.split("/")[-1]
    print(local_model_path)
    
    if not exists(local_model_path):
        download_file(model_url, local_model_path)
    
    return local_model_path

def show_images(images, cols = 1, titles = None):
    """Display a list of images in a single figure with matplotlib.
    
    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.
    
    cols (Default = 1): Number of columns in figure (number of rows is 
                        set to np.ceil(n_images/float(cols))).
    
    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.show()


async def get(session, url):
    if session.closed:
        return

    resp = await session.request('GET', url=url, timeout=None)
    data = await resp.read()
    return data


class TooManySegments(Exception):
    pass


def uploadDirectoryS3(path, bucketname, prefix):
    for root,dirs,files in os.walk(path):
        for file in files:
            s3.upload_file(os.path.join(root,file), bucketname, prefix + '/' + file)


def get_path_to_shot_frame(vid_name, frame_num):
    return join(path_to_shot_frames, f'{vid_name}_{frame_num}.png')


def get_frame_by_index(cap, frame_num):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    success, frame = cap.read()
    return frame


def resize_rect(rect, delta_ratio, max_w, max_h, delta_x=None, delta_y=None):
    xmin, ymin, xmax, ymax = rect
    new_xmin, new_ymin, new_xmax, new_ymax = rect
    
    if delta_x is not None or delta_y is not None:
        if delta_x is not None:
            new_xmin = xmin + delta_x
            new_xmax = xmax + delta_x
        if delta_y is not None:
            new_ymin = ymin + delta_y
            new_ymax = ymax + delta_y
    else:
        w, h = xmax - xmin, ymax - ymin
        new_ymin = ymin - h * delta_ratio / 2
        new_xmin = xmin - w * delta_ratio / 2
        w = w * (1 + delta_ratio)
        h = h * (1 + delta_ratio)
        new_xmax = new_xmin + w
        new_ymax = new_ymin + h

    
    new_xmin = int(min(max(new_xmin, 0), max_w))
    new_ymin = int(min(max(new_ymin, 0), max_h))
    new_xmax = int(min(max(new_xmax, 0), max_w))
    new_ymax = int(min(max(new_ymax, 0), max_h))

    return new_xmin, new_ymin, new_xmax, new_ymax


def dist_between_rects(rect1, rect2):
    pxmin, pymin, pxmax, pymax = rect1
    pxmin, pymin, pxmax, pymax = int(pxmin), int(pymin), int(pxmax), int(pymax)
    c1x, c1y = pxmin + (pxmax - pxmin) / 2, pymin + (pymax - pymin) / 2
    cxmin, cymin, cxmax, cymax = rect2
    cxmin, cymin, cxmax, cymax = int(cxmin), int(cymin), int(cxmax), int(cymax)
    c2x, c2y = cxmin + (cxmax - cxmin) / 2, cymin + (cymax - cymin) / 2
    return math.sqrt((c2x - c1x) ** 2 + (c2y - c1y) ** 2)


# returns positives if rect1 is inside rect 2
def dist_between_rects_borders(rect1, rect2):
    xmin1, ymin1, xmax1, ymax1 = rect1
    xmin2, ymin2, xmax2, ymax2 = rect2
    print(f'rect1: {rect1}, rect2: {rect2}')

    return {
        "left": xmin1 - xmin2,
        "top": ymax2 - ymax1,
        "right": xmax2 - xmax1,
        "bottom": ymin1 - ymin2
    }


def rect_square(rect):
    xmin, ymin, xmax, ymax = rect
    return (xmax - xmin) * (ymax - ymin)


def angle_between_vectors(v1, v2):
    unit_v1 = v1 / np.linalg.norm(v1)
    unit_v2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_v1, unit_v2)
    return np.arccos(dot_product)


def get_vid_csv_data(path_to_file):
    res = dict()
    with open(path_to_file) as f:
        f.readline()
        for l in f:
            line = tuple()
            frame, *line = l.strip().split(",")
            res[int(frame)] = res.get(int(frame), list())
            res[int(frame)].append(line)
    return res