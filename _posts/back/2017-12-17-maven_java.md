---
layout: post
title:  "maven环境下java开发"
date:   2017-12-17
desc: "maven环境下java开发"
keywords: "后端,maven,java"
categories: [Back]
tags: [后端,maven,java]
icon: icon-java
---
**说明：**实现两个业务:加法、减法
1. 新建maven工程：tool
添加依赖 pom.xml
```xml
    <properties>
        <maven.compiler.encoding>UTF-8</maven.compiler.encoding>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    <dependencies>
        <!-- 单元测试-->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.9</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <pluginManagement>
            <plugins>
                <!-- api 文档-->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-javadoc-plugin</artifactId>
                    <version>2.9.1</version>
                    <configuration>
                        <reportOutputDirectory>../javadocs</reportOutputDirectory>
                        <destDir>tool</destDir>
                    </configuration>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
```

2. 新建文件：com.jun.tool.java
```java
public class Tool {
    public int add(int a,int b){
        return  a+b;
    }
    public int subtract(int a,int b){
        return  a-b;
    }
}
```

3. 新建测试文件：  
ToolTest.java
```java
public class ToolTest {
    Tool tool = new Tool();
    @BeforeClass// 必须是static...因为方法将在类被装载的时候就被调用(那时候还没创建实例)
    public static void setUpBeforeClass() throws Exception {
        System.out.println("global BeforeClass");
    }
    @AfterClass
    public static void tearDownAfterClass() throws Exception {
        System.out.println("global destory AfterClass");
    }
    @Before
    public void before() {
        System.out.println("开始测试喽！");
    }
    @After
    public void after() {
        System.out.println("测试结束！");
    }
    @Test
    public void testAdd() {
        Assert.assertEquals(6, tool.add(2, 4));
    }
    @Test
    public void testSubtract() {
        Assert.assertEquals(3, tool.subtract(6, 4));
    }
}
```
ToolTest2.java
```java
public class ToolTest2 {
    Tool tool = new Tool();
    @Test
    public void testSubtract2() {
        Assert.assertEquals(2, tool.subtract(6, 4));
    }
}
```
AllTest.java
```java
@RunWith(Suite.class)
@Suite.SuiteClasses({ToolTest.class,ToolTest2.class})
public class AllTest {
}
```

4. Maven生成javadoc(api)
修改 com.jun.tool.java

   ```java
   /*
   * @(#)Tool.java 　　1.0 2017/12/09
   */
   package com.jun;
   /**
    *  * Description:
    * <br/>描述
    * 工具类
    * @author 作者
    * @version 1.0
    */
   public class Tool {
       /**
        * 加法
        * @author (作者2)
        * @version (2.0)
        * @see com.jun.Tool#add(int, int)
        * @param a int 参数
        * @param b int 参数
        * @return 参数相加
        * @throws Exception 异常了
        * @deprecated (将要被废弃)
        */
       public int add(int a,int b) throws Exception{
           return  a+b;
       }
       /**
        * 减法
        * @param a int 参数
        * @param b int 参数
        * @return 参数相加
        */
       public int subtract(int a,int b){
           return  a-b;
       }
   }
   ```
**在项目目录下执行：**`mvn javadoc:javadoc`

