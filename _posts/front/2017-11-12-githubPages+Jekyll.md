---
layout: post
title:  "基于github Pages和Jekyll的博客搭建"
date:   2017-11-12
desc: "基于github Pages和Jekyll的博客搭建"
keywords: "前端,github Pages,Jekyll,博客"
categories: [Front]
tags: [前端,github Pages,Jekyll,博客]
icon: icon-Jekyll
---
# 环境搭建
1. [下载安装 Ruby 和 DevKit](http://rubyinstaller.org/downloads/)  
    *安装路径不要带空格，勾选 “Add Ruby ... to your PATH”*  
    检测：ruby -v gem -v  
2. 安装 DevKit  
    （命令行）初始化创建 config.yml：  
    ```
    cd C:\DevKit
    ruby dk.rb init
    notepad config.yml
    ```
    末尾添加新的一行 - C:\Ruby200-x64，保存文件并退出  
    2. 审查（非必须）并安装  
        ```
        ruby dk.rb review
        ruby dk.rb install
        ```
3. 安装 Jekyll:`gem install jekyll`  
4. 安装 Pygments(语法高亮插件)  
需要安装 Python 并在配置文件_config.yml 里设置 highlighter 为pygments  
*不久之前，Jekyll 还添加另一个高亮引擎名为 Rouge， 尽管暂时不如 Pygments 支持那么多的语言，但它是原生 Ruby 程序，而不需要使用 Python*  
    1. 安装 Python2  
    下载  http://www.python.org/download/->添加安装路径 (如： C:\Python27) 至 PATH->检验 python –V
    2. 安装 Easy Install  
    下载 [ez_setup.py](https://pypi.python.org/pypi/ez_setup) --> python ez_setup.py-->(查看 Python 路径import sys print sys.path )添加 'Python Scripts' 路径至 PATH->easy_install --version  
    3. 安装 Pygments  
        ```
        easy_install Pygments
        gem install bundler
        ```
    4. RubyGems 淘宝镜像  
        ```
        gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
        gem sources -l
        gem install rails
        ```
        或用 Bundler 的 Gem 源代码镜像命令  
        ```
        $ bundle config mirror.https://rubygems.org https://gems.ruby-china.org
        //这样你不用改你的 Gemfile 的 source
        source 'https://rubygems.org/'
        gem 'rails', '4.1.0'
        ```
    5. 启动 Jekyll  
        `jekyll new myblog&&cd myblog&&jekyll serve --watch`
        浏览:localhost:4000

# 创建空白项目
## git初始化  
`$ mkdir blog && cd blog && git init&& git checkout --orphan gh-pages`  
创建没有父节点的分支gh-pages。因为github规定，只有该分支中的页面，才会生成网页文件
##  创建设置文件  
根目录/_config.yml  
　　`baseurl: /blog`  
##  创建模板文件  
根目录/_layouts目录(存放模板文件,Jekyll使用Liquid模板语言)  
　　`mkdir _layouts&&cd _layouts&& touch default.html`  
default.html  
```html
　　<!DOCTYPE html>
　　<html>
　　<head>
　　　　<meta http-equiv="content-type" content="text/html; charset=utf-8" />
　　　　<title>\{\{ page.title \}\}</title>
　　</head>
　　<body>
　　　　\{\{ content \}\}
　　</body>
　　</html>
```

##  创建文章  
　　`mkdir _posts&&cd _posts&&touch 2017-05-20-博客搭建.md`  
填入以下内容  
```html
    ---
　　layout: default
　　title: 你好，世界
　　---
　　<h2>\{\{ page.title \}\}</h2>
　　<p>我的第一篇文章</p>
　　<p>\{\{ page.date | date_to_string \}\}</p>
```
三根短划线"---"：元数据，标记开始和结束  
"layout:default"，表示该文章的模板使用_layouts目录下的default.html文件  
"title: 你好，世界"，表示该文章的标题是"你好，世界"  
##  创建首页  
根目录/index.html  
```html
　　---
　　layout: default
　　title: 我的Blog
　　---
　　<h2>\{\{ page.title \}\}</h2>
　　<p>最新文章</p>
　　<ul>
　　　　\{\% for post in site.posts \%\}
　　　　　　<li>\{\{ post.date | date_to_string \}\} <a href="{{ site.baseurl }}{{ post.url }}">\{\{ post.title \}\}</a></li>
　　　　\{\% endfor \%\}
　　</ul>
```
输出内容两层大括号，单纯命令一层大括号。`{{site.baseurl}}`  是_config.yml中设置的baseurl变量  

##  发布内容  
加入本地git库:  
　　`git add .&& git commit -m "first post"`  
前往github创建一个名为blog库，将本地内容推送到github  
> git remote add origin https://github.com/401718154/blog.git  
git push origin gh-pages  

访问hhttps://401718154.github.io/blog/

##   绑定域名  

# 主题使用
1. 克隆模板
`git clone git://github.com/jarrekk/Jalpc.git`
注释掉：
```
#gems:
#  - jekyll-assets
```
2. 编写启动文件
```
@echo off  
start cmd /k "jekyll serve --watch"  
start http://localhost:4000/blog/ 
```
4. 社会化评论插件 （有言）
    1. 注册友言账户，点击获取代码  
    `<!-- UY BEGIN -->`  
    `<div id="uyan_frame"></div>`  
    `<script type="text/javascript" src="http://v2.uyan.cc/code/uyan.js?uid=2143694"></script>`  
    `<!-- UY END -->`  

    2. 修改Jekyll  
        1. 修改_config.yml  
            ```yml
            uyan:
              uid: 2143694
            ```
        2. 修改_includes /comments  
            ```html
            {% if site.uyan %}
            <div id="uyan_frame"></div>
            <script>
                (function() {
                    var d = document, s = d.createElement('script');
                    s.src = '//v2.uyan.cc/code/uyan.js?uid={{site.uyan.uid}}';
                    s.setAttribute('data-timestamp', +new Date());
                    (d.head || d.body).appendChild(s);
                })();
            </script>
            {% endif %}            
            ```
        3. 提交到github  
            1. 创建`.gitignore` 添加 `_site/*`  
            2.  
                ```
                $ git init
                $ git add .
                $ git commit -m "init blog"
                $ git remote add origin xxxxxxx（拷贝github的地址）xxxxxxx.git
                $ git push origin master
                ```

# todo
http://www.pchou.info/open-source/2014/04/03/git-gitolite-hook.html







