import math, sys
import numpy as np
from itertools import product as product
import cv2
from ai_lib.components.config import ai_cfg

# 先验框
def priors_box(image_sizes=None):
    """prior box"""
    if image_sizes is None:
        image_sizes = ai_cfg.BOX_INPUT_SIZE
    min_sizes = ai_cfg.MIN_SIZES
    steps = ai_cfg.STEPS
    clip = ai_cfg.CLIP

    if isinstance(image_sizes, int):
        image_sizes = (image_sizes, image_sizes)
    elif isinstance(image_sizes, tuple):
        image_sizes = image_sizes
    else:
        raise Exception('Type error of input image size format,tuple or int. ')

    for m in range(4):
        if (steps[m] != pow(2, (m + 3))):
            print("steps must be [8,16,32,64]")
            sys.exit()

    assert len(min_sizes) == len(steps), "anchors number didn't match the feature map layer."

    feature_maps = [
        [math.ceil(image_sizes[0] / step), math.ceil(image_sizes[1] / step)]
        for step in steps]

    anchors = []
    num_box_fm_cell=[]
    for k, f in enumerate(feature_maps):
        num_box_fm_cell.append(len(min_sizes[k]))
        for i, j in product(range(f[0]), range(f[1])):
            for min_size in min_sizes[k]:
                if isinstance(min_size, int):
                    min_size = (min_size, min_size)
                elif isinstance(min_size, tuple):
                    min_size = min_size
                else:
                    raise Exception('Type error of min_sizes elements format,tuple or int. ')
                s_kx = min_size[1] / image_sizes[1]
                s_ky = min_size[0] / image_sizes[0]
                cx = (j + 0.5) * steps[k] / image_sizes[1]
                cy = (i + 0.5) * steps[k] / image_sizes[0]
                anchors += [cx, cy, s_kx, s_ky]

    output = np.asarray(anchors).reshape([-1, 4])
    # print("prios:",output.shape,len(output))
    # print("num box for fm cell:",num_box_fm_cell)
    if clip:
        output = np.clip(output, 0, 1)
    return output, num_box_fm_cell

def softmax(x):
    x -= np.max(x, axis=1, keepdims=True)  # 为了稳定地计算softmax概率， 一般会减掉最大的那个元素
    # print("减去行最大值 ：\n", x)
    x = np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)
    return x

def decode_bbox(pre, priors, variances=None):
    if variances is None:
        variances = [0.1, 0.2]
    centers = priors[:, :2] + pre[:, :2] * variances[0] * priors[:, 2:]

    sides = priors[:, 2:] * np.exp(pre[:, 2:] * variances[1])
    return np.concatenate([centers - sides / 2, centers + sides / 2], axis=1)

def show_image(img, boxes, classes, scores, img_height, img_width, prior_index, class_list):
    """
    draw bboxes and labels
    out:boxes,classes,scores
    """
    # bbox
    x1, y1, x2, y2 = int(boxes[prior_index][0] * img_width), int(boxes[prior_index][1] * img_height), \
                     int(boxes[prior_index][2] * img_width), int(boxes[prior_index][3] * img_height)
    if classes[prior_index] == 1:
        color = (0, 255, 0)
    else:
        color = (0, 0, 255)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    # confidence

    score = "{:.4f}".format(scores[prior_index])
    class_name = class_list[classes[prior_index]]

    cv2.putText(img, '{} {}'.format(class_name, score),
                (int(boxes[prior_index][0] * img_width), int(boxes[prior_index][1] * img_height) - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))


