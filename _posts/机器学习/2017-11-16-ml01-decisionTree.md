---
layout: post
title:  "决策树（decision tree）"
date:   2017-11-16
desc: "决策树（decision tree）"
keywords: "机器学习,python,决策树,decision tree"
categories: [Machinelearn]
tags: [机器学习,python,决策树,decision tree]
icon: icon-python
---
# 机器学习中算法的评价
    1. 准确率
    2. 速度
    3. 强壮性
    4. 可规模性
    5. 可解释性

# 什么是决策树（decision tree）
决策树是机器学习中分类方法中一个重要的算法  
决策树是一个类似于流程图的树结构：其中，每个内部结点表示在一个属性上的测试，每个分支代表一个属性输出，而每个树叶结点代表类或类分布。树的最顶层是根结点  
优点：直观，便于理解，小规模数据集有效  
缺点：处理连续变量不好 ,类别较多时，错误增加的比较快 ,可规模性一般  
<img src="{{ site.blog_img }}/ml/01-01.jpg" alt='决策树' width="75%">

## 熵（entropy）
一条信息的信息量大小和它的不确定性有直接的关系  
信息量的度量就等于不确定性的多少  
变量的不确定性越大，熵越大  
## 决策树归纳算法（ID3）
优先选择信息获取量最大的属性作为属性判断结点  
信息获取量(Information Gain)：Gain(A) = Info(D) - Infor_A(D)  
<img src="{{ site.blog_img }}/ml/01-02.jpg" alt='数据集' width="60%">  

<img src="{{ site.blog_img }}/ml/01-03.jpg" alt='Info(D)没有D的熵' width="51%">  
<img src="{{ site.blog_img }}/ml/01-04.jpg" alt='Infor_A(D)有D的熵' width="51%">  

<img src="{{ site.blog_img }}/ml/01-05.jpg" alt='信息获取量Gain(A)' width="51%">  
同理，计算income，student，credit_rating的信息获取量，因为age的信息获取量最大，所以首先将age属性作为节点来分枝  
### 算法步骤：
  1. 树以代表训练样本的单个结点开始。 
  2. 如果样本都在同一个类，则该结点成为树叶，并用该类标号。  
  3. 否则，算法使用称为信息增益的基于熵的度量作为启发信息，选择能够最好地将样本分类的属性。该属性成为该结点的“测试”或“判定”属性。在算法的该版本中，所有的属性都是分类的，即离散值。连续属性必须离散化。  
  4. 对测试属性的每个已知的值，创建一个分枝，并据此划分样本。  
  5. 算法使用同样的过程，递归地形成每个划分上的样本判定树。一旦一个属性出现在一个结点上，就不在该结点的任何后代上考虑它  
  6. 递归划分步骤仅当下列条件之一成立停止：   
    (a) 给定结点的所有样本属于同一类。  
    (b) 没有剩余属性可以用来进一步划分样本。在此情况下，使用多数表决。这涉及将给定的结点转换成树叶，并用样本中的多数所在的类标记它。替换地，可以存放结点样本的类分布。  
    (c) 分枝test_attribute = a，没有样本。在这种情况下，以 samples 中的多数类创建一个树叶。  

## 其他决策树算法
C4.5: Quinlan  
Classification and Regression Trees (CART): (L. Breiman, J. Friedman, R. Olshen, C. Stone)   
**共同点** 都是贪心算法，自上而下(Top-down approach)   
**区别** 属性选择度量方法不同： C4.5 （gain ratio), CART(gini index), ID3 (Information Gain)  

## 如何处理连续性变量的属性

离散化（阈值的选择很关键）

## 树剪枝叶 （避免overfitting)

先剪枝
后剪枝

# 决策树算法实现（scikit-learn）  
1. python机器学习的库：scikit-learn  
**特性：**   
1）简单高效的数据挖掘和机器学习分析   
2）对所有用户开放，根据不同需求高度可重用性   
3）基于Numpy, SciPy和matplotlib   
4）开源，商用级别：获得 BSD许可  
**覆盖问题领域：**   
分类（classification),，回归（regression)， 聚类（clustering)， 
降维(dimensionality reduction)，模型选择(model selection)， 预处理(preprocessing)  
2. 使用scikit-learn  
**方式一：**pip, easy_install（两个都是python安装package的工具，感觉pip更好用）   
**方式二（推荐）：** Anaconda(科学计算环境 ，包含numpy, scipy，matplotlib等科学计算常用package，当然也包含scikit-learn包）   
3. [安装Graphviz（数据可视化软件）](http://www.graphviz.org/Download_windows.php)  
系统变量: path追加：`;C:\Program Files (x86)\Graphviz2.38\bin`  

## 算法实现  
    1. 将原始数据录入[csv文件]({{ site.blog_img }}/ml/01-06.csv)
    2. 引入sk-learn相关的package
    3. 读取csv文件的数据到程序中
    4. 对数据预处理
    5. 决策树分类的核心代码
    6. 生成dot文件（结果不够直观）
    dot文件：
    7. 将dot文件用graphviz转换为pdf文件
        在命令行下，cd到你的dot文件的路径下，输入 
        `dot -Tpdf filename.dot -o output.pdf` 

[源程序]({{ site.blog_img }}/ml/01-07.py)
```py
#coding=gbk

# DictVectorizer:数据类型转换
from sklearn.feature_extraction import DictVectorizer

# csv:原始数据放在csv文件中，该package为python自带，不需要安装
import csv

#引入sk-learn数据预处理包、决策树包、读写字符串包
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals.six import StringIO


#从csv文件中读取数据，并保存到allElectronicsData变量中
allElectronicsData = open(r'.\01-06.csv','r')
# csv的reader方法按行读取数据
reader = csv.reader(allElectronicsData)
#next方法读取到csv文件的第一行数据
headers = next(reader)
#打印第一行数据
print(headers)


#建两个list，featureList装特征值，labelList装类别标签
featureList = []
labelList = []

#遍历csv文件的每一行
for row in reader:
    #将类别标签加入到labelList中
    labelList.append(row[len(row)-1])
    #下面这几步的目的是为了让特征值转化成一种字典的形式，就可以调用sk-learn里面的DictVectorizer，直接将特征的类别值转化成0,1值
    rowDict = {}
    for i in range(1,len(row)-1):
        rowDict[headers[i]] = row[i]
    featureList.append(rowDict)
print(featureList)

#实例化    
vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()
print("dummyX:"+str(dummyX))
print(vec.get_feature_names())

# label的转化，直接用preprocessing的LabelBinarizer方法
lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
print("dummyY:"+str(dummyY))
print("labelList:"+str(labelList))


#criterion是选择决策树节点的标准，这里是按照“熵”为标准，即ID3算法；默认标准是gini index，即CART算法。
clf = tree.DecisionTreeClassifier(criterion = 'entropy')
clf = clf.fit(dummyX,dummyY)
print("clf:"+str(clf))

#生成dot文件
with open("allElectronicInformationGainOri.dot",'w') as f:
    f = tree.export_graphviz(clf,feature_names = vec.get_feature_names(),out_file = f)

#测试代码，取第1个实例数据，将001->100，即age：youth->middle_aged    
oneRowX = dummyX[0,:]
print("oneRowX:"+str(oneRowX))
newRowX = oneRowX
newRowX[0] = 1
newRowX[2] = 0
print("newRowX:"+str(newRowX))

#预测代码
predictedY = clf.predict(newRowX)
print("predictedY:"+str(predictedY))
```
执行：`python 01-07.py`

**参考文档**
[sk-learn的决策树文档](scikit-learn.org/stable/modules/tree.html)













  

