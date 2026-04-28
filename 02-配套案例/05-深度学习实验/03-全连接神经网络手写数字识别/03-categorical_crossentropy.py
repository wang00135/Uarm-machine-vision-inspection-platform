import tensorflow as tf

x = tf.random.normal([2, 10])        # 构造网络输出
x = tf.nn.softmax(x)
print(x)
y_onehot = tf.constant([1, 3])      # 构造真实值
y_onehot = tf.one_hot(y_onehot, depth=10)
print(y_onehot)

loss = tf.losses.categorical_crossentropy(y_onehot, x)     # 计算交叉熵损失函数
print(loss)
loss = tf.reduce_mean(loss)         # 计算 batch 均方差
print(loss)