---
layout: post
title:  "SpringMVC+SpringDataJPA+Hibernate搭建教程"
date:   2017-12-09
desc: "SpringMVC+SpringDataJPA+Hibernate搭建教程"
keywords: "后端,SpringDataJPA"
categories: [Back]
tags: [后端,SpringDataJPA]
icon: icon-java
---
# 一、新建maven工程
  在IDEA 新建maven工程：maven-archetype-webapp

**1. 构建maven项目结构**
```
- src
    * main
        *  java
        *  resources
        *  webapp
            - WEB-INF
            - index.jsp
    * test
        *  java
        *  resources
```
**2. File->Project Struct...->modeues->更改新建包类别**

**3. WEB-INF/web.xml**
``` xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">     
    <display-name>SpringDataJPA</display-name>     
    <welcome-file-list>          
        <welcome-file>index.html</welcome-file>         
    </welcome-file-list>
</web-app>
```

**4. index.jsp**
```html
<html>
  <body>
      <h2>Hello World!</h2>
   </body>
</html>
```

**5. 配置tomcat 启动项目**

# 二、集成Spring+SpringMVC 
## （1）添加依赖及配置文件
**1. 修改pom.xml添加jar包：**
``` xml
<properties>
    <!-- spring版本号 -->
    <spring.version>4.2.5.RELEASE</spring.version>
</properties>
<dependencies>
    <!-- spring核心包 -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-orm</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-tx</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jdbc</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aop</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context-support</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-test</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-orm</artifactId>
        <version>${spring.version}</version>
    </dependency>
    <dependency>
        <groupId>org.springframework.data</groupId>
        <artifactId>spring-data-jpa</artifactId>
        <version>1.10.1.RELEASE</version>
    </dependency>
    <dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.12</version>
    </dependency>
</dependencies> 
```

**2. 添加Spring配置文件：WEB--INF/applicationContext.xml：**
``` xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop" xmlns:p="http://www.springframework.org/schema/p"
       xmlns:tx="http://www.springframework.org/schema/tx" xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.2.xsd
       http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context-4.2.xsd
       http://www.springframework.org/schema/tx
       ttp://www.springframework.org/schema/tx/spring-tx-4.2.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-4.2.xsd
       http://www.springframework.org/schema/mvc
       http://www.springframework.org/schema/mvc/spring-mvc-4.2.xsd">
    <!-- 开启IOC注解扫描 -->
    <context:component-scan base-package="com.jun"/>
    <!-- 开启MVC注解扫描 -->
    <mvc:annotation-driven/>
</beans>
```

**3. 修改web.xml，将spring添加进去：**
``` xml
<display-name>SpringDataJPA</display-name>
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<context-param>
    <param-name>contextConfigLocation</param-name>
    <!--<param-value>WEB-INF/applicationContext.xml</param-value>-->
    <param-value>classpath*:applicationContext.xml</param-value>
</context-param>
<servlet>
    <servlet-name>springmvc</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath*:springmvc-servlet.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>springmvc</servlet-name>
    <url-pattern>/*</url-pattern>
</servlet-mapping>
<welcome-file-list>
    <welcome-file>index.html</welcome-file>
</welcome-file-list>
```

