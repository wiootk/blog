---
layout: post
title:  "springCloudZuul网关与追踪服务实现(sleuth+zipkin)"
date:   2018-01-06
desc: "springCloudZuul网关与追踪服务实现(sleuth+zipkin)"
keywords: "后端,springCloud,微服务,Zuul网关,追踪服务实现,sleuth,zipkin"
categories: [Back]
tags: [后端,springCloud,微服务,Zuul网关,追踪服务实现,sleuth,zipkin"]
icon: icon-java
---

# Zuul服务网关作用
1. 对外提供统一的REST API  
2. 服务访问提供权限控制  
3. 服务访问提供均衡负载  
准备工作
服务注册中心、ribbon、feign 、client `注意先启动测试`

# 统一的REST API

1. pom.xml
   ```xml
   <modelVersion>4.0.0</modelVersion>
   <artifactId>sys_zuul</artifactId>
   <packaging>jar</packaging>
   <name>zuul</name>
   <dependencies>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-starter-zuul</artifactId>
       </dependency>
   </dependencies>
   ```

2. 应用主类 ZuulApplication.java
```java
@EnableZuulProxy//开启Zuul
@SpringCloudApplication
//整合了@SpringBootApplication、@EnableDiscoveryClient、@EnableCircuitBreaker
public class ZuulApplication {
    public static void main(String[] args) {
        new SpringApplicationBuilder(ZuulApplication.class).web(true).run(args);
    }
}
```

3. 配置文件application.properties
```properties
spring.application.name=zuul
server.port=5555
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
#直接映射
zuul.routes.api-a-url.path=/api-a-url/**
zuul.routes.api-a-url.url=http://localhost:3333/
zuul.routes.api-b-url.path=/api-b-url/**
zuul.routes.api-b-url.url=http://localhost:3344/
#serviceId 映射
zuul.routes.api-a.path= /api-a/**
zuul.routes.api-a.serviceId= ribbon
zuul.routes.api-b.path= /api-b/**
zuul.routes.api-b.serviceId= feign
```

4. 测试：
`http://localhost:5555/api-a/add?a=1&b=2`  
`http://localhost:5555/api-b/add?a=1&b=2`  
`http://localhost:5555/api-a-url/add?a=1&b=2`  
`http://localhost:5555/api-b-url/add?a=1&b=2`  


# 服务过滤
自定义Zuul过滤器：检查请求中是否有Token参数，若有就进行路由，若没有就返回401错误
1. MyFilter.java
```java
@Component
public class MyFilter extends ZuulFilter {
    private static Logger log = LoggerFactory.getLogger(MyFilter.class);
    @Override
    public String filterType() {
        //    pre：路由之前    routing：路由之时    post： 路由之后    error：发送错误调用
        return "pre";
    }
    //    过滤的顺序
    @Override
    public int filterOrder() {
        return 0;
    }

    //    逻辑判断，是否要过滤，true,永远过滤
    @Override
    public boolean shouldFilter() {
//        RequestContext ctx = RequestContext.getCurrentContext();
//        return ctx.getRequest().getParameter("token") != null;
        return true;
    }
    //过滤器的具体逻辑
    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        log.info(String.format("%s >>> %s", request.getMethod(), request.getRequestURL().toString()));
        Object accessToken = request.getParameter("token");
        if (accessToken == null) {
            log.warn("token is empty");
            ctx.setSendZuulResponse(false);
            ctx.setResponseStatusCode(401);
            try {
//                ctx.getResponse().getWriter().write("token is empty");
                ctx.setResponseBody("token is empty!!!");
            } catch (Exception e) {
            }
            return null;
        }
        ctx.set("isSuccess", true);
        log.info("ok");
        return null;
    }
}
```

2. 启动该服务网关后，访问：  
`http://localhost:5555/api-a/add?a=1&b=2`  
`http://localhost:5555/api-a/add?a=1&b=2&token=token`  

3. 跨域处理
在主类添加
```java
@Bean
public CorsFilter corsFilter() {
    final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    final CorsConfiguration config = new CorsConfiguration();
    config.setAllowCredentials(true); // 允许cookies跨域
    config.addAllowedOrigin("*");// #允许向该服务器提交请求的URI，*表示全部允许，在SpringMVC中，如果设成*，会自动转成当前请求头中的Origin
    config.addAllowedHeader("*");// #允许访问的头信息,*表示全部
    config.setMaxAge(18000L);// 预检请求的缓存时间（秒），即在这个时间段里，对于相同的跨域请求不会再预检了
    config.addAllowedMethod("OPTIONS");// 允许提交请求的方法，*表示全部允许
    config.addAllowedMethod("HEAD");
    config.addAllowedMethod("GET");// 允许Get的请求方法
    config.addAllowedMethod("PUT");
    config.addAllowedMethod("POST");
    config.addAllowedMethod("DELETE");
    config.addAllowedMethod("PATCH");
    source.registerCorsConfiguration("/**", config);
    return new CorsFilter(source);
}
```



<!-- 开启zuul的重试机制
在pom中添加spring-retry的依赖(maven工程)
设置zuul.retryable=true(该参数默认为false)
具体properties文件内容如下
#是否开启重试功能
zuul.retryable=true
#同一个Server重试的次数(除去首次)
ribbon.MaxAutoRetries=3
#切换相同Server的次数
ribbon.MaxAutoRetriesNextServer=0


Spring Cloud Hystrix的请求合并 -->

# Zuul统一异常处理
1. 方案1
```java
@Component
public class ErrorFilter extends ZuulFilter {
    Logger log = LoggerFactory.getLogger(ErrorFilter.class);
    @Override
    public String filterType() {
        return "error";
    }
    @Override
    public int filterOrder() {
        return 10;
    }
    @Override
    public boolean shouldFilter() {
        return true;
    }
    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        Throwable throwable = ctx.getThrowable();
        log.error("this is a ErrorFilter : {}", throwable.getCause().getMessage());
        ctx.set("error.status_code", HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        ctx.set("error.exception", throwable.getCause());
        return null;
    }
}
```
2. 方案2
```java
@Component
public class ThrowExceptionFilter extends ZuulFilter {
    private static Logger log = LoggerFactory.getLogger(ThrowExceptionFilter.class);
    @Override
    public String filterType() {
        return "pre";
    }
    @Override
    public int filterOrder() {
        return 0;
    }
    @Override
    public boolean shouldFilter() {
        return true;
    }
    @Override
    public Object run() {
        log.info("This is a pre filter, it will throw a RuntimeException");
        RequestContext ctx = RequestContext.getCurrentContext();
        try {
            doSomething();
        } catch (Exception e) {
            ctx.set("error.status_code", HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            ctx.set("error.exception", e);
        }
        return null;
    }
    private void doSomething() {
        throw new RuntimeException("Exist some errors...");
    }
}
```

# spring-cloud-sleuth+zipkin追踪服务实现

1. 父项目pom.xml
   ```xml
   <!--服务追踪-->
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-zipkin</artifactId>
   </dependency>
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-sleuth</artifactId>
   </dependency>
   ```
        
2. 服务注册模块eureka配置文件
```properties
#禁用追踪
spring.zipkin.enabled=false
```

1. pom.xml
   ```xml
   <artifactId>sys_zipkin</artifactId>
   <packaging>jar</packaging>
   <name>zipkin</name>
   <dependencies>
       <!--使用@EnableZipkinServer注解方式只需要依赖如下两个包-->
       <dependency>
           <groupId>io.zipkin.java</groupId>
           <artifactId>zipkin-server</artifactId>
       </dependency>
       <dependency>
           <groupId>io.zipkin.java</groupId>
           <artifactId>zipkin-autoconfigure-ui</artifactId>
           <scope>runtime</scope>
       </dependency>
       <!--保存到数据库需要如下依赖-->
       <dependency>
           <groupId>io.zipkin.java</groupId>
           <artifactId>zipkin-autoconfigure-storage-mysql</artifactId>
       </dependency>
       <dependency>
           <groupId>mysql</groupId>
           <artifactId>mysql-connector-java</artifactId>
       </dependency>
       <dependency>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-jdbc</artifactId>
       </dependency>      
   </dependencies>
   ```

2. ZipkinApplication.java
```java
@SpringBootApplication
@EnableZipkinServer
@EnableEurekaClient
public class ZipkinApplication {
    public static void main(String[] args) {
        SpringApplication.run(ZipkinApplication.class, args);
    }
    @Bean
    @ConditionalOnMissingBean
    public SpanAdjuster defaultSpanAdjuster() {
        return new NoOpSpanAdjuster();
    }
}
```

3. application.properties
```properties
spring.application.name=zipkin
server.port=8899
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
eureka.instance.metadata-map.instanceId=${spring.application.name}
# 发呆时间，即服务续约到期时间（缺省为90s）
eureka.instance.lease-expiration-duration-in-seconds=1
#eureka client发送心跳给server端的频率,默认30秒
eureka.instance.lease-renewal-interval-in-seconds=1
#eureka client 闲置多久关闭连接
eureka.client.eureka-connection-idle-timeout-seconds = 1
#表示eureka client间隔多久去拉取服务注册信息，默认为30秒
eureka.client.registry-fetch-interval-seconds=60
# 开启健康检查（依赖spring-boot-starter-actuator）
eureka.client.healthcheck.enabled=true
#断路器 默认打开
#feign.hystrix.enabled=false
#logging.level.org.springframework.cloud=DEBUG
spring.sleuth.enabled=false
#zipkin.storage.type= mem
#加快采样
spring.sleuth.sampler.percentage=1
#表示zipkin数据存储方式是mysql
zipkin.storage.type=mysql
#数据库脚本创建地址，当有多个是可使用[x]表示集合第几个元素
spring.datasource.schema[0]=classpath:/zipkin.sql
#spring boot数据源配置
spring.datasource.url=jdbc:mysql://localhost:3306/demo3?autoReconnect=true&useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&useSSL=false
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.initialize=true
spring.datasource.continue-on-error=true
```

4. 需要追踪的服务配置文件
```properties
  spring.zipkin.base-url=http://localhost:8899
```

5. 测试
启动模块eureka、ribbon、feign、client、zipkin并访问相关服务
访问：`http://localhost:8899` 查看服务访问的链路信息

## 添加logback
1. pom.xml
   ```xml
   <dependency>
       <groupId>net.logstash.logback</groupId>
       <artifactId>logstash-logback-encoder</artifactId>
       <version>4.9</version>
   </dependency>
   <dependency>
       <groupId>ch.qos.logback</groupId>
       <artifactId>logback-core</artifactId>
       <version>1.2.3</version>
   </dependency>
   ```

2. logback-spring.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- scan 是否定期扫描xml文件， scanPeriod是说扫描周期是30秒-->
<configuration scan="true" scanPeriod="30 seconds" debug="false" packagingData="true">
    <!-- 项目名称 -->
    <contextName>myApp1 contextName</contextName>
    <!-- 属性 -->
    <property name="USER_HOME" value="./log"/>

    <timestamp key="bySecond" datePattern="yyyyMMdd" timeReference="contextBirth"/>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    ​
    <springProperty scope="context" name="springAppName" source="spring.application.name"/>
    <!-- Example for logging into the build folder of your project -->
    <property name="LOG_FILE" value="${BUILD_FOLDER:-build}/${springAppName}"/>​

    <property name="CONSOLE_LOG_PATTERN"
              value="%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(${LOG_LEVEL_PATTERN:-%5p}) %clr([${springAppName:-},%X{X-B3-TraceId:-},%X{X-B3-SpanId:-},%X{X-Span-Export:-}]){yellow} %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}"/>

    <!-- appender很重要，一个配置文件会有多个appender -->
    <!-- ConsoleApperder意思是从console中打印出来 -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <!-- 过滤器，一个appender可以有多个 -->
        <!-- 阈值过滤，就是log行为级别过滤，debug及debug以上的信息会被打印出来 -->
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>WARN</level>
        </filter>
        <!-- encoders are assigned the type
             ch.qos.logback.classic.encoder.PatternLayoutEncoder by default -->
        <!-- encoder编码规则 -->
        <encoder>
            <!--<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>-->
            <!--<pattern>%d %contextName %msg%n</pattern>-->
            <!-- pattern模式 %d时间 %thread 线程名 %level行为级别 %logger logger名称 %method 方法名称 %message 调用方法的入参消息  ${CONSOLE_LOG_PATTERN}-->
            <pattern>%-4d [%thread] %highlight%-5level %cyan%logger.%-10method - %message%n</pattern>
            <charset>utf8</charset>
        </encoder>
    </appender>
    <!-- 滚动日志文件，这个比较常用 -->
    <appender name="ROLLINGFILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 当project等于true的时候file就不会起效果-->
        <prudent>true</prudent>
        <file>${LOG_FILE}</file>
        <!--<file>${USER_HOME}/logFile.log</file>-->
        <!-- 按天新建log日志 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- daily rollover -->
            <fileNamePattern>${USER_HOME}/logFile.%d{yyyy-MM-dd}_%i.log</fileNamePattern>
            <!-- 保留30天的历史日志 -->
            <maxHistory>30</maxHistory>

            <!-- 基于大小和时间，这个可以有，可以没有 -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <!-- or whenever the file size reaches 100MB -->
                <!-- 当一个日志大小大于10KB，则换一个新的日志。日志名的%i从0开始，自动递增 -->
                <maxFileSize>10KB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <encoder>
            <!-- %ex就是指抛出的异常，full是显示全部，如果在{}中写入数字，则表示展示多少行 -->
            <pattern>%-4date [%thread] %-5level %logger{35} - %msg%n%ex{full, DISPLAY_EX_EVAL}</pattern>
            <charset>utf8</charset>
        </encoder>
    </appender>

    <!-- FileAppender 输出到文件 -->
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <!-- 文件存放位置 %{xxx} 就是之前定义的属性xxx -->
        <file>${USER_HOME}/myApp1log-${bySecond}.log</file>
        <encoder>
            <!-- %date和%d是一个意思 %file是所在文件 %line是所在行 -->
            <pattern>%date %level [%thread] %logger{30} [%file:%line] %msg%n</pattern>
        </encoder>
    </appender>
    <!-- 输出到HTML格式的文件 -->
    <appender name="HTMLFILE" class="ch.qos.logback.core.FileAppender">
        <!-- 过滤器，这个过滤器是行为过滤器，直接过滤掉了除debug外所有的行为信息 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>debug</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
        <encoder class="ch.qos.logback.core.encoder.LayoutWrappingEncoder">
            <!-- HTML输出格式 可以和上边差不多 -->
            <layout class="ch.qos.logback.classic.html.HTMLLayout">
                <pattern>%relative%thread%mdc%level%logger%msg</pattern>
            </layout>
        </encoder>
        <file>${USER_HOME}/test.html</file>
    </appender>    ​
    <!-- Appender to log to file in a JSON format -->
    <appender name="logstash" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_FILE}.json</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_FILE}.json.%d{yyyy-MM-dd}.gz</fileNamePattern>
            <maxHistory>7</maxHistory>
        </rollingPolicy>
        <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
            <providers>
                <timestamp>
                    <timeZone>UTC</timeZone>
                </timestamp>
                <pattern>
                    <pattern>
                        {
                        "severity": "%level",
                        "service": "${springAppName:-}",
                        "trace": "%X{X-B3-TraceId:-}",
                        "span": "%X{X-B3-SpanId:-}",
                        "exportable": "%X{X-Span-Export:-}",
                        "pid": "${PID:-}",
                        "thread": "%thread",
                        "class": "%logger{40}",
                        "rest": "%message"
                        }
                    </pattern>
                </pattern>
            </providers>
        </encoder>
    </appender>

    <!-- 重点来了，上边都是appender输出源。这里开始就是looger了 -->
    <!-- name意思是这个logger管的哪一片，像下面这个管的就是log/test包下的所有文件 level是只展示什么行为信息级别以上的，类似阈值过滤器 additivity表示是否再抛出事件，就是说如果有一个logger的name是log，如果这个属性是true，另一个logger就会在这个logger处理完后接着继续处理 -->
    <logger name="log.test" level="INFO" additivity="false">
        <!-- 连接输出源，也就是上边那几个输出源 ，你可以随便选几个appender-->
        <appender-ref ref="STDOUT"/>
        <appender-ref ref="ROLLINGFILE"/>
        <appender-ref ref="HTMLFILE"/>
    </logger>
    <!-- 这个logger详细到了类 -->
    <logger name="log.test.Foo" level="debug" additivity="false">
        <appender-ref ref="STDOUT"/>
        <appender-ref ref="ROLLINGFILE"/>
        <appender-ref ref="HTMLFILE"/>
    </logger>
    <!-- Strictly speaking, the level attribute is not necessary since -->
    <!-- the level of the root level is set to DEBUG by default.       -->
    <!-- 这就是上边logger没有管到的情况下 root默认接管所有logger -->
    <root level="debug">
        <appender-ref ref="STDOUT"/>
        <!--<appender-ref ref="console"/>-->
        <appender-ref ref="logstash"/>
        <!--<appender-ref ref="flatfile"/>-->
    </root>
</configuration>
```








