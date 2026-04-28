#！/usr/bin/env python3

#从sklearn.datasets 里导入新闻数据抓取器fetch_20newsgroups
from sklearn.datasets import fetch_20newsgroups
#需从互联网下载数据
news=fetch_20newsgroups(subset='all')

#查验数据规模和细节`
print (len(news.data))
print(news.data[0])

#数据分割
from sklearn.model_selection import train_test_split
#随机采样25%的数据样本作为测试集
X_train,X_test,y_train,y_test=train_test_split(news.data,news.target,test_size=0.25,random_state=33)


#使用朴素贝叶斯分类器进行预测
from sklearn.feature_extraction.text import CountVectorizer
vec=CountVectorizer()
X_train=vec.fit_transform(X_train)
X_test=vec.transform(X_test)
#从sklearn.naive_bayes里导入朴素贝叶斯模型
from sklearn.naive_bayes import MultinomialNB
#初始化朴素贝叶斯模型
mnb=MultinomialNB()
#使用 训练数据对模型参数进行估计
mnb.fit(X_train,y_train)
#对测试样本进行预测额，结果保留在储存变量y_predictio中
y_predict=mnb.predict(X_test)


#性能评估
from sklearn.metrics import classification_report
print('The Accuracy of Naive Bayes Classifier is',mnb.score(X_test,y_test))
print(classification_report(y_test,y_predict,target_names=news.target_names))

