---
layout: post
title:  "springCloud集成非java项目（koa2）"
date:   2018-01-09
desc: "springCloud集成非java项目（koa2）"
keywords: "后端,springCloud,微服务,koa2"
categories: [Back]
tags: [后端,springCloud,微服务,koa2]
icon: icon-java
---

>使用Sidecar将koa2引入Spring Cloud

# koa2

1. 初始化
```shell
mkdir koa2&&cd koa2&&npm init -y
npm install koa  koa-router superagent --save
touch app.js
```

2. app.js
```js
const Koa = require('koa')
const app = new Koa()
const Router = require('koa-router')
const router = new Router()
var  request = require('superagent');
const SERVICE = 'compute-service'
// 调取其他服务
  router.get('/hi',async  ctx => {
    var res=await request.get('http://localhost:8003/compute-service/hi?name=forezp').then(function(res){
        console.log(res.status,res.text);return res;})
    ctx.body=res.text;
  })
 //服务健康指标接口
  router.get('/health', ctx => {
      ctx.body ={    status: 'UP'}
  })
  var books=[{"id":1,"name":"book1"},{"id":2,"name":"book2"},{"id":3,"name":"book3"}]
// 提供服务
  router.get('/books/:id', ctx => {
      console.log(ctx.params.id);
      ctx.body =books;
  })
app .use(router.routes()).use(router.allowedMethods());
app.listen(8004)
console.log(`koa2 已启动 , 端口 : 8004`)
```


3. 启动： `node app.js`  
    访问 `http://localhost:8004/books/1`  
         `http://localhost:8004/hi`

# sys_koa2模块集成Sidecar

1. 依赖 pom.xml
    ```xml
    <artifactId>demo_koa2</artifactId>
    <packaging>jar</packaging>
    <name>koa2</name>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-netflix-sidecar</artifactId>
        </dependency>
    </dependencies>
    ```

2. 主类 SidecarApplication.java
```java
@SpringBootApplication
@EnableSidecar
public class SidecarApplication {
    public static void main(String[] args) {
        SpringApplication.run(SidecarApplication.class, args);
    }
}
```

3. 配置文件 bootstrap.properties
```properties
spring.application.name=koa2
server.port=8003
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
#eureka.instance.hostname=localhost
#eureka.instance.metadata-map.instanceId=${spring.application.name}:${spring.application.instance_id:${random.value}}
#eureka.instance.instance-id=
#eureka.instance.prefer-ip-address=true
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
eureka.client.fetchRegistry= true
eureka.client.registry-fetch-interval-seconds=1
# http://${server.port}/info 显示的内容
info.description= Spring Cloud +koa2
sidecar.port=8004
sidecar.home-page-uri= http://localhost:${sidecar.port}/
sidecar.health-uri= http://localhost:${sidecar.port}/health
hystrix.command.default.execution.timeout.enabled= false
```

4. 获取服务的相关信息 `http://localhost:8003/hosts/koa2` 

# sys_feign模块集成Sidecar

1. 新建KOAClient (调用第三方服务)
```java
@FeignClient(value = "koa2")
public interface KOAClient {
    @RequestMapping(method = RequestMethod.GET, value = "/books/{id}")
    public List<Object> findBooks(@RequestParam("id") String id);
}
```

2. 新建 KOAController
```java
@RestController
public class KOAController {
    @Autowired
    KOAClient client;
//    http://localhost:3344/findBooks
    @RequestMapping(value = "/findBooks", method = RequestMethod.GET)
    public List<Object> books() {
        return client.findBooks("10");
    }
}
```

3. 启动  
    访问：`http://localhost:3344/findBooks`



