import os

# import keras
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.gpu import setup_gpu
import numpy as np

from keras.models import Model
import keras_retinanet.layers as layers

# use this to change which GPU to use
gpu = 0

# set the modified tf session as backend in keras
setup_gpu(gpu)

# import the necessary packages
import numpy as np
# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh, labels=None):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes 
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type
    result_labels = None
    if labels is not None:
        result_labels = labels[pick]
    return boxes[pick].astype("int"), result_labels

class BallDetector:
    def __init__(self, model_path, backbone_name='resnet50'):
        self.ball_model = models.load_model(model_path, backbone_name=backbone_name)
        self.ball_model = models.convert_model(self.ball_model)

    def process_frame(self, frame):
        assert(frame.shape[2] == 3)
        img_copy = frame.copy()
        img_copy = preprocess_image(img_copy)
        try:
            img_copy, scale = resize_image(img_copy, min_side=200,max_side=200)
        except ZeroDivisionError:
            return None

        boxes, scores, labels = self.ball_model.predict_on_batch(np.expand_dims(img_copy, axis=0))
        boxes /= scale
        high_confidence_boxes = []
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < 0.5:
                break
            high_confidence_boxes.append(box)
        if not high_confidence_boxes:
            return None
        nms_boxes = non_max_suppression_fast(np.array(high_confidence_boxes), .5)
        return nms_boxes[0]


class HoopDetector:
    def __init__(self, model_path, min_score, backbone_name):
        self.hoop_model = models.load_model(model_path, backbone_name=backbone_name)
        self.hoop_model = models.convert_model(self.hoop_model)
        boxes, classification = self.hoop_model.layers[-2].output, self.hoop_model.layers[-1].output
        detections = layers.FilterDetections(
                nms                   = True,
                class_specific_filter = True,
                name                  = 'filtered_detections',
                nms_threshold         = 0.5,
                score_threshold       = 0.05,
                max_detections        = 10,
                parallel_iterations   = 32
            ) ([boxes, classification])
       
        self.hoop_model = Model(self.hoop_model.input, detections)
        self.min_score = min_score

    def process_frame(self, frame):
        assert(frame.shape[2] == 3)
        img_copy = frame.copy()
        img_copy = preprocess_image(img_copy)

        boxes, scores, labels = self.hoop_model.predict_on_batch(np.expand_dims(img_copy, axis=0))
        high_confidence_boxes = []
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < self.min_score:
                break
            high_confidence_boxes.append(box)
        if not high_confidence_boxes:
            return None
        nms_boxes = non_max_suppression_fast(np.array(high_confidence_boxes), .5)
        return nms_boxes


class ShotDetector:
    def __init__(self, model_path, min_score, backbone_name):
        self.shot_model = models.load_model(model_path, backbone_name=backbone_name)
        self.shot_model = models.convert_model(self.shot_model)
        boxes, classification = self.shot_model.layers[-2].output, self.shot_model.layers[-1].output
        detections = layers.FilterDetections(
                nms                   = True,
                class_specific_filter = True,
                name                  = 'filtered_detections',
                nms_threshold         = 0.5,
                score_threshold       = 0.05,
                max_detections        = 10,
                parallel_iterations   = 32
            ) ([boxes, classification])
       
        self.shot_model = Model(self.shot_model.input, detections)
        self.min_score = min_score

    def process_frame(self, frame):
        assert(frame.shape[2] == 3)
        img_copy = frame.copy()
        img_copy = preprocess_image(img_copy)

        boxes, scores, labels = self.shot_model.predict_on_batch(np.expand_dims(img_copy, axis=0))
        high_confidence_boxes, high_confidence_labels = [], []
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < self.min_score:
                break
            high_confidence_boxes.append(box)
            high_confidence_labels.append(label)
        if not high_confidence_boxes:
            return None, None
        nms_boxes, labels = non_max_suppression_fast(np.array(high_confidence_boxes), .5, labels=np.array(high_confidence_labels))
        return nms_boxes, labels
