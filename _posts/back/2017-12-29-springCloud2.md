---
layout: post
title:  "springCloud微服务服务消费与均衡负载"
date:   2017-12-29
desc: "springCloud微服务服务消费与均衡负载"
keywords: "后端,springCloud,微服务,服务消费,均衡负载"
categories: [Back]
tags: [后端,springCloud,微服务,服务消费,均衡负载]
icon: icon-java
---
# 2.服务消费者(Ribbon)
Ribbon是一个基于HTTP和TCP客户端的负载均衡器。  
**准备工作**
```
启动服务注册中心：eureka-server：`java -jar simple.jar`
启动服务提供方：compute-service：`java -jar simple.jar >log2222.log`
再启动一个服务提供方:compute-service：`java -jar target/jun-1.0-SNAPSHOT.jar --server.port=2223 >log2223.log`
```

## 2.1 客户端负载均衡的消费者(Ribbbon)
**构建基本Spring Boot项目**  
1. pom.xml：
   ```xml
   <parent>
       <artifactId>springCloud</artifactId>
       <groupId>com.jun</groupId>
       <version>1.0-SNAPSHOT</version>
   </parent>
   <modelVersion>4.0.0</modelVersion>
   <artifactId>sys_ribbon</artifactId>
   <packaging>jar</packaging>
   <name>ribbon</name>
   <dependencies>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-starter-ribbon</artifactId>
       </dependency>
   </dependencies>
   ```

2. RibbonApplication 类
```java
@SpringBootApplication
//@EnableEurekaClient
@EnableDiscoveryClient//添加发现服务能力
public class RibbonApplication {
    @Bean
    @LoadBalanced//开启均衡负载
    RestTemplate restTemplate() {
        return new RestTemplate();
    }
    public static void main(String[] args) {
        SpringApplication.run(RibbonApplication.class, args);
    }
}
```

3. 创建Controller来消费COMPUTE-SERVICE的add服务
```java
@RestController
public class Controller {
    @Autowired
    RestTemplate restTemplate;
    @RequestMapping(value = "/add", method = RequestMethod.GET)
    public String add() {
        return restTemplate.getForEntity("http://compute-service/add?a=10&b=20", String.class).getBody();
    }
    @RequestMapping(value = "/hi", method = RequestMethod.GET)
    public String hi() {
        return restTemplate.getForEntity("http://compute-service/hi?a=testRibbon", String.class).getBody();
    }
}
```

4. application.properties中配置eureka服务注册中心
```properties
spring.application.name=ribbon-consumer
server.port=3333
# eureka.client.serviceUrl.defaultZone=http://localhost:1111/eureka/
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
eureka.instance.metadata-map.instanceId=${spring.application.name}:${server.port}
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
#eureka.client.fetchRegistry= true
#eureka.client.registry-fetch-interval-seconds=1
```

5. 启动(`mvn package&&java -jar target/jun-1.0-SNAPSHOT.jar`)应用  
    访问两次：`http://localhost:3333/add   http://localhost:3333/hi`

## 2.2 断路器 Netflix Hystrix  
调用故障或延迟，返回一个错误响应  
Hystrix具备拥有回退机制和断路器功能的线程和信号隔离，请求缓存和请求打包，以及监控和配置等功能。  

**Ribbon中引入Hystrix**  

0. 准备
启动`eureka-server`、`compute-service`、`eureka-ribbon`  
注册中心状态`http://localhost:1111/`  
访问`http://localhost:3333/add`  
关闭compute-service服务，访问`http://localhost:3333/add`  

1. pom.xml
```xml
    <!-- 断路器 hystrix
         Feigh工程不需要引入Hystix-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-hystrix</artifactId>
    </dependency>
```

2. RibbonApplication主类
```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableCircuitBreaker//开启断路器
public class RibbonApplication {
    @Bean
    @LoadBalanced
    RestTemplate restTemplate() {
        return new RestTemplate();
    }
    public static void main(String[] args) {
        SpringApplication.run(RibbonApplication.class, args);
    }
}
```

3. 改造原来的服务消费方式
```java
@RestController
public class Controller {
    @Autowired
    RestTemplate restTemplate;
    @RequestMapping(value = "/add", method = RequestMethod.GET)
    @HystrixCommand(fallbackMethod = "addFallback")
    //指定调用失败断路器调用的函数
    public String add() {
        return restTemplate.getForEntity("http://compute-service/add?a=10&b=20", String.class).getBody();
    }
    public String addFallback() {
        return "error";
    }
}
```

