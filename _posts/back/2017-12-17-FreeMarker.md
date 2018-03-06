---
layout: post
title:  "FreeMarker 基本语法"
date:   2017-12-17
desc: "FreeMarker 基本语法"
keywords: "后端,FreeMarker"
categories: [Back]
tags: [后端,FreeMarker]
icon: icon-java
---

# 主要组成部分
FreeMarker模板文件主要由如下4个部分组成: 

1. **文本:**直接输出的部分 
2. **注释:**<#-- ... -->格式部分,不会输出 
3. **插值:**即${...}或#{...}格式的部分,将使用数据模型中的部分替代输出
    通用插值${expr};2,数字格式化插值:#{expr}或#{expr;format} 
4. **FTL指令:**FreeMarker指定,和HTML标记类似,名字前加#予以区分,不会输出
``` 
<!-- 如果该指令是一个用户指令而不是系统内建指令时,应将#符号改成@符号 -->
<#list animals as being><br> 
   <li>${being.name} for ${being.price} Euros<br> 
<#list><br>
```
*FreeMarker会忽略FTL标签中的空白字符.值得注意的是< , /> 和指令之间不允许有空白字符.*

# 内置函数

1. Sequence的内置函数
```
1.sequence?first 返回第一个值。
2.sequence?last 返回最后一个值。
3.sequence?reverse 倒序排序
4.sequence?size 返回大小
5.sequence?sort 将对象转化为字符串后排序
6.sequence?sort_by(value) 按对象的value属性排序
注意：Sequence不能为null
```

2. Hash的内置函数
```
1.hash?keys 返回hash里的所有key,返回结果为sequence
2.hash?values 返回hash里的所有value,返回结果为sequence
```

3. 操作字符串内置函数
   ```
   ${"str"?substring(0,2)}结果为st
   ${"str"?cap_first}结果为Str
   ${"Str"?cap_first}结果为str
   ${"str"?capitalize}结果为STR
   <#assign date1="2009-10-12"?date("yyyy-MM-dd")>
   <#assign date2="9:28:20"?time("HH:mm:ss")>
   <#assign date3="2009-10-12 9:28:20"?time("HH:mm:ss")>
   ${"string"?ends_with("ing")?string},是否由某个子串结尾 返回结果为true
   注意：布尔值必须转换为字符串才能输出
   ${"string"?html},将字符串中的<、>、&和"替换为对应得<>&quot:&amp
   ${"string"?index_of("in")结果为3
   ${"string"?index_of("ab")结果为-1
    length返回字符串的长度 ${"string"?length}结果为6
   ${"STRING"?lower_case}结果为string
   ${"string"?upper_case}结果为STRING
   ${"string"?contains("ing")?string}结果为true
   ${"111.11"?number}结果为111.11
   ${"111.11"?int}结果为111
   ${"STRING"?size}结果为6
   ${"strabg"?replace("ab","in")}结果为string
   <#list "This|is|split"?split("|") as s>${s}</#list>
    ${"   String   "?trim} 结果为String
    ${"hello, ${user}!"}   //字符串连接 
   ${"hello, " + user + "!"} //字符串连接 
   ${book[0]}${book[4]}   //截取子串 
   ${book[1..4]}     //截取子串
   
   ${r"${foo}"} 输出 ${foo} 
   ${r"C:\foo\bar"} 输出 C:\foo\bar
   ```
   格式化
   ```
   ${answer?string} 
   ${answer?string.number} 
   ${answer?string.currency} 
   ${answer?string.percent} 
   ${lastUpdated?string("yyyy-MM-dd HH:mm:ss zzzz")} 
   ${foo?string("yes", "no")} 
   ```
   转义字符:
   ``` 
   \";双引号(u0022) 
   \';单引号(u0027) 
   \\;反斜杠(u005C) 
   \n;换行(u000A) 
   \r;回车(u000D) 
   \t;Tab(u0009) 
   \b;退格键(u0008) 
   \f;Form feed(u000C)  
   \l;<  
   \g;>  
   \a;&  
   \{;{ 
   ```

