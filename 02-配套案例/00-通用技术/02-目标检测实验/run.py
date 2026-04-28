#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.
import argparse
import os
import cv2
import numpy as np
import onnxruntime
import time
from demo_utils import preproc,multiclass_nms,\
    VOC_CLASSES,demo_postprocess
from visualize import vis


def make_parser():
    parser = argparse.ArgumentParser("onnxruntime inference sample")
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="./models/yolox_nano.onnx",
        # default="yolox_hand_nano.onnx",
        help="Input your onnx model.",
    )
    parser.add_argument(
        "-i",
        "--image_path",
        type=str,
        default='dog.jpg',
        help="Path to your input image.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default='demo_output',
        help="Path to your output directory.",
    )
    parser.add_argument(
        "-s",
        "--score_thr",
        type=float,
        default=0.5,
        help="Score threshould to filter the result.",
    )
    parser.add_argument(
        "--input_shape",
        type=str,
        default="416, 416",
        help="Specify an input shape for inference.",
    )
    parser.add_argument(
        "--with_p6",
        action="store_true",
        help="Whether your model uses p6 in FPN/PAN.",
    )
    return parser


if __name__ == '__main__':
    args = make_parser().parse_args()

    input_shape = tuple(map(int, args.input_shape.split(',')))
    origin_img = cv2.imread(args.image_path)

    cap = cv2.VideoCapture(0)
    session = onnxruntime.InferenceSession(args.model)

    while True:
        ret, origin_img = cap.read()

        img, ratio = preproc(origin_img, input_shape)

        ort_inputs = {session.get_inputs()[0].name: img[None, :, :, :]}

        s = time.time()
        output = session.run(None, ort_inputs)
        print('onnx Infer:{} ms.'.format((time.time() - s) * 1000))

        predictions = demo_postprocess(output[0], input_shape, p6=args.with_p6)[0]

        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2]/2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3]/2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2]/2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3]/2.
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)
        if dets is not None:
            final_boxes, final_scores, final_cls_inds = dets[:, :4], dets[:, 4], dets[:, 5]
            origin_img = vis(origin_img, final_boxes, final_scores, final_cls_inds,
                             conf=args.score_thr, class_names=VOC_CLASSES)
        cv2.imshow("yolox_nano", origin_img)
        cv2.waitKey(5)

        # mkdir(args.output_dir)
        # output_path = os.path.join(args.output_dir, args.image_path.split("/")[-1])
        # cv2.imwrite(output_path, origin_img)
