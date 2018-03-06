#coding=gbk

# DictVectorizer:数据类型转换
from sklearn.feature_extraction import DictVectorizer

# csv:原始数据放在csv文件中，该package为python自带，不需要安装
import csv

#引入数据预处理包、决策树包、读写字符串包
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