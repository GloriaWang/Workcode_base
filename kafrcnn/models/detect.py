import os
import sys
import cv2
import argparse
import numpy as np
from utils.timer import Timer
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from kafrcnn.config import NETS
from kafrcnn.structs import ObjectDetection
from kafrcnn.utils import resolve_file_path


"""
MARKED FOR DELETION
"""


def parse_args():
    """
    Parse input argument
    """
    parser = argparse.ArgumentParser(
        description='Faster R-CNN bbox processing script')

    parser.add_argument(
        '--net',
        dest='test_net',
        help='Network to use [vgg16]',
        choices=NETS.keys(),
        default='vgg16')

    parser.add_argument(
        '--caffemodel',
        dest='custom_caffemodel',
        help='Path to caffemodel weights to load',
        type=str,
        default='')

    parser.add_argument(
        '--rpn',
        dest='use_rpn',
        help='Use RPN instead of selective search',
        default=True,
        type=bool)

    parser.add_argument(
        '--gpu',
        dest='gpu_id',
        help='GPU device id to use',
        default=0,
        type=int)

    parser.add_argument(
        '--cpu',
        dest='cpu_mode',
        help='Use CPU mode (overrides --gpu)',
        action='store_true')

    parser.add_argument(
        '--conf',
        dest='det_conf_thresh',
        help='Min. detection confidence threshold',
        default=0.5,
        type=float)

    parser.add_argument(
        '--nms',
        dest='det_nms_thresh',
        help='Non-Max-Suppression threshold',
        default=0.3,
        type=float)

    parser.add_argument(
        '--N',
        dest='max_num_images',
        help='Maximum number of images to process in <IMAGES_PATH>',
        default=0,
        type=int)

    parser.add_argument(
        '--pklpath',
        dest='dets_pkl_path',
        help='Path of the detection resulte file',
        default='',
        type=str)

    parser.add_argument(
        '--vis',
        dest='save_overlay',
        help='Render and save images overlaid with detections',
        action='store_true')

    parser.add_argument(
        '--vispath',
        dest='overlay_path_header',
        help='Path header to save overlaid images',
        default='',
        type=str)

    parser.add_argument(
        '--image_list',
        dest='image_list')

    parser.add_argument(
        'images_path',
        help='Path to image file or folder to be processed')

    args = parser.parse_args()
    return args


def process_image(net, net_class_names, target_class_colors, im_file, args):
    """
    Process images for teh detection
    """
    dets = []

    # Load image
    im = cv2.imread(im_file)
    if im is None:
        print 'Skipping bad image: ', im_file
        return dets

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()

    # Filter and store detections
    recog_counts = dict()
    for cls_ind, cls in enumerate(net_class_names):
        if cls not in target_class_colors:
            continue

        cls_boxes = boxes[:, 4 * cls_ind: 4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        cls_box_scores = np.hstack(
            (cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)

        idx_nms_keep = nms(cls_box_scores, args.nms_thresh)
        cls_box_scores = cls_box_scores[idx_nms_keep, :]

        idx_conf_keep = np.where(
            cls_box_scores[:, -1] >= args.conf_thresh)[0]

        recog_counts[cls] = len(idx_conf_keep)

        if len(idx_conf_keep) <= 0:
            continue
        cls_box_scores = cls_box_scores[idx_conf_keep, :]

        for idx in xrange(len(idx_conf_keep)):
            bbox = cls_box_scores[idx, :4]
            score = cls_box_scores[idx, 4]
            dets.append(
                ObjectDetection(cls, bbox[0], bbox[1], bbox[2], bbox[3], score)
            )

    # ToDo: this should be logged, not printed
    stats_str = ('model=%s, min_conf=%.2f, nms_thresh=%.2f\nelapsed=%.3fs'
                 'for %d proposals\ncounts: %s' % (args.test_net,
                                                   args.conf_thresh,
                                                   args.nms_thresh,
                                                   timer.total_time,
                                                   boxes.shape[0],
                                                   str(recog_counts)))
    print stats_str
    return dets


def load_image_paths(args):
    """
    Loads the images
    ToDo: this method could be refactored
    """
    image_paths = []

    if len(args.images_path) > 0 and os.path.isdir(args.images_path):
        with open(args.image_list) as f:
            flist = f.read().splitlines()
        for file_path in os.listdir(args.images_path):
            file_base, file_ext = os.path.splitext(file_path)
            if len(file_base) > 7 and file_base[:7] == '_frcnn_':
                continue
            file_ext = file_ext.lower()
            if (file_base not in flist):
                continue
            if (file_ext == '.jpg' or
               file_ext == '.jpeg' or
               file_ext == '.png' or
               file_ext == '.bmp'):
                image_paths.append(os.path.join(args.images_path, file_path))
    else:
        image_path = resolve_file_path(args.images_path)
        if image_path is None:
            print 'Image path not found: %s' % args.images_path
            sys.exit(-1)
        image_paths.append(image_path)
    return image_paths