**4. 创建 springMVC 配置文件 resources/springmvc-servlet.xml**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.2.xsd">
</beans>
```

## （2）编写代码(注意注解)  

**1. 实体com.jun.entity.User.java：**
```java
public class User {
    private Integer id;
    private String name;
    public User(Integer id, String name) {
        this.id = id;
        this.name = name;
    }
    @Override
    public String toString() {
        return "id:"+id+",name:"+name;
    }
Set/get...
}
```

**2. dao层接口com.jun.dao.UserDao.java：**
``` java
public interface UserDao {
    User getUser(Integer id, String name);
}
```

**3. dao层实现com.jun.dao.impl.UserDaoImpl.java：**
``` java
@Repository
public class UserDaoImpl implements UserDao {
    public User getUser(Integer id, String name) {
        return new User(id, name);
    }
}
```

**4. service层接口com.jun.service.UserService.java:**
``` java
public interface UserService {
    User getUser(Integer id, String name);
}
```

**5. service层实现 com.jun.service.impl.UserServiceImpl.java：**
``` java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserDao userDao;
    public User getUser(Integer id, String name) {
        return userDao.getUser(id, name);
    }
}
```

**6. controller层com.jun.controller.DemoController.java：**
``` java
@Controller
@RequestMapping("/")
public class DemoController {
    @Autowired
    UserService userService;
    @RequestMapping("/")
    @ResponseBody
    public String index(){
        return "index";
    }
    @RequestMapping("/getuser")
    @ResponseBody
    public String getUser(Integer id, String name){
        return userService.getUser(id, name).toString();
    }
}
```
 ~~配置jar包一同发布：File->project structure->artifacts~~  
**7. 启动项目运行：`localhost:8080`  `localhost:8080/getuser?id=1&name=demo`**  
## (3)添加返回Json格式数据支持 
**1. pom.xml添加jar包：**
``` xml
   <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.5.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-core</artifactId>
      <version>2.5.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.5.0</version>
    </dependency>
    <dependency>
      <groupId>com.alibaba</groupId>
      <artifactId>fastjson</artifactId>
      <version>RELEASE</version>
    </dependency>
```

**2. DemoController添加getUser()方法：**
```java
@RequestMapping("/getuserJson")
@ResponseBody
public Map<String, Object> getUserJson(Integer id, String name){
    Map<String, Object> map = new HashMap<String, Object>();
    map.put("state", "success");
    map.put("data", userService.getUser(id, name));
    return map;
}
```

**3. applicationContext.xml 添加json 解析支持**
``` xml
<!--避免IE执行AJAX时，返回JSON出现下载文件 -->
<bean id="mappingJacksonHttpMessageConverter"
      class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
    <property name="supportedMediaTypes">
        <list>
            <value>text/html;charset=UTF-8</value>
        </list>
    </property>
</bean>
<!-- 启动SpringMVC的注解功能，完成请求和注解POJO的映射 -->
<bean class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter ">
    <property name="messageConverters">
        <list>
            <ref bean="mappingJacksonHttpMessageConverter"/>    <!-- JSON转换器 -->
        </list>
    </property>
</bean>
```

**重新运行后访问：`http://localhost:8080/getuserJson?id=1&name=demo`**

## （4）配置静态资源访问

*通常WEB-INF目录下的资源，无法直接访问*
 *在WEB-INF之外新建img目录,拷贝图片进去`meinv.jpg`*

``` xml
<!-- 对静态资源文件访问，将无法mapping到Controller的path交给default servlet handler处理-->
<mvc:default-servlet-handler /> 
<!--两者写一个就行 -->
<mvc:resources mapping="/img/**" location="/img/">
    <mvc:cache-control max-age="3600" cache-public="true"/>
</mvc:resources>
```

**重启项目访问 `localhost:8080/img/meinv.jpg`**

## （5）乱码解决
**post提交请求乱码处理，在web.xml添加一个编码过滤器解决：**
``` xml
    <filter>
        <filter-name>CharacterEncoding</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <init-param>
            <param-name>forceEncoding</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>CharacterEncoding</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
```
**get（含浏览器地址栏直接提交方式）乱码处理**，修改`tomcat/conf/server.xml`：
``` xml
<Connector connectionTimeout="20000" port="8080" protocol="HTTP/1.1" redirectPort="8443" URIEncoding="UTF-8"/>
```

# 三、整合JPA+Hibernate
**1. jar包：SpringDataJPA、Hibernate(和mysql驱动)的jar包**
``` xml
<!-- hibernate -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>${hibernate.version}</version>
</dependency>
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-ehcache</artifactId>
    <version>${hibernate.version}</version>
</dependency>
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-entitymanager</artifactId>
    <version>${hibernate.version}</version>
</dependency>
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-c3p0</artifactId>
    <version>${hibernate.version}</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.9</version>
</dependency>
```
**统一管理的版本为：**
```xml
<!-- hibernate 版本号 -->
<hibernate.version>5.1.0.Final</hibernate.version>
```
**2. 添加jdbc的配置文件resources/jdbc.properties：**
```xml
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://127.0.0.1:3306/demo?createDatabaseIfNotExist=true&&useUnicode=true&amp;characterEncoding=UTF-8
jdbc.username=root
jdbc.password=
hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect
```

