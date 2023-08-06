import os.path

IMAGE_DIR_PREFIX = "pngs"
BOXED_IMAGE_DIR_PREFIX = "boxed"
ANNOT_DIR_PREFIX = "voc"
MODIFIED_ANNOT_DIR_PREFIX = "modified_voc"

def precise_path(vid_path):
    directory, filename = os.path.split(vid_path)
    filename = "precise_" + filename.replace("mp4", "csv")
    return os.path.join(directory, filename)

def annotation_dir(vid_path):
    return vid_path.split(".mp4")[0] + "_annotations"

def big_box_path(vid_path):
    return vid_path.replace('.mp4', '.csv')

def annotation_img_dir(vid_path):
    return os.path.join(annotation_dir(vid_path), IMAGE_DIR_PREFIX)

def annotation_preview_dir(vid_path):
    return os.path.join(annotation_dir(vid_path), BOXED_IMAGE_DIR_PREFIX)

def annotation_voc_dir(vid_path):
    return os.path.join(annotation_dir(vid_path), ANNOT_DIR_PREFIX)

def modified_voc_dir(vid_path):
    return os.path.join(annotation_dir(vid_path), MODIFIED_ANNOT_DIR_PREFIX)