4. aplicarion.properties
```json
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds= 5000
hystrix.command.default.execution.timeout.enabled=false
```

5. 验证断路器的回调  
依次启动`eureka-server`、`compute-service`、`eureka-ribbon`工程  
访问`http://localhost:1111/`可以看到注册中心的状态  
访问`http://localhost:3333/add`，页面显示：30  
关闭compute-service服务后再访问`http://localhost:3333/add`，页面显示：error  

## 2.3  熔断监控Hystrix Dashboard

1. 父项目pom.xml
   ```xml
   <!-- Hystrix Dashboard (断路器：hystrix 仪表盘)
   @EnableHystrixDashboard   http://localhost:3333/hystrix
   -->
   <!--http://localhost:1111/health -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-hystrix-dashboard</artifactId>
   </dependency>
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-hystrix</artifactId>
   </dependency>
   ```

2. RibbonApplication主类添加注解
```java
@EnableHystrixDashboard
//断路器仪表盘  http://localhost:3333/hystrix
```

3. 访问
  1、 `http://localhost:3333/hystrix.stream`  
  2、 `http://localhost:1111/health`  
  3、 `http://localhost:3333/hystrix` 输入：`http://localhost:3333/hystrix.stream 、2000 、title`  
    另一个窗口 `http://localhost:3333/add`

# 3. Feign声明式的Web Service客户端
可插拔的注解支持，包括Feign注解和JAX-RS注解、Spring MVC注解。Feign也支持可插拔的编码器和解码器。整合了Ribbon和Eureka来提供均衡负载的HTTP客户端实现。  

## 3.1 web Service客户端

**创建基础Spring Boot工程**  
1. pom.xml：
   ```xml
   <parent>
       <artifactId>springCloud</artifactId>
       <groupId>com.jun</groupId>
       <version>1.0-SNAPSHOT</version>
   </parent>
   <modelVersion>4.0.0</modelVersion>
   <artifactId>sys_feign</artifactId>
   <packaging>jar</packaging>
   <name>feign</name>
   <dependencies>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-starter-feign</artifactId>
       </dependency>
   </dependencies>
   ```

2. FeignApplication.java 应用主类中：
```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients//开启Feign功能
public class FeignApplication {
    public static void main(String[] args) {
        SpringApplication.run(FeignApplication.class, args);
    }
}
```

3. 定义compute-service服务的接口：
```java
//绑定该接口对应compute-service服务
@FeignClient("compute-service")//绑定该接口对应服务
public interface Client {
    @RequestMapping(method = RequestMethod.GET, value = "/add")
    Integer add(@RequestParam(value = "a") Integer a, @RequestParam(value = "b") Integer b);
}
```

4. 在web层中调用上面定义的Client：
```java
@RestController
public class Controller {
    @Autowired
    Client client;
    @RequestMapping(value = "/add", method = RequestMethod.GET)
    public Integer add() {
        return client.add(10, 20);
    }
}
```

5. application.properties：
```properties
spring.application.name=feign
server.port=3344
#eureka.client.serviceUrl.defaultZone=http://localhost:1111/eureka/
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds= 5000
hystrix.command.default.execution.timeout.enabled=false
eureka.instance.metadata-map.instanceId=${spring.application.name}
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
#断路器 默认打开
#feign.hystrix.enabled=false
```

6. 启动应用，访问几次：`http://localhost:3344/add`  `http://localhost:3344/hi`

## 3.2 Feign使用Hystrix
1. 准备
依次启动`eureka-server`、`client-service`、`eureka-feign`工程  
注册中心的状态：`http://localhost:1111/`  
访问`http://localhost:3333/add`  
关闭compute-service服务，访问`http://localhost:3333/add`  

2. 创建回调类 ClientHystrix
```java
@Component
public class ClientHystrix implements Client {
    @Override
    public Integer add(@RequestParam(value = "a") Integer a, @RequestParam(value = "b") Integer b) {
        return -9999;
    }
    @Override
    public String hi(@RequestParam(value = "name") String name) {
        return "-9999";
    }
}
```

