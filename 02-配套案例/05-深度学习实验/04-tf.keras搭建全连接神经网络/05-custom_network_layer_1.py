import tensorflow as tf
from tensorflow.keras import layers

class MyDense(layers.Layer):
    # 自定义网络层
    def __init__(self, inp_dim, outp_dim):
        super(MyDense, self).__init__()
        # 创建权值张量并添加到类管理列表中，设置为需要优化
        self.kernel = self.add_variable('w', [inp_dim, outp_dim],
                                        trainable=True)

        # # 通过 tf.Variable 创建的类成员也会自动加入类参数列表
        # self.kernel2 = tf.Variable(tf.random.normal([inp_dim, outp_dim]),
        #                            trainable=False)

    def call(self, inputs, training=None):
        # X@W
        out = inputs @ self.kernel
        # 执行激活函数运算
        out = tf.nn.relu(out)
        return out

# 实现自定义类的前向计算逻辑
net = MyDense(4, 3)                              # 创建输入为4，输出为3节点的自定义层
print('全部参数列表', net.variables)              # 查看类的全部参数列表
print('待优化参数列表', net.trainable_variables)  # 查看类的待优化参数列表
