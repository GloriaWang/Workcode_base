import os
import sys
import json
import boto3
import caffe
import numpy as np
from bunch import bunchify
import numpy.matlib as npm
from lxml import etree as ET
from fast_rcnn.config import cfg
from kafrcnn.config import RPNS, NETS
from kafrcnn.structs import ObjectDetection, FrameDetections


# ToDo: heavy refactoring
def loadDetsXML(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    dets = []
    for o in root.findall('object'):
        class_id = o.find('name').text
        b = o.find('bndbox')
        left = int(b.find('xmin').text) - 1
        top = int(b.find('ymin').text) - 1
        right = int(b.find('xmax').text) - 1
        bottom = int(b.find('ymax').text) - 1
        dets.append((left, top, right, bottom, class_id))
    return dets


def connectToS3(credentials_file="scripts/credentials.json"):
    with open(credentials_file) as json_data_file:
        data = json.load(json_data_file)
    s3_client = boto3.client('s3',
                             aws_access_key_id=data['s3']['access_key_id'],
                             aws_secret_access_key=data['s3']['secret_access_key'])
    return s3_client, data


def get_args(config_file, section):
    """
     Reads arguments from a section of the config file
    """
    with open(config_file) as cfg_file:
        data = json.load(cfg_file)
        args = bunchify(data[section])
    return args


def get_test_data(data_test):
    """
    Change xml file to txt and use this format to test
    """
    # ToDo: hardcoded dependencies. Do we HAVE to save the file?
    DATA_PATH = "/opt/py-faster-rcnn/data/"
    ANNOT_PATH = DATA_PATH + "CUSTOM8888/Annotations/"
    IMGSET_PATH = DATA_PATH + "CUSTOM8888/ImageSets/Main/"
    testdata = open(data_test, "r")
    example = testdata.read().splitlines()

    # Give the whole path of xml file for each image
    for k in range(len(example)):
        example[k] = os.path.join(ANNOT_PATH, example[k] + ".xml")
    test = []

    # Convert xml file to txt and write on testnew.txt
    for i in range(len(example)):
        if os.path.isfile(example[i]):
            test.append(loadDetsXML(example[i]))
        else:
            print "Groud truth file not exist"
    gt_file_list = os.path.basename(data_test)
    f = open(os.path.join('data', gt_file_list[:-4] + "new.txt"), "w")
    for i in range(len(test)):
        f.write(IMGSET_PATH + example[i][33:-4] + ".jpg" + "\n")
        for j in range(0, len(test[i])):
            f.write(" ")
            for k in range(0, 4):
                f.write(str(test[i][j][k]) + ", ")
            f.write(str(test[i][j][4] + "\n"))
    gt_boxes_filename = f.name
    f.close
    return gt_boxes_filename, test


def resolve_file_path(path):
    if len(path) > 0:
        if path[0] == '.' or path[0] == '/' or path[0] == '~':
            path = os.path.abspath(path)
        else:
            path = os.path.join(os.getcwd(), path)
        if os.path.isfile(path):
            return path
    return None


def setup_frcnn_test_net(args, rpn_only=False):
    cfg.TEST.HAS_RPN = args.use_rpn  # Use RPN for proposals
    if rpn_only:
        prototxt, caffemodel, is_voc = RPNS[args.test_net]
    else:
        prototxt, caffemodel, is_voc = NETS[args.test_net]
    try:
        if len(args.test_model) > 0:
            caffemodel = str(args.test_model)
    except BaseException, err:
        print err

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))
    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id

    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    print '\nLoaded network %s, using CPU? %d' % (caffemodel, args.cpu_mode)

    return (net, prototxt, caffemodel, is_voc)


