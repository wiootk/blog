---
layout: post
title:  "springCloud分布式配置中心与消息服务"
date:   2018-01-06
desc: "springCloud分布式配置中心与消息服务"
keywords: "后端,springCloud,微服务,分布式配置中心,消息服务"
categories: [Back]
tags: [后端,springCloud,微服务,分布式配置中心,消息服务]
icon: icon-java
---
# 4. 分布式配置中心Spring Cloud Config
## 4.1 构建Config Server

1. pom.xml中引入spring-cloud-config-server依赖
   ```xml
   <modelVersion>4.0.0</modelVersion>
   <artifactId>sys_config</artifactId>
   <packaging>jar</packaging>
   <name>config</name>
   <dependencies>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-config-server</artifactId>
       </dependency>
   </dependencies>
   ```

2. 创建Spring Boot的程序主类，并添加@EnableConfigServer注解，
```java
@SpringBootApplication
@EnableConfigServer//开启Config Server
@EnableEurekaClient
//@EnableDiscoveryClient//激活Eureka中的DiscoveryClient实现
public class ConfigApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigApplication.class, args);
    }
}
```

3.  在GitHub上建立项目
      1. 建立项目`git@github.com/401718154/springCloud.git`  
      2. 配置Git以及上传代码  
      `git config --global user.name "Your Real Name"`  
      `git config --global user.email you@email.address`  
      3. 创建SSH key:  
         `ssh-keygen -C 'your@email.address' -t rsa`  
         打开Key保存位置，找到id_rsa.pub，复制字符  
         到GitHub找到`Account Settings-->SSH Public Keys-->Add another public key`    
      4. 下载项目：  
      `git clone https://github.com/401718154/springCloud`  
      `git clone gti@github.com:401718154/springCloud.git`  
      5. 右击Git Bash：
      ```shell
      //git init 
      //创建文件夹及文件
      git add .
      git commit -m 'Test'
      git remote add origin git@github.com:401718154/springCloud.git
      git push -u origin master
      ```
      6. 创建配置文件：
           1. didispace.properties        `from=git-default-1.0`
           2. didispace-dev.properties        `from=git-dev-1.0`
           在master中，1.0后缀，另建一个configTest分支，2.0后缀。
      7. git常用命令
      ```shell
      git branch -a        #查看远程分支
      git branch           #查看本地分支
      git branch configTest       #创建分支
      git push origin configTest  #把分支推到远程分支
      git checkout configTest    #切换分支到test 
      git branch -d xxxxx         #删除本地分支
      git remote  -v              #查看本地和远程分支 
      git push origin :br-1.0.0   #删除远程版本 
      git branch -r -d origin/branch-name #删除远程分支
      git push origin :branch-name  
      git push -u origin configTest
      ```

4. application.properties：
```properties
spring.application.name=config-server
server.port=7001
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
#################################################################
#配置git仓库地址
#搜索位置，可配多个
spring.cloud.config.server.git.uri=https://github.com/wiootk/springCloud/
#配置仓库路径
spring.cloud.config.server.git.searchPaths=config
#配置仓库的分支  master/configTest
#spring.cloud.config.label=master
spring.cloud.config.server.git.username=401718154@qq.com
spring.cloud.config.server.git.password=215sos716
#通过服务来访问ConfigServer的功能
spring.cloud.config.discovery.enabled=true
spring.cloud.config.discovery.service-id=config
#################################################################
#本地存储配置
#spring.profiles.active=native
#默认从应用的src/main/resource目录下检索配置文件
#spring.cloud.config.server.native.searchLocations=file:F:/properties
#################################################################
#http://localhost:7001/didispace/from
#http请求地址和资源文件映射
#/{application}/{profile}[/{label}]
#/{application}-{profile}.yml
#/{label}/{application}-{profile}.yml
#/{application}-{profile}.properties
#/{label}/{application}-{profile}.properties
```

5. 访问configTest分支的didispace的dev文件：`http://localhost:7001/didispace/dev/configTest`  
   url会映射{application}-{profile}.properties



## 4.2 客户端验证

1. 父项目pom.xml：
   ```xml
   <!-- config 分布式配置中心-->
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-config</artifactId>
   </dependency>
   ```

2. sys_client模块创建ConfigController
```java
@RefreshScope
@RestController
class ConfigController {
    private final Logger logger = Logger.getLogger(getClass());
    //    http://localhost:2222/from
    //  post  http://localhost:2222/refresh  刷新数据
    @Value("${from}")
    private String from;
    @RequestMapping("/from")
    public String from() {
        return this.from;
    }
}
```

