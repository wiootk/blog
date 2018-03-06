---
layout: post
title:  "mysql导入导出"
date:   2017-09-11
desc: "mysql导入导出"
keywords: "Database,mysql,import,export"
categories: [Database]
tags: [Database,mysql,import,export]
icon: icon-mysql
---
1. 导出
```sql
<!-- 导出一个库 -->
mysqldump --user=db_user --password=pwd --complete-insert=TRUE --default-character-set=utf8 --skip-triggers dbname > "./dbname.sql"
<!-- 导出一个库，并压缩 -->
mysqldump --user=db_user --password=pwd --complete-insert=TRUE --default-character-set=utf8 --skip-triggers dataBase  | gzip > "./dataBase.sql.$(date +%Y%m%d%H%M%S).tar.gz"
<!-- 导出一个表 -->
mysqldump -u db_user -p pwd dbname tablename > tablename.sql 
<!-- 导出一个数据库结构 -->
mysqldump -u db_user -p pwd -d --add-drop-table dbname> d:\dbname.sql
```
2. 导入
```sql
mysql --user=root --password=_pwd
use dataBase
source ./dataBase.sql
```
*shell文件 import.sh*
```shell
mysql --user=root --password=_pwd;
use $1;
source "./$2";
exit;
```
使用 ./import.sh  dataBase dataBase.sql
```sql
mysql -u用户名 -p密码 数据库名 < 数据库名.sql
```
3. 方式2
```sql
导出: Select语句 into outfile '保存路径+文件名';
导入：load data local infile '保存路径+文件名' into table 表名 character set utf8;
```
4. 使用bat脚本减少人肉运维（导出csv）  
  新建查询导出sql脚本:test.sql  
```sql
  use demo3;
  set @id=3;
  SELECT (@id:=id) AS vehId from `user` where `id`=@id;
  SELECT *  from `user` where id=@id into outfile 'D:/1.csv' fields terminated by ','optionally enclosed by ''lines terminated by '\r\n';
```
  新建调用sql脚本的bat文件：aaa.bat  
```shell
  @echo off  
  set errorlevel=0  
  set db=demo3  
  set user=root  
  set password=root  
  mysql -u%user% -p%password% -D%db% < test.sql  
```
5. 使用bat脚本减少人肉运维（导出sql文件）    
```
    @echo off  
    :start
    set errorlevel=0 
    set user=root  
    set password=root  
    set db=demo3
    set table=
    set /p table=请输入表名:  
    if defined table ( 
      goto XX
    ) else (
      goto YY
    )  
    :YY
    set table=user  
    goto XX  
    :XX
    mysql  -u%user% -p%password% -e"select id from user where id=3" %db% > tmp.txt
    for /f "tokens=* skip=1" %%f in (tmp.txt) do (
    :: tokens=2 第几列 delims 分隔符 
    :: skip忽略前多少行，eol指定当以什么符号开始时忽略它
    echo %%f 
      set where="`id` in (%%f)"
      goto ZZ    
    )  
    :ZZ
    mysqldump  -t  --compact -u%user% -p%password% %db% %table% --where=%where% >> D:/mysql/1.sql
    pause&goto start
  :: 多条insert --skip-extended-insert
  :: 只备份表结构 --no-data  或 --opt -d
  :: 只备份数据 -t
  :: 从备份文件恢复数据库  mysql database < file
  :: -B　数据库名　--table　表名
  ::  –skip-add-locks   (取消LOCK语句)
  ::  –skip-add-drop-table  (取消drop语句)
  ::  --skip-comments   (取消注释)
  :: 字符集 --default-character-set=utf8
  ::  > 文件名：先清空后写入  >>文件名,将追加到末尾。  
  :: 导入数据： 
  :: mysql　数据库名　<　文件名 
  :: source　/tmp/xxx.sql
```












   
   
  


 










 

        







 
 
