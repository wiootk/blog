---
layout: post
title:  "cmd提取增量(某天之后)文件"
date:   2018-01-27
desc: "cmd提取增量(某天之后)文件"
keywords: "cmd,增量文件"
categories: [Mixed]
tags: [cmd,增量文件]
icon: icon-shell
---
**介绍：**  
提取某天之后编辑过的文件，进行系统增量部署。  
脚本为windows平台下的bat文件  

1. 新建 EXCLUDE.txt 内容为提取时进行排除的文件
```
lib
node_modules
js\appInfo.js
```

2. 新建 xcopyTime.bat 使用xcopy进行指定的文件提取
```
@echo off 
rem xcopy2.BAT transfers all files in all subdirectories of 
rem the source drive or directory (%1) to the destination 
rem drive or directory (%2) 
rem lastModifyTime (%3) 
xcopy %1 %2 /s /d:%3 /exclude:EXCLUDE.txt /y 
if errorlevel 4 goto lowmemory 
if errorlevel 2 goto abort 
if errorlevel 0 goto exit 
:lowmemory 
echo Insufficient memory to copy files or 
echo invalid drive or command-line syntax. 
goto exit 
:abort 
echo You pressed CTRL+C to end the copy operation. 
goto exit 
:exit
pause
```

3. 新建copyFile.bat接收输入参数(不输入参数：默认当天)调用 xcopyTime.bat
   ```
   @echo off
   :start
   set "source=F:\yunzhengf\sill"
   set "target=C:\Users\Administrator\Desktop\copyFile\"
   set startDate=
   set /p startDate=请输入指定日期[如06-19]:
   
   if defined startDate ( 
   goto YY
   ) else (
   goto XX
   )
   
   :YY
   echo 复制 %startDate% 之后的文件
   xcopyTime %source% %target% %startDate%-2018
   pause&goto start
   
   :XX
   set startDate=%date:~5,2%-%date:~8,2%
   echo 复制 %startDate% 之后的文件
   xcopyTime %source% %target% %startDate%-2018
   pause&goto start
   
   pause
   ```

