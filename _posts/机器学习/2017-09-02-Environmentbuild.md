---
layout: post
title:  "windows平台搭建python机器学习环境"
date:   2017-09-02
desc: "Machine learn desc"
keywords: "机器学习,python,环境搭建"
categories: [Machinelearn]
tags: [机器学习,python,环境搭建]
icon: icon-python
---


### 1. 安装[python 2.7](https://www.python.org/downloads/)  

1. 在上面路径下在download 标签下载windows版本
2. 安装，一路next（注意安装路径）
3. cmd命令行：python （python不是内部或外部命令：Path环境变量添加python的安装路径）
4. 退出： exit() 或 ctrl+z  

### 2. 	安装 Easy Install  

1. 下载[ez_setup.py](https://pypi.python.org/pypi/ez_setup)  
2. python ez_setup.py  
3. (查看 Python 路径import sys print sys.path )添加 ‘Python Scripts’ 路径至 PATH  
4. easy_install --version  
5. 国内镜像  
	豆瓣PyPi镜像：http://pypi.douban.com/simple/  
	阿里云PyPi源：http://mirrors.aliyun.com/pypi/simple/  
	中科大PyPi源：http://pypi.mirrors.ustc.edu.cn/  
 	1. 手动  
		pip install web.py -i http://mirrors.aliyun.com/pypi/simple  
		easy_install -i http://pypi.douban.com/simple    
	2. 创建或修改配置文件（linux的文件在~/.pip/pip.conf，windows在C:\Users\Administrator\pip\pip.ini） 
	```
	[global]  
	index-url = http://mirrors.aliyun.com/pypi/simple #镜像源  
	trusted-host = mirrors.aliyun.com            #添加镜像源为可信主机  
	disable-pip-version-check = true          #取消pip版本检查，排除每次都报最新的pip  
	timeout = 120
	```
    创建或修改配置文件（linux的文件在~/.pydistutils.cfg，windows在C:\Users\Administrator\pydistutils.cfg）
	```  
	[easy_install]  
	index_url = http://mirrors.aliyun.com/pypi/simple
	```

	3. 修改源文件的下载路径：
	pip:			C:\Python27\Lib\site-packages\pip\models\index.py
	easy_install:	C:\Python27\Lib\site-packages\setuptools\command\easy_install.py	
	
### 3. 安装 Numpy(数值计算扩展：矩阵数据类型、矢量处理，以及精密的运算库)      

~~1 安装：pip install numpy 可以下载但与scipy 不同源安装会报错,卸载 pip uninstall numpy~~

  1.  安装：[Numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy) ->pip install numpy-1.13.3+mkl-cp27-cp27m-win_amd64.whl
  2.  测试：python->import numpy as py

### 4. 安装 scipy（数学、科学和工程计算包）
  1. 安装：[scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy) ->pip install scipy-0.19.1-cp27-cp27m-win_amd64.whl  
  2. 测试：python->import scipy as sy

### 5. 安装 MatplotLib（画图）
  1. 安装：pip install matplotlib
  2. 测试：python->import matplotlib as mb
  
### 6. 安装 scikit-learn（机器学习算法）
  1. 安装：pip install scikit-learn
  2. 测试：python->import sklearn as sl

### 7. 测试：

1. 斜线坐标 test1.py
	```py
	import matplotlib
	import numpy
	import scipy
	import matplotlib.pyplot as plt
	
	plt.plot([1,2,3])
	plt.ylabel('some numbers')
	plt.show()
	```
	运行：python test1.py

2. 矩阵数据集 test2.py
	```py
	from sklearn import datasets
	iris = datasets.load_iris()
	digits = datasets.load_digits()
	print digits.data
	```
	运行：python test2.py

### 8. IDEA安装Python环境  
  1. 安装插件：file->pluglns->python  
  2. 配置SDK：File->New module>python：module SDK:python路径/python.exe 
   
### 9. sublimeText3安装Python环境
  Ctrl+Shift+P-> Install Package ->插件名->安装
  SublimeCodeIntel,SideBarEnhancements,pylinter ,Terminal,AutoPep8,Anaconda,SublimeREPL
  1.   Tools > Build System > New Build System:输入： 
```
	"encoding": "utf-8",  
	"working_dir": "$file_path",  
	"shell_cmd": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python35-32\\python.exe -u \"$file\"",  
	"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",  
	"selector": "source.python"
```
	Ctrl + S 直接保存为想要命名的编译名称（python27）
	按ctrl +b 是执行操作的命令
  2.  快捷键f5=>执行程序： preferences>key bindings :
```
		{ 
		"keys":["f5"],  
		"caption": "SublimeREPL: Python - RUN current file",  
		"command": "run_existing_window_command", "args": {"id": "repl_python_run",  
		"file": "config/Python/Main.sublime-menu"} 
		}
```

  3.  快捷键：Preferences-->Browser Packages...-->进入相关的目录SublimeCodeIntel\.codeintel找到config
```
		{  
			"Python": {    
					"python":"C:/Python27/python.exe",    
					"pythonExtraPaths":    
						[    
							"C:/Python27",  
							"C:/Python27/DLLs",  
							"C:/Python27/Lib",   
							"C:/Python27/Lib/site-packages"    
						]    
						
				},    
		}
```

  4. SublimeTmpl：在settings-user中设置上自己的信息
``` 
		{  
            "disable_keymap_actions": false, // "all"; "html,css"  
            "date_format" : "%Y-%m-%d %H:%M:%S",  
            "attr": {  
                "author": "mx",  
                "email": "mengxiang@xiangcloud.com.cn",  
                "link": "http://www.xiangcloud.com.cn/"  
            }  
        } 
```

  5. 修改快捷键：ctrl+alt+p创建Python模板：key bindings-user添加  
``` 
		[   
			{  
				"caption": "Tmpl: Create python", "command": "sublime_tmpl",  
				"keys": ["ctrl+alt+p"], "args": {"type": "python"}  
			},  
		] 
```

### 10. 数据可视化
    [下载安装Graphviz](www.graphviz.org)
    系统变量: path追加：`;C:\Program Files (x86)\Graphviz2.38\bin`

### 深度学习
1.  theano windows安装及配置gpu  
~~打开 www.mingw.org-> Download Installer->mingw-get-setup.exe->安装->mingw32-gcc-g++->Mark for Installation->Installation:Apply changes
环境变量: ;C:\MinGW\bin->g++ -v~~
    1.  安装[anaconda](https://www.anaconda.com/download/#windows)([简版miniconda](https://conda.io/miniconda.html))为了安装python环境
        添加Anaconda的TUNA镜像 `conda config –add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/` 
        设置搜索时显示通道地址 `conda config –set show_channel_urls yes`
    2. `conda install mingw libpython` 
    修改path环境变量：`D:\Anaconda2\MinGW\bin;D:\Anaconda2\MinGW\x86_64-w64-mingw32\lib`
    3.  `pip install theano`

    4.  新建C:\Users\Administrator\.theanorc
        ```
        [global]  
        openmp=False  
        [blas]  
        ldflags=  
        [gcc]  
        cxxflags = -I"C:\Program Files\miniconda\MinGW" 
        ```
    5. 测试
        `pip install nose`
        ```py
        import theano
        theano.test()
        ```
2. 安装pylearn2 模块化
`pip install -e git+https://github.com/lisa-lab/pylearn2.git#egg=Package`
3. 对pylearn2的神经网络封装，兼容scikit-learn
```py
pip install scikit-neuralnetwork
git clone  https://github.com/aigamedev/scikit-neuralnetwork.git
cd scikit-neuralnetwork
pip install matplotlib
python setup.py develop
```
4. 测试
```
python examples/plot_mlp.py --params activation
python examples/bench_mnist.py sknn
```



基于scikitlearn的深度学习环境安装(三)(完整版)




















