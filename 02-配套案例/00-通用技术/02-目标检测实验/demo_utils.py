#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.

import os
import numpy as np
import cv2

__all__ = ["mkdir", "nms", "multiclass_nms", "demo_postprocess"]

# COCO_CLASSES = (
#     "person",
#     "bicycle",
#     "car",
#     "motorcycle",
#     "airplane",
#     "bus",
#     "train",
#     "truck",
#     "boat",
#     "traffic light",
#     "fire hydrant",
#     "stop sign",
#     "parking meter",
#     "bench",
#     "bird",
#     "cat",
#     "dog",
#     "horse",
#     "sheep",
#     "cow",
#     "elephant",
#     "bear",
#     "zebra",
#     "giraffe",
#     "backpack",
#     "umbrella",
#     "handbag",
#     "tie",
#     "suitcase",
#     "frisbee",
#     "skis",
#     "snowboard",
#     "sports ball",
#     "kite",
#     "baseball bat",
#     "baseball glove",
#     "skateboard",
#     "surfboard",
#     "tennis racket",
#     "bottle",
#     "wine glass",
#     "cup",
#     "fork",
#     "knife",
#     "spoon",
#     "bowl",
#     "banana",
#     "apple",
#     "sandwich",
#     "orange",
#     "broccoli",
#     "carrot",
#     "hot dog",
#     "pizza",
#     "donut",
#     "cake",
#     "chair",
#     "couch",
#     "potted plant",
#     "bed",
#     "dining table",
#     "toilet",
#     "tv",
#     "laptop",
#     "mouse",
#     "remote",
#     "keyboard",
#     "cell phone",
#     "microwave",
#     "oven",
#     "toaster",
#     "sink",
#     "refrigerator",
#     "book",
#     "clock",
#     "vase",
#     "scissors",
#     "teddy bear",
#     "hair drier",
#     "toothbrush",
# )

VOC_CLASSES = (
    "人",
    "自行车",
    "小汽车",
    "摩托车",
    "飞机",
    "公交汽车",
    "火车",
    "卡车",
    "船",
    "交通灯",
    "消防栓",
    "停车标志",
    "停车记时器",
    "长凳",
    "鸟",
    "猫",
    "狗",
    "马",
    "绵羊",
    "牛",
    "大象",
    "熊",
    "斑马",
    "长颈鹿",
    "双肩背包",
    "雨伞",
    "手提包",
    "领带",
    "手提箱",
    "飞碟",
    "滑雪板",
    "滑雪板",
    "运动球",
    "风筝",
    "棒球棒",
    "棒球手套e",
    "溜冰板",
    "冲浪板",
    "网球拍",
    "瓶子",
    "酒杯",
    "杯子",
    "餐叉",
    "刀",
    "勺子",
    "碗",
    "香蕉",
    "苹果",
    "三明治",
    "橘子",
    "西兰花",
    "胡萝卜",
    "热狗",
    "披萨",
    "甜甜圈",
    "蛋糕",
    "椅子",
    "长沙发",
    "盆栽",
    "床",
    "餐桌",
    "厕所",
    "电视",
    "笔记本电脑",
    "鼠标",
    "遥控器",
    "键盘",
    "手机",
    "微波炉",
    "烤箱",
    "烤面包机",
    "洗手池",
    "冰箱",
    "书",
    "钟表",
    "花瓶",
    "剪刀",
    "泰迪熊",
    "吹风机",
    "牙刷",
)

# VOC_CLASSES = (
# 	"LuDeng",
# 	"CheKu",
# 	"DaoZha",
# 	'gong_jiao',
# 	"jiao_tong_deng",
# 	"jtbzw",
# 	"JiaoTongDeng",
# 	"BaoJingTai",
# 	"LED",
# 	"ETC",
# 	"TFT",
# 	"LTXS",
# 	"YYBB",
# 	"WXCD",
# 	"JT"
# )

#
# def preprocess(image, input_size, mean, std, swap=(2, 0, 1)):
#     if len(image.shape) == 3:
#         padded_img = np.ones((input_size[0], input_size[1], 3)) * 114.0
#     else:
#         padded_img = np.ones(input_size) * 114.0
#     img = np.array(image)
#     r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])
#     resized_img = cv2.resize(
#         img, (int(img.shape[1] * r), int(img.shape[0] * r)), interpolation=cv2.INTER_LINEAR
#     ).astype(np.float32)
#     padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img
#     image = padded_img
#
#     image = image.astype(np.float32)
#     image = image[:, :, ::-1]
#     image /= 255.0
#     # if mean is not None:
#     #     image -= mean
#     # if std is not None:
#     #     image /= std
#     image = image.transpose(swap)
#     image = np.ascontiguousarray(image, dtype=np.float32)
#     return image, r
#


def preproc(img, input_size, swap=(2, 0, 1)):
    if len(img.shape) == 3:
        padded_img = np.ones((input_size[0], input_size[1], 3), dtype=np.uint8) * 114
    else:
        padded_img = np.ones(input_size, dtype=np.uint8) * 114

    r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])
    resized_img = cv2.resize(
        img,
        (int(img.shape[1] * r), int(img.shape[0] * r)),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.uint8)
    padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img

    padded_img = padded_img.transpose(swap)
    padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
    return padded_img, r


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def nms(boxes, scores, nms_thr):
    """Single class NMS implemented in Numpy."""
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= nms_thr)[0]
        order = order[inds + 1]

    return keep


def multiclass_nms(boxes, scores, nms_thr, score_thr):
    """Multiclass NMS implemented in Numpy"""
    final_dets = []
    num_classes = scores.shape[1]
    for cls_ind in range(num_classes):
        cls_scores = scores[:, cls_ind]
        valid_score_mask = cls_scores > score_thr
        if valid_score_mask.sum() == 0:
            continue
        else:
            valid_scores = cls_scores[valid_score_mask]
            valid_boxes = boxes[valid_score_mask]
            keep = nms(valid_boxes, valid_scores, nms_thr)
            if len(keep) > 0:
                cls_inds = np.ones((len(keep), 1)) * cls_ind
                dets = np.concatenate([valid_boxes[keep], valid_scores[keep, None], cls_inds], 1)
                final_dets.append(dets)
    if len(final_dets) == 0:
        return None
    return np.concatenate(final_dets, 0)


def demo_postprocess(outputs, img_size, p6=False):

    grids = []
    expanded_strides = []

    if not p6:
        strides = [8, 16, 32]
    else:
        strides = [8, 16, 32, 64]

    hsizes = [img_size[0]//stride for stride in strides]
    wsizes = [img_size[1]//stride for stride in strides]

    for hsize, wsize, stride in zip(hsizes, wsizes, strides):
        xv, yv = np.meshgrid(np.arange(hsize), np.arange(wsize))
        grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
        grids.append(grid)
        shape = grid.shape[:2]
        expanded_strides.append(np.full((*shape, 1), stride))

    grids = np.concatenate(grids, 1)
    expanded_strides = np.concatenate(expanded_strides, 1)
    outputs[..., :2] = (outputs[..., :2] + grids) * expanded_strides
    outputs[..., 2:4] = np.exp(outputs[..., 2:4]) * expanded_strides

    return outputs
