labels = {
    "commodity_labels": ["背景", "橙汁", "面条", "牛奶", "薯片", "雪碧"],
}

cfg = {
    "datas_path": './dataset/commodity/',
    "tfrecord_file": "./dataset/commodity.tfrecord",
    "tflite_model_path": "./models/commodity.tflite",
    "model_path": "./models/commodity_model.h5",
    "labels_list": labels["commodity_labels"],
    "camera_id": 0,

    "width": 224,
    "height": 224,
    "color_channel": 3,

    "batch_size": 32,
    "epoch": 10,
    "lr": 0.001,
    "save_freq": 1,

    "steps": [8, 16, 32, 64],
    "match_thresh": 0.45,
    "variances": [0.1, 0.2],
    "clip": False,

    # network
    "base_channel": 16,
}