**3. Spring配置文件applicationContext.xml中增加JPA支持后的完整内容：**
``` xml
    <!-- 开启IOC注解扫描 -->
    <context:component-scan base-package="com.jun">
        <!-- 排除@controller由springmvc扫描-->
        <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
    </context:component-scan>
    <!-- 数据库连接 -->
    <context:property-placeholder location="classpath:jdbc.properties" ignore-unresolvable="true"/>
    <!-- 数据源 -->
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
    <!-- JPA实体管理器工厂 -->
    <bean id="entityManagerFactory"
          class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
        <property name="dataSource" ref="dataSource"/>
        <property name="jpaVendorAdapter" ref="hibernateVendor"/>
        <property name="packagesToScan" value="com.jun.entity"/>
        <property name="jpaProperties">
            <props>
                <prop key="hibernate.current_session_context_class">thread</prop>
                <prop key="hibernate.hbm2ddl.auto">create</prop><!-- validate/update/create -->
                <prop key="hibernate.show_sql">false</prop>
                <prop key="hibernate.format_sql">false</prop>
                <!-- 建表的命名规则 -->
                <prop key="hibernate.ejb.naming_strategy">org.hibernate.cfg.ImprovedNamingStrategy</prop>                
                <!-- 定义延迟加载-->
                <prop key="hibernate.enable_lazy_load_no_trans">false</prop>  
                <!-- 不检查设置默认值 可能是JDK版本或者数据库驱动版本的问题，设置为true会报错 -->  
                <prop key="hibernate.temp.use_jdbc_metadata_defaults">false</prop>  
                <!-- 缓存配置 -->  
                <prop key="cache.use_second_level_cache">true</prop><!-- 启用二级缓存 -->    
                <prop key="hibernate.cache.use_query_cache">true</prop><!-- 启用查询缓存 -->   
                <prop key="hibernate.cache.region.factory_class">org.hibernate.cache.ehcache.EhCacheRegionFactory</prop>
            </props>
        </property>
    </bean>
    <bean id="hibernateVendor" class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter">
        <property name="databasePlatform" value="${hibernate.dialect}"/>
        <property name="generateDdl" value="true"/>
        <property name="database" value="MYSQL"/>
    </bean>
    <!-- 设置JPA实现厂商的特定属性 -->
    <bean id="hibernateJpaVendorAdapter" class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter"/>
    <!-- Jpa 事务配置 -->
    <bean id="transactionManager" class="org.springframework.orm.jpa.JpaTransactionManager">
        <property name="entityManagerFactory" ref="entityManagerFactory"/>
    </bean>
    <!-- Spring Data Jpa配置 -->
    <jpa:repositories base-package="com.jun.dao" transaction-manager-ref="transactionManager"
                      entity-manager-factory-ref="entityManagerFactory"/>
    <!-- 使用annotation定义事务 -->
    <tx:annotation-driven transaction-manager="transactionManager" proxy-target-class="true"/>


<!--    &lt;!&ndash; 事务 &ndash;&gt;
    <tx:advice id="txAdvice" transaction-manager="transactionManager">
        <tx:attributes>
            <tx:method name="*" />
            <tx:method name="get*" read-only="true" />
            <tx:method name="find*" read-only="true" />
            <tx:method name="select*" read-only="true" />
            <tx:method name="delete*" propagation="REQUIRED" />
            <tx:method name="update*" propagation="REQUIRED" />
            <tx:method name="add*" propagation="REQUIRED" />
            <tx:method name="insert*" propagation="REQUIRED" />
        </tx:attributes>
    </tx:advice>
    &lt;!&ndash; 事务入口 &ndash;&gt;
    <aop:config>
        <aop:pointcut id="allServiceMethod" expression="execution(* your service implements package.*.*(..))" />
        <aop:advisor pointcut-ref="allServiceMethod" advice-ref="txAdvice" />
    </aop:config>-->
```