4. 操作数字内置函数
   ```
   1, 算术运算符  +, - , * , / , % ,round, floor, ceiling,int
   2, 比较运算符 =或者==   !=: >或者gt >=或者gte <或者lt <=或者lte 
   3, 逻辑运算符  &&  ||  ! 
   4, c 用于将数字转换为字符串
   5, string用于将数字转换为字符串：number,currency（货币）和percent(百分比)其中number为默认的数字格式转换
      ${tempNum?string.number}或${tempNum?string("number")} 结果为20
   6, 2..5等同于`[2, 3, 4, 5]
   7, #{2.5837; M2} <#-- 小数部分最大X位,输出2.58 -->
   8, #{2.8; m2} <#-- 小数部分最小X位,输出2.80 -->
   9, #{expr;format}格式化数字
   ```
   运算符的优先级
   ```
   1,一元运算符:! 
   2,内建函数:? 
   3,乘除法:*, / , % 
   4,加减法:- , + 
   5,比较:> , < , >= , <= (lt , lte , gt , gte) 
   6,相等:== , = , != 
   7,逻辑与:&& 
   8,逻辑或:|| 
   9,数字范围:.. 
   ```

5. 操作布尔值内置函数
```
string用于将布尔值转换为字符串输出:true转为"true"，false转换为"false"
foo?string("yes","no")如果布尔值是true,那么返回"yes",否则返回no
```

6. 空值处理运算符 
```
![defaultValue]:指定缺失变量的默认值 
??:判断某个变量是否存在 布尔值
```

# 常用逻辑控制语法

```
<#setting number_format="currency" locale="国家/语言" boolean_format="布尔值格式" date_format="" time_format="" datetime_format="" time_zone="时区 " /> 
<#assign answer=42/> 
${answer}

<#if (age>60)>老年人 
<#elseif (age>40)>中年人 
<#elseif (age>20)>青年人 
<#else> 少年人 
</#if> 

<#switch value> 
<#case refValue>...<#break> 
<#case refValue>...<#break> 
<#default>... 
</#switch> 

<#list sequence as item> 
item_index:当前变量的索引值 
item_has_next:是否存在下一个对象 
<#break>指令跳出迭代 
</#list>

<#list ["星期一", "星期二", "星期三"] + ["星期四", "星期五", "星期六", "星期天"] as x> 
${x} //${week[2]}   week[3..5]
</#list> 

<#include filename [options]>  options包含encoding和parse（true）
<#import "/lib/common.ftl" as com>导入/lib/common.ftl模板文件中的所有变量,放置com的

<#noparse>FreeMarker不处理的内容</#noparse> 
escape指令导致body区的插值都会被自动加上escape表达式 
<#escape x as x?html> 
First name:${firstName} 
<#noescape>...</#noescape> 
</#escape> 
等同于: 
First name:${firstName?html} 

创建或替换顶层变量
<#assign x> <#list ["星期一", "星期二", "星期三"] as n> ${n} </#list> </#assign> ${x} 
<#assign x="Hello ${user}!"> 
```

# 自定义指令 

1. 
```
<#macro book booklist>    //定义指令booklist是参数 
<#list booklist as book> 
   ${book} 
</#list> 
<#return> //随时结束该自定义指令
</#macro> 
<@book booklist=["spring","j2ee"] />   //使用
```

2. common.ftl：将一个HTML页面模板定义成一个page指令
   ```
   <#macro page title> 
   <html> 
   <head> 
      <title></title> 
   </head> 
   <body> 
      <h1>${title?html}</h1> 
      <#nested>      //用于引入用户自定义指令的标签体 
   </body> 
   </html> 
   </#macro>
   ```
   在其他页面引用page指令:
   ``` 
   <#import "/common.ftl" as com>     //导入页面 
   <@com.page title="book list">      //使用 
   <u1> 
   <li>spring</li> 
   <li>j2ee</li> 
   </ul> 
   </@com.page>
   ```

3. 循环变量
```
<#macro repeat count> 
<#list 1..count as x>     //使用 nested 指令时指定了三个循环变量 
   <#nested x, x/2, x==count> 
</#list> 
</#macro> 
<@repeat count=4 ; c halfc last> 
${c}. ${halfc}<#if last> Last! </#if> 
</@repeat> 
```
