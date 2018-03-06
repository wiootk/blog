---
layout: post
title:  "WebServices"
date:   2018-01-02
desc: "WebServices"
keywords: "后端,java,WebServices"
categories: [Back]
tags: [后端,java,WebServices]
icon: icon-java
---

WebServices:别人通过项目的网络地址，调用我们的方法  
本文基于IDEA搭建简单的WebServices环境  
# 1. 创建项目
在IDEA创建项目：`java --> java EE (WebServices) --> Version:ApacheAxis-->finish`  
创建lib文件夹并引入jar包：`file-->Project Structure-->Artifacts-->war exploded-->WEB-INF/lib/JAX-WS-Apache Axis`

# 2. 服务端
1. 编辑 service/HelloWord.java
```java
public class HelloWorld {    
    public String sayTitle(String from) {
        String result = "title is" + from;
        System.out.println(result);
        return result;
    }   
}
```
2. 文件右键：`Recomplie....`
3. 文件右键：`WebServices-->generate Wsdl from java code-->WEB Servere URL:host:8080//services/service/HelloWorld`  
同级目录下生成 HelloWord.wsdl  
4. 编辑(添加)web/WEB-INF/server-config.wsdd
   ```xml
     <service name="HelloWorldService" provider="java:RPC" style="document" use="literal">
       <parameter name="className" value="service.HelloWorld"/>
       <parameter name="allowedMethods" value="*"/>
       <parameter name="scope" value="Application"/>
       <namespace>http://service</namespace>
     </service>
   ```
5. 配置tomcat
6. 启动并访问：`http://localhost:8080/services`

# 3. 客户端
1. 创建 service 同级目录 client
2. 生成文件：文件夹右键-->`WebServices-->generate java code  from Wsdl-->WEB Servere wsdlURL:http://localhost:8080/services/HelloWorldService?wsdl` 

# 4. 测试
创建 test/Test.java
```java
import client.HelloWorldServiceSoapBindingStub;
import org.apache.axis.client.Service;
import java.net.URL;
public class Test {
    public static void main(String[] args) {
        try {
            URL  url = new URL("http://localhost:8080/services/HelloWorldService");
            HelloWorldServiceSoapBindingStub stub = new HelloWorldServiceSoapBindingStub(url,new Service());
            String resp=stub.sayTitle("  test");
            System.out.println(resp);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
