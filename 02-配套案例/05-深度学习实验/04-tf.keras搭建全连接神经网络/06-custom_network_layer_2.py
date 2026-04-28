import tensorflow as tf
# 导入 Sequential 容器，优化器，损失函数模块
from tensorflow.keras import layers, Sequential

class MyDense(layers.Layer):
    # 自定义网络层
    def __init__(self, inp_dim, outp_dim):
        super(MyDense, self).__init__()
        # 创建权值张量并添加到类管理列表中，设置为需要优化
        self.kernel = self.add_variable('w', [inp_dim, outp_dim],
                                        trainable=True)

    def call(self, inputs, training=None):
        # X@W
        out = inputs @ self.kernel
        # 执行激活函数运算
        out = tf.nn.relu(out)
        return out


model = Sequential([MyDense(784, 256),       # 使用自定义的层
                     MyDense(256, 128),
                     MyDense(128, 64),
                     MyDense(64, 32),
                     MyDense(32, 10)])

model.build(input_shape=(None, 28*28))
model.summary()

