import os
from fast_rcnn.config import cfg

# This script contains common imports and constants

PARQ_CACHE_DIR = './cache/'

COCO_CLASSES = (
    '__background__', u'person', u'bicycle', u'car', u'motorcycle',
    u'airplane', u'bus', u'train', u'truck', u'boat', u'traffic light',
    u'fire hydrant', u'stop sign', u'parking meter', u'bench', u'bird',
    u'cat', u'dog', u'horse', u'sheep', u'cow', u'elephant', u'bear',
    u'zebra', u'giraffe', u'backpack', u'umbrella', u'handbag', u'tie',
    u'suitcase', u'frisbee', u'skis', u'snowboard', u'sports ball', u'kite',
    u'baseball bat', u'baseball glove', u'skateboard', u'surfboard',
    u'tennis racket', u'bottle', u'wine glass', u'cup', u'fork', u'knife',
    u'spoon', u'bowl', u'banana', u'apple', u'sandwich', u'orange',
    u'broccoli', u'carrot', u'hot dog', u'pizza', u'donut', u'cake', u'chair',
    u'couch', u'potted plant', u'bed', u'dining table', u'toilet', u'tv',
    u'laptop', u'mouse', u'remote', u'keyboard', u'cell phone', u'microwave',
    u'oven', u'toaster', u'sink', u'refrigerator', u'book', u'clock', u'vase',
    u'scissors', u'teddy bear', u'hair drier', u'toothbrush')

VOC_CLASSES = (
    '__background__', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor')

TARGET_CLASS_COLORS = {
    'car': 'lawngreen',
    'bus': 'yellow',
    'bicycle': 'red',
    'motorbike': 'red',
    'motorcycle': 'red'}

NETS = {
    'vgg16': (os.path.join(
        cfg.MODELS_DIR, 'VGG16', 'faster_rcnn_alt_opt', 'faster_rcnn_test.pt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'VGG16_faster_rcnn_final.caffemodel'),
        True),
    'zf': (os.path.join(
        cfg.MODELS_DIR, 'ZF', 'faster_rcnn_alt_opt', 'faster_rcnn_test.pt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'ZF_faster_rcnn_final.caffemodel'),
        True),
    'coco': (os.path.join(
        cfg.MODELS_DIR, '..', 'coco', 'VGG16', 'faster_rcnn_end2end', 'test.prototxt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'coco_vgg16_faster_rcnn_final.caffemodel'),
        False)}

RPNS = {
    'vgg16': (os.path.join(
        cfg.MODELS_DIR, 'VGG16', 'faster_rcnn_alt_opt', 'rpn_test.pt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'VGG16_faster_rcnn_final.caffemodel'),
        True),
    'zf': (os.path.join(
        cfg.MODELS_DIR, 'ZF', 'faster_rcnn_alt_opt', 'rpn_test.pt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'ZF_faster_rcnn_final.caffemodel'),
        True),
    'coco': (os.path.join(
        cfg.MODELS_DIR, '..', 'coco', 'VGG16', 'faster_rcnn_end2end', 'run_test.pt'),
        os.path.join(
            cfg.DATA_DIR,
            'faster_rcnn_models',
            'coco_vgg16_faster_rcnn_final.caffemodel'),
        False)}
