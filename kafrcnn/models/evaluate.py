import os
import cv2
import argparse
import numpy as np
import cPickle as pkl
from kafrcnn.utils import (load_bbox_labeler_gui_gts,
                           filter_dets, match_gt_parq_dets)


# Load ground truth frames and bboxes
def eval_models(args):
    gt_frames = load_bbox_labeler_gui_gts(args.bbox_labeler_gt_list_path)
    if args.verbose:
        print('- Loaded %d '
              'gt frames (%d bboxes) '
              'from %s' % (len(gt_frames),
                           sum(len(f.dets) for f in gt_frames),
                           args.bbox_labeler_gt_list_path))

    # Load detected frames and bboxes
    parq_detect_frames = []
    with open(args.dets_pkl_path, 'rb') as fh:
        dets_pkl = pkl.load(fh)
        # parq_detect_args = dets_pkl['parq_detect_args']
        parq_detect_frames = dets_pkl['parq_detect_frames']
        parq_detect_frames.sort(key=lambda x: x.img_name)

    if args.verbose:
        print('- Loaded %d frame detections '
              'from %s' % (len(parq_detect_frames),
                           args.dets_pkl_path))

    # Filter detected bboxes via various criteria
    num_filtered_bboxes = 0
    num_remaining_bboxes = 0
    for frame_idx in xrange(len(parq_detect_frames)):
        frame = parq_detect_frames[frame_idx]
        frame.car_dets = filter_dets(frame.dets,
                                     args.max_nms_thresh,
                                     args.min_conf_thresh,
                                     args.min_aspect_ratio_thresh,
                                     args.max_aspect_ratio_thresh)
        num_filtered_bboxes += (len(frame.dets) - len(frame.car_dets))
        num_remaining_bboxes += len(frame.car_dets)
    if args.verbose:
        print('- Filtered %d '
              'detections and kept %d detections '
              'within %d frames' % (num_filtered_bboxes,
                                    num_remaining_bboxes,
                                    len(parq_detect_frames)))

    # Accumulate statistics for each ground truth frame
    stats = []
    num_gt_frames = len(gt_frames)
    for gt_frame_idx, gt_frame in enumerate(gt_frames):
        if args.verbose:
            print 'Evaluating %3d/%3d: %s' % (gt_frame_idx + 1,
                                              num_gt_frames,
                                              gt_frame.img_name)

        # Find matching image in detection set
        matching_parq_frame_idx = None
        for parq_frame_idx, parq_frame in enumerate(parq_detect_frames):
            if gt_frame.img_name == parq_frame.img_name:
                matching_parq_frame_idx = parq_frame_idx
                break
        if matching_parq_frame_idx is None:
            raise IOError('Failed to find %s in '
                          'parq_detect_frames' % gt_frame.img_name)

        # Load image to determine width and height,
        #   then convert bboxes into relative coords and format:
        #   left, top, width, height
        if len(args.bbox_labeler_gt_img_dir) <= 0:
            img_path = gt_frame.img_path
        else:
            img_path = os.path.join(args.bbox_labeler_gt_img_dir,
                                    gt_frame.img_name)
        img = cv2.imread(img_path)
        if img is None:
            raise IOError('Failed to load %s' % img_path)

        img_height, img_width, _ = img.shape

        parq_frame_dets = []
        for d in parq_frame.car_dets:
            parq_frame_dets.append((float(d.left) / img_width,
                                    float(d.top) / img_height,
                                    float(d.right - d.left + 1) / img_width,
                                    float(d.bottom - d.top + 1) / img_height))
        gt_frame_dets = []
        for d in gt_frame.dets:
            gt_frame_dets.append((float(d.left) / img_width,
                                  float(d.top) / img_height,
                                  float(d.right - d.left + 1) / img_width,
                                  float(d.bottom - d.top + 1) / img_height))
        (matching_IOUs,
         matching_gt2parq_idx,
         matching_parq2gt_idx,
         FN_gt_idx,
         FP_parq_idx) = match_gt_parq_dets(gt_frame_dets,
                                           parq_frame_dets,
                                           args.min_iou_thresh)
        TP_count = len(matching_IOUs)
        FP_count = len(FP_parq_idx)
        FN_count = len(FN_gt_idx)

        # WARNING: these stats may contain a lot of
        # variance, due to frames with 1 (or ZERO) gt bbox
        precision = float('NaN')
        recall = float('NaN')
        F1_score = float('NaN')
        if TP_count + FP_count > 0:
            precision = float(TP_count) / (TP_count + FP_count)
        if TP_count + FN_count > 0:
            recall = float(TP_count) / (TP_count + FN_count)
        if precision + recall > 0:
            F1_score = 2 * precision * recall / (precision + recall)
        stats.append({'TP': TP_count,
                      'FP': FP_count,
                      'FN': FN_count,
                      'precision': precision,
                      'recall': recall,
                      'F1': F1_score,
                      'IOUs': matching_IOUs})

    # Calculate statistics
    all_IOUs = []
    for s in stats:
        all_IOUs += s['IOUs']
        all_TP_count = sum(s['TP'] for s in stats)
        all_FP_count = sum(s['FP'] for s in stats)
        all_FN_count = sum(s['FN'] for s in stats)
        all_precision = 0
        all_recall = 0
        all_F1 = 0
        if (all_TP_count + all_FP_count) > 0:
            all_precision = (float(all_TP_count) /
                             (all_TP_count + all_FP_count))
        if all_TP_count + all_FN_count > 0:
            all_recall = (float(all_TP_count) /
                          (all_TP_count + all_FN_count))
        if all_precision + all_recall > 0:
            all_F1 = (2 * all_precision * all_recall /
                      (all_precision + all_recall))
        avg_IOU = np.mean(all_IOUs)
    return all_precision, all_recall, all_F1, avg_IOU


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(
        description='Faster R-CNN IOU Model Accuracy Evaluation Script')

    parser.add_argument('--min_conf', dest='min_conf_thresh',
                        help='Min. FRCNN score threshold [0.15]',
                        default=0.15, type=float)

    parser.add_argument('--max_nms', dest='max_nms_thresh',
                        help='Max. Non-Max-Suppression threshold [0.375]',
                        default=0.375, type=float)

    parser.add_argument('--min_ar', dest='min_aspect_ratio_thresh',
                        help='Min. aspect ratio threshold [0]',
                        default=0, type=float)

    parser.add_argument('--max_ar', dest='max_aspect_ratio_thresh',
                        help='Max. aspect ratio threshold [inf]',
                        default=float('inf'), type=float)

    parser.add_argument('--min_iou', dest='min_iou_thresh',
                        help='Min. Intersection-over-Union threshold [0.5]',
                        default=0.5, type=float)

    parser.add_argument('--gt_img_dir', dest='bbox_labeler_gt_img_dir',
                        help=('Parent folder containing images inside '
                              '--gt_list_path, default=do not override '
                              'path in list []'),
                        default='', type=str)

    parser.add_argument('--verbose', dest='verbose',
                        help='Verbose print-out [1]',
                        default=1, type=int)

    parser.add_argument('dets_pkl_path',
                        help='Path of detection results pickle file',
                        type=str)
    parser.add_argument('--gt_list_path', dest='bbox_labeler_gt_list_path',
                        help='Path of bbox_labeler_gui bbox list file',
                        default='', type=str)

    args = parser.parse_args()
    if len(args.bbox_labeler_gt_list_path) <= 0:
        print ('Must specify --gt_list_path')
    return args