**4. springMVC 配置文件 springMVC-servlet.xml**
``` xml
<!-- 开启MVC注解扫描 -->
    <mvc:annotation-driven/>
    <!-- SpringMVC的扫描范围 -->
    <context:component-scan base-package="com.jun.controller" use-default-filters="false">
        <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        <context:include-filter type="annotation" expression="org.springframework.web.bind.annotation.ControllerAdvice"/>
    </context:component-scan>
    <!-- 默认访问跳转到登录页面，即定义无Controller的path<->view直接映射
<mvc:view-controller path="/" view-name="redirect:/login"/>
-->
    <!-- 用于返回json格式 -->
    <!--    <bean id="mappingJacksonHttpMessageConverter"
              class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
            <property name="supportedMediaTypes">
                <list>
                    <value>text/html;charset=UTF-8</value>
                    <value>application/x-www-form-urlencoded;charset=UTF-8</value>
                </list>
            </property>
        </bean>
        &lt;!&ndash; 启动SpringMVC的注解功能，完成请求和注解POJO的映射 &ndash;&gt;
        <bean class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter ">
            <property name="messageConverters">
                <list>
                    <ref bean="mappingJacksonHttpMessageConverter"/>    &lt;!&ndash; JSON转换器 &ndash;&gt;
                </list>
            </property>
        </bean>-->
    <!-- 配置SpringMVC的视图解析器 -->
    <!-- 其viewClass属性的默认值就是org.springframework.web.servlet.view.JstlView -->
    <bean id="internalResourceViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <!-- <property name="viewClass" value="org.springframework.web.servlet.view.JstlView" /> -->
        <property name="prefix" value="/" />
        <property name="suffix" value=".html" />
    </bean>
    <bean class="org.springframework.web.servlet.view.ContentNegotiatingViewResolver">
        <property name="viewResolvers">
            <list>
                <ref bean="internalResourceViewResolver"/>
            </list>
        </property>
        <!-- 将对象转换为JSON -->
        <property name="defaultViews">
            <list>
                <bean class="org.springframework.web.servlet.view.json.MappingJackson2JsonView" />
            </list>
        </property>
    </bean>
    <!-- 对静态资源文件的访问，将无法mapping到ontroller的path交给default servlet handler处理 -->
    <mvc:resources location="/img/" mapping="/img/**">
        <mvc:cache-control max-age="3600" cache-public="true"/>
    </mvc:resources>
    <mvc:default-servlet-handler />
    <!-- 总错误处理--><!--     <bean id="exceptionResolver" class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">
        <property name="defaultErrorView">
            <value>/base/error</value>
        </property>
        <property name="defaultStatusCode">
            <value>500</value>
        </property>
        <property name="warnLogCategory">
            <value>org.springframework.web.servlet.handler.SimpleMappingExceptionResolver</value>
        </property>
    </bean> -->
```

*启动报错：*
>新建WEB-INF/classes/logging.properties 打印具体错误信息

```
handlers = org.apache.juli.FileHandler, java.util.logging.ConsoleHandler  
  
############################################################  
# Handler specific properties.  
# Describes specific configuration info for Handlers.  
############################################################  
  
org.apache.juli.FileHandler.level = FINE  
org.apache.juli.FileHandler.directory = ${catalina.base}/logs  
org.apache.juli.FileHandler.prefix = error-debug.  
  
java.util.logging.ConsoleHandler.level = FINE  
java.util.logging.ConsoleHandler.formatter = java.util.logging.SimpleFormatter
```
错误：例：通配符的匹配很全面, 但无法找到元素 XXX:tx 
删掉并重新引入
>xmlns:tx="...
xsi:schemaLocation 相关行

**4. 修改实体：**
```java
@Entity
@Table
public class User2 {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private String name;
    public User2() {
    }
    public User2(String name) {
        this.name = name;
    }
    @Override
    public String toString() {
        return "id:"+id+",name:"+name;
    }
    // get/set ...
}
```