def apply_nms(dets, nms_thresh):
    from nms.py_cpu_nms import py_cpu_nms

    # Group detections into matrix form:
    #  [[top, left, bottom, right, score], ...]
    per_class_dets = dict()
    for det_i, det in enumerate(dets):
        if det.cls not in per_class_dets:
            per_class_dets[det.cls] = [[det.top, det.left,
                                        det.bottom, det.right,
                                        det.score, det_i]]
        else:
            per_class_dets[det.cls].append([det.top, det.left,
                                            det.bottom, det.right,
                                            det.score, det_i])

    # Apply NMS
    class_removals = dict()
    idx_det_keep = []
    for k in per_class_dets.keys():
        per_class_dets[k] = np.array(per_class_dets[k])
        idx_nms_keep = py_cpu_nms(per_class_dets[k], nms_thresh)
        if len(idx_nms_keep) < len(per_class_dets[k]):
            class_removals[k] = len(per_class_dets[k]) - len(idx_nms_keep)
        idx_det_keep += list(per_class_dets[k][idx_nms_keep, -1])

    filtered_dets = []
    for idx in idx_det_keep:
        filtered_dets.append(dets[int(idx)])

    return (filtered_dets, class_removals)


def filter_dets(dets, max_nms_thresh=1.0, min_score_thresh=0.0,
                min_aspect_ratio_thresh=0,
                max_aspect_ratio_thresh=float('inf'),
                target_class_names=['car', 'truck', 'bus']):
    nms_dets, _ = apply_nms(dets, max_nms_thresh)
    filtered_dets = []
    filter_result = []
    for det in nms_dets:
        detect_filter = []
        if det.cls not in target_class_names:
            continue
        if det.score < min_score_thresh:
            continue
        width = det.right - det.left
        height = det.bottom - det.top
        ar = float(width) / height
        if (ar > max_aspect_ratio_thresh) or (ar < min_aspect_ratio_thresh):
            continue
        filtered_dets.append(det)
        detect_filter.append(det.left)
        detect_filter.append(det.top)
        detect_filter.append(det.right)
        detect_filter.append(det.bottom)
        detect_filter.append(det.cls)
        detect_filter.append(det.score)
        filter_result.append(detect_filter)
    return filtered_dets, filter_result


# expect in normalized coordinates: left, top, width, height
def IOU_vec(bbox1, bbox2):
    tlx1, tly1, w1, h1 = bbox1[:, 0], bbox1[:, 1], bbox1[:, 2], bbox1[:, 3]
    tlx2, tly2, w2, h2 = bbox2[:, 0], bbox2[:, 1], bbox2[:, 2], bbox2[:, 3]

    x1 = np.concatenate([[tlx1], [tlx2]], axis=0).transpose()
    y1 = np.concatenate([[tly1], [tly2]], axis=0).transpose()

    x2 = np.concatenate([[tlx1 + w1], [tlx2 + w2]], axis=0).transpose()
    y2 = np.concatenate([[tly1 + h1], [tly2 + h2]], axis=0).transpose()

    x5 = np.max(x1, 1)
    y5 = np.max(y1, 1)

    x6 = np.min(x2, 1)
    y6 = np.min(y2, 1)

    valid_x = np.array(x5 <= x6, dtype='int8')
    valid_y = np.array(y5 <= y6, dtype='int8')
    intersections = valid_x * valid_y * (x6 - x5) * (y6 - y5)

    sum_areas = (w1 * h1) + (w2 * h2)
    unions = sum_areas - intersections

    return intersections / unions


