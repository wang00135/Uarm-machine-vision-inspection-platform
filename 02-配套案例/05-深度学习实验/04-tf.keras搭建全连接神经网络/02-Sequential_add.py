import tensorflow as tf
from tensorflow.keras import layers, Sequential

model = Sequential([])                # 创建一个空的网络容器
layers_num = 2                        # 堆叠 2 次
for _ in range(layers_num):
    model.add(layers.Dense(3))        # 添加全连接层
    model.add(layers.ReLU())          # 添加激活函数层

model.build(input_shape=(4, 4))       # 创建网络参数
model.summary()                       # 打印出网络结构和参数量

x = tf.random.normal([4, 4])
out = model(x)                        # 输入从第一层开始，逐层传播至输出层，并返回输出层的输出
print(out)

for p in model.trainable_variables:
    print(p.name, p.shape)            # 参数名和形状