**5. 将dao层接口继承自强大的JpaRepository,可以删掉dao层实现了：**
>Repository：标识，继承它的均为仓库接口类  
CrudRepository：继承Repository，实现一组CRUD相关方法  
PagingAndSortingRepository：继承CrudRepository，实现了一组分页排序相关的方法  
JpaRepository：继承PagingAndSortingRepository，实现一组JPA规范相关的方法  
JpaSpecificationExecutor：比较特殊，不属于Repository体系，实现一组JPA Criteria查询相关的方法。

``` java
@Repository
public interface User2Dao extends JpaRepository<User2, Serializable> {
    User2 findById(Integer id);
}
```
**6. 修改service层接口：**
``` java
public interface User2Service {
    User2 findById(Integer id);
    User2 save(String name);
    List<User2> findAll();
}
```
**7. 修改service层实现：**
``` java
@Service
public class User2ServiceImpl implements User2Service {
    @Autowired
    private User2Dao userDao;    
    public User2 findById(Integer id) {
        return userDao.findById(id);
    }    
    public User2 save(String name) {
        return userDao.save(new User2(name));
    }    
    public List<User2> findAll() {
        return userDao.findAll();
    }
    public User2 getUser(Integer id, String name) {
        return null;
    }
}
```
**8. 修改controller:**
```java
@Controller
@RequestMapping("/demo2")
public class Demo2Controller {
    @Autowired
    User2Service userService;
    @RequestMapping("/")
    @ResponseBody
    public String index(){
        return "index";
    }
    @RequestMapping("/info")
    public String info(){
        return "info";
    }
    @RequestMapping("/findall")
    @ResponseBody
    public Map<String, Object> getUser(){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data", userService.findAll());
        return map;
    }
    @RequestMapping("/findById")
    @ResponseBody
    public Map<String, Object> findById(Integer id){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data", userService.findById(id));
        return map;
    }
    @RequestMapping("/add")
    @ResponseBody
    public Map<String, Object> save(String name){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data", userService.save(name));
        return map;
    }
}
```

**9. 启动tomcat 访问 `localhost:8080/demo2/add?name=名字` `localhost:8080/demo2/findById?id=1` `localhost:8080/demo2/findall`**

**10. 需要添加一个查找id大于指定值的指定姓氏的数据**  
*SQL语句是：`SELECT * FROM user WHERE id>? AND name like '?%';`*  
*直接在dao层接口添加一个方法即可*  
>List<User> findByIdGreaterThanAndNameLike(Integer id,String name);  

>注意：service实现的使用，调用该方法记得name+"%")  

>controller层使用@RestController(等同于@Controller + @ResponseBody)  

# 四、常用方法示例
```java
interface TaskDao extends MyRepo<Task, Long> {
    List<Task> findByNameAndId(String name,Long id);
    List<Task> findByNameOrId(String name,Long id);
    Page<Task> findByName(String name,Pageable pageable);
    Slice<Task> findByName(String name, Pageable pageable);
    List<Task> findByName(String name, Sort sort);
    List<Person> findDistinctTaskByNameOrid(String name, Long id);
    List<Person> findByNameOrderByIdDesc(String name, Long id);
    Page<Task> queryFirst10ByNameOrderByLastnameAsc(String name, Pageable pageable);
    Slice<Task> findTop3ByNameOrderByNameDesc(String name, Pageable pageable);
    List<Task> findFirst10ByName(String name, Sort sort);
    List<Task> findTop10ByName(String name, Pageable pageable);
    List<String> findIdByPlanId(List<String> planId);   
    Page<Task>  findDistinctByIdOrderByCreateTime(List<String> ids);      
    List<String> findPlanId(Specification<Task> spec);
}
```
保存实体的方法
 >1）保存一个实体：repository.save(T entity)  

 >2）保存多个实体：repository.save(Iterable<T> entities)  

 >3）保存并立即刷新：repository.saveAndFlush(T entity)  