3. 指定回调类
```java
@FeignClient(value ="compute-service", fallback = ClientHystrix.class,configuration =="")
//绑定该接口对应compute-service服务
//@FeignClient("compute-service")//绑定该接口对应服务
//指定服务名，同时需要制定服务配置类
public interface Client {
    @RequestMapping(method = RequestMethod.GET, value = "/add")
//    @HystrixCommand(fallbackMethod="findByIdFallback")// 单个方法的fallback
    Integer add(@RequestParam(value = "a") Integer a, @RequestParam(value = "b") Integer b);
    @RequestMapping(method = RequestMethod.GET, value = "/hi")
    String hi(@RequestParam(value = "name") String name);
}
```

5. 验证一下
访问 `http://localhost:3344/hi`  `http://localhost:3344/add`
关闭client-service后再访问

## 3.3 熔断监控Hystrix Dashboard
1. 主类 FeignApplication 添加注解
```java
@EnableHystrixDashboard
@EnableCircuitBreaker
```

2. 验证
  1. `http://localhost:3344/hystrix.stream`  
  2. `http://localhost:1111/health`  
  3. `http://localhost:3344/hystrix` 输入：`http://localhost:3344/hystrix.stream 、2000 、title`  
    另一个窗口 `http://localhost:3344/add`

## 2.4  断路器聚合监控(Hystrix Turbine)
子模块 sys_turbine
1. pom.xml
   ```xml
   <modelVersion>4.0.0</modelVersion>
   <artifactId>sys_turbine</artifactId>
   <packaging>jar</packaging>
   <name>turbine</name>
   <dependencies>
       <!--断路器聚合监控-->
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-starter-turbine</artifactId>
       </dependency>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-netflix-turbine</artifactId>
       </dependency>
   </dependencies>
   ```

2. TurbineApplication.java
```java
@SpringBootApplication
@EnableTurbine
@EnableHystrixDashboard
public class TurbineApplication {
    public static void main(String[] args) {
        SpringApplication.run(TurbineApplication.class, args);
    }
}
```

3. application.properties
```properties
spring.application.name=turbine
#服务注册中心的端口
server.port=3355
#是否从eureka服务器获取注册信息
eureka.client.fetch-registry=false
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
#是否开启自我保护模式，默认为true
eureka.server.enable-self-preservation=true
eureka.instance.appname=turbine
#eureka.instance.hostname=localhost
#eureka.instance.metadata-map.instanceId=${spring.application.name}:${spring.application.instance_id:${random.value}}
#eureka.instance.instance-id=
#eureka.instance.prefer-ip-address=true
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
eureka.client.fetchRegistry= true
eureka.client.registry-fetch-interval-seconds=1
```

**3.1 application.properties 添加**
```
# 集群名称，默认为default  多个用逗号分隔
# 访问 http://localhost:3355/turbine.stream?cluster={MAIN}
turbine.aggregator.clusterConfig=MAIN
# 监控哪些服务:配置Eureka中的serviceId列表
turbine.appConfig=feign,ribbon-consumer
turbine.clusterNameExpression=metadata['cluster']
```
feign,ribbon-consumer的application.properties 添加
```properties
eureka.instance.metadata-map.cluster=MAIN
```
访问
  1. `http://localhost:3355/turbine.stream?cluster=MAIN`  
  2. `http://localhost:1111/health`  
  3. `http://localhost:3355/hystrix` 输入：`http://localhost:3355/turbine.stream?cluster=MAIN 、2000 、title`  
    另一个窗口 `http://localhost:3344/add`  
               `http://localhost:3333/add`

**3.1 application.properties 添加**
```
# 集群名称，默认为default  多个用逗号分隔
# 访问 http://localhost:3355/turbine.stream
turbine.aggregator.clusterConfig=default
# 监控哪些服务:配置Eureka中的serviceId列表
turbine.appConfig=feign,ribbon-consumer
turbine.clusterNameExpression=new String("default")
```
访问
  1. `http://localhost:3355/turbine.stream`  
  2. `http://localhost:1111/health`  
  3. `http://localhost:3355/hystrix` 输入：`http://localhost:3355/turbine.stream 、2000 、title`  
    另一个窗口 `http://localhost:3344/add`  
               `http://localhost:3333/add`