# Expect in normalized coordinates: left, top, width, height
def IOU_mat(bbox1, bbox2):
    num_pts_1 = bbox1.shape[0]
    num_pts_2 = bbox2.shape[0]

    left_1, top_1, width_1, height_1 = (bbox1[:, 0], bbox1[:, 1],
                                        bbox1[:, 2], bbox1[:, 3])
    left_2, top_2, width_2, height_2 = (bbox2[:, 0], bbox2[:, 1],
                                        bbox2[:, 2], bbox2[:, 3])

    left_1_mat = npm.repmat(left_1.reshape((num_pts_1, 1)), 1,
                            num_pts_2).reshape((num_pts_1, num_pts_2, 1))

    left_2_mat = npm.repmat(left_2,
                            num_pts_1, 1).reshape((num_pts_1, num_pts_2, 1))

    top_1_mat = npm.repmat(top_1.reshape((num_pts_1, 1)), 1,
                           num_pts_2).reshape((num_pts_1, num_pts_2, 1))

    top_2_mat = npm.repmat(top_2,
                           num_pts_1, 1).reshape((num_pts_1, num_pts_2, 1))

    right_1_mat = npm.repmat((left_1 + width_1).reshape((num_pts_1, 1)), 1,
                             num_pts_2).reshape((num_pts_1, num_pts_2, 1))

    right_2_mat = npm.repmat((left_2 + width_2),
                             num_pts_1, 1).reshape((num_pts_1, num_pts_2, 1))

    bottom_1_mat = npm.repmat((top_1 + height_1).reshape((num_pts_1, 1)), 1,
                              num_pts_2).reshape((num_pts_1, num_pts_2, 1))

    bottom_2_mat = npm.repmat((top_2 + height_2), num_pts_1,
                              1).reshape((num_pts_1, num_pts_2, 1))

    left_12_mat = np.concatenate([left_1_mat, left_2_mat], axis=2)
    left_max_mat = np.max(left_12_mat, 2)

    top_12_mat = np.concatenate([top_1_mat, top_2_mat], axis=2)
    top_max_mat = np.max(top_12_mat, 2)

    right_12_mat = np.concatenate([right_1_mat, right_2_mat], axis=2)
    right_min_mat = np.min(right_12_mat, 2)

    bottom_12_mat = np.concatenate([bottom_1_mat, bottom_2_mat], axis=2)
    bottom_min_mat = np.min(bottom_12_mat, 2)

    valid_x_mat = np.array(left_max_mat <= right_min_mat, dtype='int8')
    valid_y_mat = np.array(top_max_mat <= bottom_min_mat, dtype='int8')

    intersections_mat = valid_x_mat * valid_y_mat * (
        right_min_mat - left_max_mat) * (bottom_min_mat - top_max_mat)

    width_1_mat = npm.repmat(width_1.reshape((num_pts_1, 1)), 1, num_pts_2)
    height_1_mat = npm.repmat(height_1.reshape((num_pts_1, 1)), 1, num_pts_2)

    width_2_mat = npm.repmat(width_2, num_pts_1, 1)
    height_2_mat = npm.repmat(height_2, num_pts_1, 1)

    sum_areas_mat = (width_1_mat * height_1_mat) + (width_2_mat * height_2_mat)
    unions_mat = sum_areas_mat - intersections_mat

    return intersections_mat / unions_mat


