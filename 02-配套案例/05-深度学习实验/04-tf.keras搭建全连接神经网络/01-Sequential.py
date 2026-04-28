import tensorflow as tf
from tensorflow.keras import layers, Sequential

model = Sequential([                                # 封装为一个网络
            layers.Dense(3, activation=None),       # 全连接层，此处不使用激活函数
            layers.ReLU(),                          # 激活函数层
            layers.Dense(2, activation=None),       # 全连接层，此处不使用激活函数
            layers.ReLU()                           # 激活函数层
            ])
x = tf.random.normal([4, 3])
print(x)
out = model(x)   # 输入从第一层开始，逐层传播至输出层，并返回输出层的输出
print(out)