def nms(box, scor, thresh):
    # 首先数据赋值和计算对应矩形框的面积
    # dets的数据格式是dets[[xmin,ymin,xmax,ymax,scores]....]
    x1 = box[:, 0]
    y1 = box[:, 1]
    x2 = box[:, 2]
    y2 = box[:, 3]
    areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    scores = scor
    # print('areas  ', areas)
    # print('scores ', scores)

    # 这边的keep用于存放，NMS后剩余的方框
    keep = []

    # 取出分数从大到小排列的索引。.argsort()是从小到大排列，[::-1]是列表头和尾颠倒一下。
    index = scores.argsort()[::-1]
    # print(index)
    # 上面这两句比如分数[0.72 0.8  0.92 0.72 0.81 0.9 ]
    #  对应的索引index[  2   5    4     1    3   0  ]记住是取出索引，scores列表没变。

    # index会剔除遍历过的方框，和合并过的方框。
    while index.size > 0:
        # print(index.size)
        # 取出第一个方框进行和其他方框比对，看有没有可以合并的
        i = index[0]  # every time the first is the biggst, and add it directly

        # 因为我们这边分数已经按从大到小排列了。
        # 所以如果有合并存在，也是保留分数最高的这个，也就是我们现在那个这个
        # keep保留的是索引值，不是具体的分数。
        keep.append(i)
        # print(keep)
        # print('x1', x1[i])
        # print(x1[index[1:]])

        # 计算交集的左上角和右下角
        # 这里要注意，比如x1[i]这个方框的左上角x和所有其他的方框的左上角x的
        x11 = np.maximum(x1[i], x1[index[1:]])  # calculate the points of overlap
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])

        # print(x11, y11, x22, y22)
        # 这边要注意，如果两个方框相交，X22-X11和Y22-Y11是正的。
        # 如果两个方框不相交，X22-X11和Y22-Y11是负的，我们把不相交的W和H设为0.
        w = np.maximum(0, x22 - x11 + 1)
        h = np.maximum(0, y22 - y11 + 1)

        # 计算重叠面积就是上面说的交集面积。不相交因为W和H都是0，所以不相交面积为0
        overlaps = w * h
        # print('overlaps is', overlaps)

        # 这个就是IOU公式（交并比）。
        # 得出来的ious是一个列表，里面拥有当前方框和其他所有方框的IOU结果。
        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)
        # print('ious is', ious)

        # 接下来是合并重叠度最大的方框，也就是合并ious中值大于thresh的方框
        # 我们合并的操作就是把他们剔除，因为我们合并这些方框只保留下分数最高的。
        # 我们经过排序当前我们操作的方框就是分数最高的，所以我们剔除其他和当前重叠度最高的方框
        # 这里np.where(ious<=thresh)[0]是一个固定写法。
        idx = np.where(ious <= thresh)[0]
        # print(idx)

        # 把留下来框在进行NMS操作
        # 这边留下的框是去除当前操作的框，和当前操作的框重叠度大于thresh的框
        # 每一次都会先去除当前操作框，所以索引的列表就会向前移动移位，要还原就+1，向后移动一位
        index = index[idx + 1]  # because index start from 1
        # print(index)
    return keep

def parse_predict(predictions, priors, labels_list):
    label_classes = labels_list
    # print('predictions[0]', predictions[0].shape)
    bbox_regressions, confs = np.split(predictions[0], [4, ], axis=1)
    boxes = decode_bbox(bbox_regressions, priors, ai_cfg.VARIANCES)

    confs = softmax(confs)

    out_boxes = []
    out_labels = []
    out_scores = []

    for c in range(1, len(label_classes)):
        cls = confs[:, c]
        score_idx = cls > ai_cfg.SCORE_THRESHOLD
        cls_boxes = boxes[score_idx]
        cls_scores = cls[score_idx]

        # print('cls_boxes', cls_boxes)

        nms_idx = nms(cls_boxes, cls_scores, ai_cfg.NMS_THRESHOLD)
        # print("nms_idx", type(nms_idx), nms_idx)

        cls_boxes = cls_boxes[nms_idx]
        cls_scores = cls_scores[nms_idx]

        # print("cls_boxes", cls_boxes.shape)
        # print("cls_scores", cls_scores.shape)

        cls_labels = [c] * cls_boxes.shape[0]

        out_boxes.append(cls_boxes)
        out_labels.extend(cls_labels)
        out_scores.append(cls_scores)

    boxes = np.concatenate(out_boxes, axis=0)
    scores = np.concatenate(out_scores, axis=0)
    classes = np.array(out_labels)
    return boxes, classes, scores


if __name__ == '__main__':
    print(priors_box())