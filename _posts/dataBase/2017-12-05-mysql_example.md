---
layout: post
title:  "记一次数据库异构（数据源：mysql）"
date:   2017-12-05
desc: "记一次数据库异构（数据源：mysql）"
keywords: "Database,mysql,isomerism"
categories: [Database]
tags: [Database,mysql,isomerismt]
icon: icon-mysql
---
1. 删除表  
`DROP TABLE IF EXISTS baseinfo ;`
2. 创建表
```sql
  CREATE TABLE baseinfo
  SELECT (@i:=@i+1) AS id , null as emid,
  if(arc.date1 is null||arc.date1 ="",arc.beginDate,
  arc.date1)  AS  date1,group_concat(distinct arc.certNo) AS certcode,
   FROM_UNIXTIME(arc.time/1000,'%Y-%m-%d %H:%i:%s') AS time1 ,
   CONCAT("类型",case arc.type WHEN 1 then '一'  WHEN 2 then '二' end) AS type,  
   group_concat(distinct arc.type) as certtype   
  from archive arc,(select @i:=0) as it
  WHERE  arc.status=2 GROUP BY arc.id ;
```
3. 创建索引
```sql
ALTER TABLE baseinfo ADD INDEX index_emid (emid);
-- DROP INDEX index_emid ON baseinfo;
```
4. 更改字段类型  
`alter table baseinfo modify column emid bigint;`
5. 更新字段值  
`UPDATE base_d bd,baseinfo bas SET bd.emid=bas.ID WHERE bd.oldID=bas.oldID;`
6. 查询多余一条的数据  
`select CONCAT(bas.id) AS ids from baseinfo bas  GROUP BY bas.type HAVING  count(*)>1;`
7. mysql 同步  
  7.1 （数据少：工具Navicat）：在原库选择表右键：复制-->在目标库右键：粘贴  
  7.2 （数据多）：[mysql导入导出](/blog/database/2017/09/11/mysql_import_export.html)  