3. 创建bootstrap.properties：
```properties
server.port=2222
#对应前配置文件中的{application}部分
spring.application.name=didispace
spring.cloud.config.discovery.serviceId=config-server
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
spring.cloud.config.discovery.enabled=true
#忽略权限拦截
management.security.enabled=false
#security.user.name=admin
#security.user.password=123
#management.security.enabled=true
#management.security.role=ADMIN
#刷新 http://localhost:2222/refresh
##############################
##远程仓库的分支
#对应前配置文件的git分支
spring.cloud.config.label=master
##dev/test/pro
#对应前配置文件中的{profile}部分
spring.cloud.config.profile=dev
#配置中心的地址
spring.cloud.config.uri= http://localhost:7001/
#对应的配置文件    didispace-dev.properties
```
注释或删除application.properties 相关配置

4. 测试  
访问：`http://localhost:2222/from`  
修改github上数据 再次访问`http://localhost:2222/from`  
post访问 `http://localhost:2222/refresh`刷新数据  
访问`http://localhost:2222/from`  

# 5. 消息总线
消息代理中间件可以将消息路由到一个或多个目的地

## 5.1 Spring Cloud Bus
**先安装RabbitMQ**  
[Erland](http://www.erlang.org/downloads){:target=_bank}  
[RabbitMQ](https://www.rabbitmq.com/download.html){:target=_bank}  
**Rabbit管理**  
进入mq安装目录（sbin）执行`rabbitmq-plugins enable rabbitmq_management`命令  
*（启动报错：将 C:\WINDOWS\.erlang.cookie   同步到RabbitMq 启动用户C:\Users\%USERNAME%\.erlang.cookie ）*  
Web管理插件：http://localhost:15672/，用户guest,密码guest  

1. 父项目pom.xml
   ```xml
   <!-- 消息总线 amqp-->
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-bus-amqp</artifactId>
   </dependency>
   ```

2. 在sys_config、sys_client 配置文件
```properties
spring.cloud.bus.trace.enabled=true
#忽略权限拦截
management.security.enabled=false
spring.rabbitmq.host=localhost
spring.rabbitmq.port=5672
spring.rabbitmq.username=test
spring.rabbitmq.password=123456
#管理界面 http://localhost:15672/  guest guest
#刷新 http://localhost:2222/bus/refresh 指定服务刷新“/bus/refresh?destination=customers:**”
```

3. 测试
启动sys_config，两个sys_client  
访问两个sys_client的/from请求  
修改didispace-dev.properties中的from值  
并发送POST请求到客户端或服务端的/bus/refresh  
指定刷新范围：/bus/refresh?destination=customers:**  
访问两个sys_client的/from请求  

## 5.1 Kafka(待学习)

Kafka是一个由LinkedIn开发的分布式消息系统，Kafka是基于消息发布/订阅模式实现的消息系统，主要设计目标：消息持久化、高吞吐、分布式、跨平台、实时性、伸缩性  
下载并解压[kafka](http://kafka.apache.org/downloads.html){:target=_bank}  
启动ZooKeeper：zookeeper-server-start config/zookeeper.properties
zookeeper.properties绑定2181端口  
启动Kafka：kafka-server-start config/server.properties
配置文件中zookeeper.connect设置ZooKeeper的地址和端口，它默认会连接本地2181端口的ZooKeeper；设置多个ZooKeeper节点：zookeeper.connect=127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002   
创建Topic：kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test  
创建一个名为“test”的Topic，该Topic包含一个分区一个Replica。在创建完成后，可以使用kafka-topics --list --zookeeper localhost:2181命令来查看当前的Topic  
创建消息生产者：kafka-console-producer --broker-list localhost:9092 --topic test  
创建消息消费者：kafka-console-consumer --zookeeper localhost:2181 --topic test --from-beginning  

1. 父项目pom.xml
把spring-cloud-starter-bus-amqp替换成spring-cloud-starter-bus-kafka模块
```xml
<!-- 消息总线 kafka-->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-kafka</artifactId>
</dependency>
```

2. 修改sys_config、sys_client配置文件
```properties
#kafka
spring.cloud.stream.kafka.binder.zk-nodes=localhost:2181
spring.cloud.stream.kafka.binder.brokers=localhost:9092
spring.cloud.bus.trace.enabled=true
```
3. 启动 ZooKeeper、Kafka
修改kafka_2.12-1.0.0\bin\windows\kafka-run-class.bat文件将：
set COMMAND=%JAVA% %KAFKA_HEAP_OPTS%
 %KAFKA_JVM_PERFORMANCE_OPTS%
 %KAFKA_JMX_OPTS% %KAFKA_LOG4J_OPTS%
 -cp %CLASSPATH% %KAFKA_OPTS% %的 %CLASSPATH% 用双引号。

 `.\bin\windows\kafka-server-start.bat .\config\server.properties` 

 http://blog.csdn.net/derrantcm/article/details/73368538






