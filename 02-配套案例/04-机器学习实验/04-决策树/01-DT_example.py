#!/usr/bin/env python3


import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
# 导入鸢尾花数据集
iris = datasets.load_iris()

iris_feature = iris.data #特征数据
iris_target = iris.target #分类数据


"""
    feature_train, feature_test, target_train, target_test 分别代表训练集特征、测试集特征、训练集目标值、验证集特征。
    test_size 参数代表划分到测试集数据占全部数据的百分比，你也可以用 train_size 来指定训练集所占全部数据的百分比。
    一般情况下，我们会将整个训练集划分为 70% 训练集和 30% 测试集。最后的 random_state 参数表示乱序程度。

"""
feature_train, feature_test, target_train, target_test = train_test_split(iris_feature, iris_target, test_size=0.33, random_state=42)


# 训练决策树模型
from sklearn.tree import DecisionTreeClassifier,export_graphviz
"""
DecisionTreeClassifier() 模型方法中也包含非常多的参数值。例如：

criterion = gini/entropy 可以用来选择用基尼指数或者熵来做损失函数。
splitter = best/random 用来确定每个节点的分裂策略。支持“最佳”或者“随机”。
max_depth = int 用来控制决策树的最大深度，防止模型出现过拟合。
min_samples_leaf = int 用来设置叶节点上的最少样本数量，用于对树进行修剪。
"""
dt_model = DecisionTreeClassifier() # 所以参数均置为默认状态
dt_model.fit(feature_train,target_train) # 使用训练集训练模型
predict_results = dt_model.predict(feature_test) # 使用模型对测试集进行预测


# 模型的评价
from sklearn.metrics import accuracy_score
print(accuracy_score(predict_results, target_test))


# 决策树可视化
import pydotplus
import os

os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'  #注意修改你的路径
dot_data = export_graphviz(dt_model,out_file=None,feature_names=iris.feature_names,class_names=iris.target_names,filled=True,rounded=True,special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png('iris.png')