def match_gt_dets(gt_frame_dets, frame_dets, min_iou_thresh):
    # 0. Initialize outputs and check for valid inputs
    matching_IOUs = []
    matching_gt2_idx = dict()
    matching_2gt_idx = dict()
    FP_idx = []
    FN_gt_idx = []
    if len(gt_frame_dets) == 0:
        FP_idx = range(len(frame_dets))
        return (matching_IOUs, matching_gt2_idx,
                matching_2gt_idx, FN_gt_idx, FP_idx)
    elif len(frame_dets) == 0:
        FN_gt_idx = range(len(gt_frame_dets))
        return (matching_IOUs, matching_gt2_idx,
                matching_2gt_idx, FN_gt_idx, FP_idx)

    # 1. Compute and threshold pairwise IOU matrix
    #    (row_i == gt_i, col_j == _j)
    all_IOUs = IOU_mat(np.array(gt_frame_dets), np.array(frame_dets))
    IOUs = all_IOUs * (all_IOUs >= min_iou_thresh)

    # 2. Initialize loop-invariant state
    num_gts, num_ = IOUs.shape
    matching_gt2_idx = dict()
    matching_2gt_idx = dict()
    rem_gt_idx = set(range(num_gts))
    rem_idx = set(range(num_))

    while len(rem_gt_idx) > 0:
        """
        Proof that loop terminates: either
          (3) will remove at least one FN, or
          (5) will remove at least one (non-contended) TP
        """
        # 3. Remove false negatives: gt entries without
        #    any IOU-matched entries
        upd_rem_gt_idx = []
        for gt_idx in rem_gt_idx:
            if np.max(IOUs[gt_idx, :]) == 0:
                FN_gt_idx.append(gt_idx)
            else:
                upd_rem_gt_idx.append(gt_idx)
        rem_gt_idx = set(upd_rem_gt_idx)

        if (len(rem_gt_idx) <= 0):
            break

        # 4. For each gt, tentatively match with based on max IOU;
        #    if this tentative had already been matched then break
        #    tie by largest IOU

        # Indexed by _idx; contains tuple (gt_idx, IOU)
        matching_gt_per_idx = dict()
        for gt_idx in rem_gt_idx:
            tent_idx = np.argmax(IOUs[gt_idx, :])
            tent_IOU = IOUs[gt_idx, tent_idx]
            if tent_idx not in matching_gt_per_idx:
                # No contention
                matching_gt_per_idx[tent_idx] = (gt_idx, tent_IOU)
            elif matching_gt_per_idx[tent_idx][1] < tent_IOU:
                # Ccontention but new match better
                matching_gt_per_idx[tent_idx] = (gt_idx, tent_IOU)
            # else contention but old match better

        # 5. Remove true positives: non-contended gt-matchings
        for _idx, gt_idx_iou_pair in matching_gt_per_idx.iteritems():
            gt_idx = gt_idx_iou_pair[0]
            matching_gt2_idx[gt_idx] = _idx
            matching_2gt_idx[_idx] = gt_idx
            IOUs[gt_idx, :] = 0
            IOUs[:, _idx] = 0
        unique_idxs = set(idx for idx, _ in matching_gt_per_idx.values())
        rem_gt_idx = rem_gt_idx - unique_idxs
        rem_idx = rem_idx - set(matching_gt_per_idx.keys())
        matching_IOUs += [iou for _, iou in matching_gt_per_idx.values()]

    FP_idx = list(rem_idx)

    return (matching_IOUs, matching_gt2_idx,
            matching_2gt_idx, FN_gt_idx, FP_idx)


# ToDo: Jesuschrist, this could be so much simpler
def load_bbox_labeler_gui_gts(bbox_list_path):
    gt_frames = []
    with open(bbox_list_path, 'r') as f:
        for line_idx, line in enumerate(f.readlines()):
            if len(line) <= 0:
                continue
            if line[0] == ' ':
                if len(gt_frames) <= 0:
                    err_str = 'BBox entries before first image path on line'
                    print(err_str + '%d' % (line_idx + 1))
                line = line.replace(',', '')
                left, top, right, bottom, cls = line.split()
                gt_frames[-1].dets.append(ObjectDetection(cls,
                                                          float(left),
                                                          float(top),
                                                          float(right),
                                                          float(bottom),
                                                          1.0))
            else:
                gt_frames.append(FrameDetections(line.strip(), []))
    return gt_frames


def load_image_paths(args):
    """
    Loads the images
    ToDo: this method could be refactored
    """
    image_paths = []
    # images_path is for example CUSTOM8888/JPEGImages
    if len(args.images_path) > 0 and os.path.isdir(args.images_path):
        with open(args.image_list) as f:
            flist = f.read().splitlines()

        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

        for file_path in os.listdir(args.images_path):
            file_base, file_ext = os.path.splitext(file_path)

            if len(file_base) > 7 and file_base[:7] == '_frcnn_':
                continue
            file_ext = file_ext.lower()

            if (file_base not in flist):
                continue

            if file_ext in valid_extensions:
                image_paths.append(os.path.join(args.images_path, file_path))
    else:
        image_path = resolve_file_path(args.images_path)

        if image_path is None:
            print 'Image path not found: %s' % args.images_path
            sys.exit(-1)

        image_paths.append(image_path)

    # IDK WTF is this for, maybe in case you have millions of images
    # in the image list and you only want to process some of them??
    if args.max_images > 0 and args.max_images < len(image_paths):
        filtered_image_paths = []
        for idx in np.linspace(0, len(image_paths) - 1, args.max_images):
            filtered_image_paths.append(image_paths[int(round(idx))])
        image_paths = filtered_image_paths

    return image_paths
