---
layout: post 
title:  "SpringBoot+SpringDataJpa+SpringSecurity+thymeleaf项目搭建"
date:   2017-12-17
desc: "SpringBoot+SpringDataJpa+SpringSecurity+thymeleaf 项目搭建"
keywords: "后端,springBoot,搭建"
categories: [Back]
tags: [后端,springBoot,搭建]
icon: icon-java
---
**简介：**  
SpringBoot旨在简化新Spring应用的初始搭建以及开发过程,可以快速创建一个基于Spring的项目，它是一些库的集合，可以jar包形式独立运行，内嵌tomcat，简化maven配置，自动配置Spring ，采用约定简化（或不用）xml配置  

# 初始化项目搭建
新建 maven 项目-创建子模块：`biz（业务逻辑）、data（数据库操作 entity,repo）、design(接口及pojo)、release(项目发布)`  
父项目的pom.xml
```xml
      <packaging>pom</packaging>
    <name>springBoot</name>
    <description>Demo for Spring Boot</description>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.2.RELEASE</version>
        <relativePath/>
    </parent>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>javax</groupId>
            <artifactId>javaee-api</artifactId>
            <version>7.0</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.5</version>
        </dependency>
        <!-- SpringSecurity依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```
release的pom.xml
```xml
    <parent>
        <artifactId>wioo</artifactId>
        <groupId>tk.wioo</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>
    <artifactId>release</artifactId>
    <packaging>jar</packaging>
    <name>release</name>
    <dependencies>
        <dependency>
            <groupId>${project.groupId}</groupId>
            <artifactId>design</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId>${project.groupId}</groupId>
            <artifactId>biz</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
```
design的pom.xml
```xml
    <packaging>jar</packaging>
    <name>design</name>
```
data的pom.xml
```xml
   <packaging>jar</packaging>
    <name>data</name>
```
biz 的pom.xml
```xml
    <parent>
        <artifactId>wioo</artifactId>
        <groupId>tk.wioo</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>
    <artifactId>biz</artifactId>
    <packaging>jar</packaging>
    <name>biz</name>
    <dependencies>
        <dependency>
            <groupId>${project.groupId}</groupId>
            <artifactId>data</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId>${project.groupId}</groupId>
            <artifactId>design</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
```

# 集成 SpringDataJpa

1. release 模块
应用主类 tk.wioo.Application.java
```java
@SpringBootApplication
@ComponentScan(basePackages = { "tk.wioo","tk.wioo.biz" })
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```
配置文件 application.properties
```properties
server.port=8005
#
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost/demo2
spring.datasource.username=root
spring.datasource.password=root
#
spring.jpa.show-sql = true
#(create, create-drop, update)
spring.jpa.hibernate.ddl-auto = update
spring.jpa.hibernate.naming-strategy = org.hibernate.cfg.ImprovedNamingStrategy
spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.MySQL5Dialect
#
# Keep the connection alive if idle for a long time (needed in production)
spring.datasource.testWhileIdle = true
spring.datasource.validationQuery = SELECT 1
```

2. design 模块
pojo(前端使用): tk.wioo.pojo.UserPojo.java
```java
public class UserPojo {
    private long id;
    private String name;
    get/set...
}
```
tk.wioo.pojo.PageableList.java
```java
public class PageableList<T> implements Serializable {
    private static final long serialVersionUID = 768859725396601724L;
    private int pageNo, totalPages, pageSize;
    private long totalRecords;
    private List<T> records = new ArrayList<T>();
    set/get...
}
```
接口  tk.wioo.design.User.java
```java
@RequestMapping("/user")
public interface User {
    @RequestMapping(value="/getAll",method = RequestMethod.GET)
    public List<UserPojo> getAllUsers();
    @RequestMapping(method = RequestMethod.POST)
    public UserPojo createUser(@Valid @RequestBody UserPojo user);
    @RequestMapping(value="{id}", method = RequestMethod.GET)
    public ResponseEntity<UserPojo> findOne(@PathVariable("id") Long id);
    @RequestMapping(value="{id}", method = RequestMethod.PUT)
    public ResponseEntity<UserPojo> updateUser(@Valid @RequestBody UserPojo user, @PathVariable("id") Long id);
    @RequestMapping(value="{id}", method = RequestMethod.DELETE)
    public void deleteUser(@PathVariable("id") Long id) ;
}
```

3. data 模块
entity(数据库实体) tk.wioo.entity.UserEntity.java
```java
@Entity
@Table(name="user")
public class UserEntity {
    @Id
//    @GeneratedValue(strategy = GenerationType.AUTO)
//    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    @NotBlank
    private String name;
    get/set...    
}
```
repo(数据库dao操作) tk.wioo.entity.CommRepo.java
```java
@NoRepositoryBean
public interface CommRepo<T, ID extends Serializable> extends JpaRepository<T, ID>, JpaSpecificationExecutor<T> {
    List<T> findAll();
    T findOne(ID id);
    void delete(ID id);
}
```
tk.wioo.entity.UserRepo.java
```java
@Repository
public interface UserRepo extends CommRepo<UserEntity, Long> {
}
```

4. biz模块  
工具类 tk.wioo.utils.CommCopier.java  
```java
@Component
public interface CommCopier<V,E> {
    public V newViewObject();
    public E newEntity();
    public void copyForInsert(V vo, E entity);
    public void copyForUpdate(V vo, E entity);;
    public void copyToViewObject(E entity, V vo);
    public V copyToViewObject(E entity,Class<V> clazz);
    public E copyForInsert(V vo) ;
    public E copyForUpdate(V vo) ;
    public V copyToView(E entity) ;
}
```
tk.wioo.utils.CommCopierImpl.java
```java
@Component
public abstract class CommCopierImpl<V, E> implements CommCopier<V, E> {
    private Class  voclass;
    private Class entityClass;
    public CommCopierImpl() {
        // 反射得到T的真实类型
        ParameterizedType ptype = (ParameterizedType) this.getClass().getGenericSuperclass();
        // 获取当前new的对象的泛型的父类的类型
        // 获取第一个类型参数的真实类型model = clazz.newInstance();
        this.voclass = (Class<V>) ptype.getActualTypeArguments()[0];
        this.entityClass = (Class<E>) ptype.getActualTypeArguments()[1];
    }
    @Override
    public V newViewObject() {
      try {
            return (V)voclass.newInstance();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        return null;
    }
    @Override
    public E newEntity() {
        try {
            return (E)entityClass.newInstance();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        return null;
    }
    @Override
    public void copyForInsert(V vo, E entity) {
//      BeanUtils.copyProperties(vo, entity, "id");
        BeanUtils.copyProperties(vo, entity);
    }
     @Override
    public E  copyForInsert(V vo)  {
        E entity= null;
        try {
            entity = (E)entityClass.newInstance();
            copyForInsert(entity,vo);
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        return entity;
    }
    @Override
    public void copyForUpdate(V vo, E entity) {
        BeanUtils.copyProperties(vo, entity);
    }
    @Override
    public E copyForUpdate(V vo) {
        E entity= null;
        try {
           entity = (E)entityClass.newInstance();
            copyForUpdate(entity,vo);
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        return entity;
    }
    @Override
    public void copyToViewObject(E entity, V vo) {
        BeanUtils.copyProperties(entity, vo);
    }
    @Override
    public V copyToView(E entity)  {
        V vo=null;
        try {
           vo = (V)voclass.newInstance();
            copyToView(vo, entity);
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
       return  vo;
    }
    @Override
    public V copyToViewObject(E entity, Class<V> clazz) {
        V vo = null;
        try {
            vo = clazz.newInstance();
            BeanUtils.copyProperties(entity, vo);
        } catch (Exception e) {
//            logger.error("初始化{}对象失败。", clazz, e);
        }
        return vo;
    }
}
```
tk.wioo.utils.DataMaker.java
```java
@Component
public class DataMaker<V, E> {
    @Autowired
    private CommCopierImpl<V, E> commCopier;
        public List<V> toView(List<E> eList,Class<V> vClass) {
        List<V> vList = new ArrayList<V>();
        for (E e : eList) {
            V v =  commCopier.copyToViewObject(e,vClass );
            vList.add(v);
        }
        return vList;
    }
    public PageableList<V> toView(Page<E> page) {
        PageableList<V> pl = new PageableList<V>();
        pl.setPageNo(page.getNumber() + 1);
        pl.setPageSize(page.getSize());
        pl.setTotalPages(page.getTotalPages());
        pl.setTotalRecords(page.getTotalElements());
        List<V> list = new ArrayList<V>();
        List<E> pList = page.getContent();
        for (E entity : pList) {
            V vo = commCopier.newViewObject();
            commCopier.copyToViewObject(entity, vo);
            list.add(vo);
        }
        pl.setRecords(list);
        return pl;
    }
}
```
tk.wioo.copier.UserCopierImpl.java
```java
@Component
public class UserCopierImpl extends CommCopierImpl<UserPojo,UserEntity> {   }
```
业务实现 tk.wioo.biz.UserImpl.java
```java
@RestController
public class UserImpl implements User {
    @Autowired
    private UserRepo userRepo;
    @Autowired
    private UserCopierImpl userCopier;
    @Autowired
    private DataMaker<UserPojo, UserEntity> userDataMaker;

    public List<UserPojo> getAllUsers() {
        List<UserEntity> list = userRepo.findAll();
        List<UserPojo> pojoList = userDataMaker.toView(list,UserPojo.class);
        return pojoList;
    }

    @RequestMapping(method = RequestMethod.POST)
    public UserPojo createUser(@Valid @RequestBody UserPojo pojo) {
        UserEntity entity = new UserEntity();
        userCopier.copyForInsert(pojo, entity);
        entity = userRepo.save(entity);
        userCopier.copyToViewObject(entity, pojo);
        return pojo;
    }

    public ResponseEntity<UserPojo> findOne(@PathVariable("id") Long id) {
        UserEntity user = userRepo.findOne(id);
        if (user == null) {
            return new ResponseEntity<UserPojo>(HttpStatus.NOT_FOUND);
        }
        UserPojo pojo = new UserPojo();
        userCopier.copyToViewObject(user, pojo);
        return new ResponseEntity<UserPojo>(pojo, HttpStatus.OK);
    }
    public ResponseEntity<UserPojo> updateUser(@Valid @RequestBody UserPojo pojo, @PathVariable("id") Long id) {
        UserEntity userDb = userRepo.findOne(id);
        if (userDb == null) {
            return new ResponseEntity<UserPojo>(HttpStatus.NOT_FOUND);
        } else {
            userDb.setName(pojo.getName());
            userDb = userRepo.save(userDb);
            userCopier.copyToViewObject(userDb, pojo);
            return new ResponseEntity<UserPojo>(pojo, HttpStatus.OK);
        }
    }
    @RequestMapping(value = "{id}", method = RequestMethod.DELETE)
    public void deleteUser(@PathVariable("id") Long id) {
        userRepo.delete(id);
    }
}
```

5. 启动测试

# 集成SpringSecurity+thymeleaf
1. 添加依赖 pom.xml
```xml
 <!-- SpringSecurity、thymeleaf依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
```
2. 配置application.properties
```properties
logging.level.org.springframework.security=info
spring.thymeleaf.cache=false
spring.jackson.serialization.indent_output=true
spring.thymeleaf.check-templates-location=true
## 这个是配置模板路径的，默认就是templates，可不用配置
#spring.thymeleaf.prefix=classpath:/templates/
## 这个可以不配置，检查模板位置
#spring.thymeleaf.check-templates-location=true
#spring.thymeleaf.suffix=.html
#spring.thymeleaf.encoding=UTF-8
#spring.thymeleaf.content-type=text/html
#spring.thymeleaf.mode=HTML5
```
3. 用户和角色
SysRole.java
```java
@Entity
public class SysRole {
    @Id
    @GeneratedValue
    private Long id;
    private String name;
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
}
```
SysUser.java
```java
//实现UserDetails接口,即为Spring Security的用户
@Entity
public class SysUser implements UserDetails {
    @Id
    @GeneratedValue
    private Long id;
    private String username;
    private String password;

    @ManyToMany(cascade = {CascadeType.REFRESH},fetch = FetchType.EAGER)
    private List<SysRole> roles;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public List<SysRole> getRoles() {
        return roles;
    }

    public void setRoles(List<SysRole> roles) {
        this.roles = roles;
    }
//角色和权限关联
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        List<GrantedAuthority> auths = new ArrayList<>();
        List<SysRole> roles = this.getRoles();
        for (SysRole role : roles) {
            auths.add(new SimpleGrantedAuthority(role.getName()));
        }
        return auths;
    }

    @Override
    public String getPassword() {
        return this.password;
    }

    @Override
    public String getUsername() {
        return this.username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
```
SysUserRepository.java
```java
@Repository
public interface SysUserRepository extends CommRepo<SysUser, Long> {
    SysUser findByUsername(String username);
}
```
预设数据
```sql
insert  into `sys_role`(`id`,`name`) values (1,'ROLE_ADMIN'),(2,'ROLE_USER');
insert  into `sys_user`(`id`,`password`,`username`) values (1,'root','root'),(2,'sang','sang');
insert  into `sys_user_roles`(`sys_user_id`,`roles_id`) values (1,1),(2,2);
```
pojo 实体类向客户端传递消息的实体
Msg.java
```java
public class Msg {
    private String title;
    private String content;
    private String extraInfo;
    public Msg() {    }
    public Msg(String title, String content, String extraInfo) {
        this.title = title;
        this.content = content;
        this.extraInfo = extraInfo;
    }
    get/set...
}
```
4. 定义业务
主页：Home.java
```java
public interface Home {
    @RequestMapping("/")
    public String index(Model model) ;
}
```
HomeBiz.java
```java
@Controller
public class HomeBiz implements Home {
    public String index(Model model) {
        Msg msg = new Msg("测试标题", "测试内容", "额外信息，只对管理员显示");
        model.addAttribute("msg", msg);
        return "index";
    }
}
```
登录 UserDetailsService.java
```java
public class CustomUserService implements UserDetailsService {
    @Autowired
    SysUserRepository userRepository;
    //重写UserDetailsService接口，实现loadUserByUsername方法, 查询到对应的用户
    @Override
    public UserDetails loadUserByUsername(String s) throws UsernameNotFoundException {
        SysUser user = userRepository.findByUsername(s);
        if (user == null) {
            throw new UsernameNotFoundException("用户名不存在");
        }
        System.out.println("s:"+s);
        System.out.println("username:"+user.getUsername()+";password:"+user.getPassword());
        return user;
    }
}
```
5. SpringMVC配置
WebMvcConfig.java
```java
@Configuration
public class WebMvcConfig extends WebMvcConfigurerAdapter {
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        //访问login时跳转到login.html页面
        registry.addViewController("/login").setViewName("login");
    }
}
```
6. 配置Spring Security
WebSecurityConfig.java
```java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean
    UserDetailsService customUserService() {
        return new CustomUserService();
    }
    //注册CustomUserService的Bean，通过重写configure方法添加我们自定义的认证方式
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(customUserService());
    }
    //设置了登录页面，登录失败地址，设置注销请求,permitAll:任何人都可以访问
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .anyRequest().authenticated()
                .and().formLogin().loginPage("/login").failureUrl("/login?error").permitAll().and()
                .logout().logoutSuccessUrl("/login").permitAll();
////        http.authorizeRequests()
////                //.anyRequest().authenticated(),其他的请求都必须要有权限认证
////                .anyRequest().authenticated()
////                //管理员才可以访问admin文件夹下的内容
////                .antMatchers("/admin/**").hasAnyRole("ROLE_ADMIN","ROLE_USER")
////                //只允许访问ip为210.210.210.210的请求获取admin下的资源
////                .antMatchers("/admin/**").hasIpAddress("210.210.210.210")
////                .and().formLogin().loginPage("/login").defaultSuccessUrl("/index").failureUrl("/login?error").permitAll().and()
////                //开启cookie保存用户数据
////                .rememberMe()
////                //设置cookie有效期
////                .tokenValiditySeconds(60 * 60 * 24 * 7)
////                //设置cookie的私钥
////                .key("test").and()
////                //修改默认注销行为(logout),注销成功后跳转页面(默认:登录页面)
////                .logout().logoutUrl("/custom-logout").logoutSuccessUrl("/index").permitAll() ;
    }
}
```

7. 创建页面
   templates/login.html
   ```html
   <!DOCTYPE html>
   <html lang="en" xmlns:th="http://www.thymeleaf.org">
   <head>
       <meta charset="UTF-8"/>
       <title>登录</title>
       <link rel="stylesheet" th:href="@{css/bootstrap.min.css}"/>
       <link rel="stylesheet" th:href="@{css/signin.css}"/>
       <style type="text/css">
           body {
               padding-top: 50px;
           }
           .starter-template {
               padding: 40px 15px;
               text-align: center;
           }
       </style>
   </head>
   <body>
   <nav class="navbar navbar-inverse navbar-fixed-top">
       <div class="container">
           <div class="navbar-header">
               <a class="navbar-brand" href="#">Spring Security演示</a>
           </div>
           <div id="navbar" class="collapse navbar-collapse">
               <ul class="nav navbar-nav">
                   <li><a th:href="@{/}">首页</a></li>
                   <li><a th:href="@{http://www.baidu.com}">百度</a></li>
               </ul>
           </div>
       </div>
   </nav>
   <div class="container">
       <div class="starter-template">
           <p th:if="${param.logout}" class="bg-warning">已注销</p>
           <p th:if="${param.error}" class="bg-danger">有错误，请重试</p>
           <h2>使用账号密码登录</h2>
           <form class="form-signin" role="form" name="form" th:action="@{/login}" action="/login" method="post">
               <div class="form-group">
                   <label for="username">账号</label>
                   <input type="text" class="form-control" name="username" value="" placeholder="账号"/>
               </div>
               <div class="form-group">
                   <label for="password">密码</label>
                   <input type="password" class="form-control" name="password" placeholder="密码"/>
               </div>
               <input type="submit" id="login" value="Login" class="btn btn-primary"/>
           </form>
       </div>
   </div>
   </body>
   </html>
   ```
   templates/index.html
   ```html
   <!DOCTYPE html>
   <html lang="en" xmlns:th="http://www.thymeleaf.org"
         xmlns:sec="http://www.thymeleaf.org/thymeleaf-extras-springsecurity4">
   <head>
       <meta charset="UTF-8"/>
       <title sec:authentication="name"></title>
       <link rel="stylesheet" th:href="@{css/bootstrap.css}"/>
       <style type="text/css">
           body {
               padding-top: 50px;
           }
           .starter-template {
               padding: 40px 15px;
               text-align: center;
           }
       </style>
   </head>
   <body>
   <nav class="navbar navbar-inverse navbar-fixed-top">
       <div class="container">
           <div class="navbar-header">
               <a class="navbar-brand" href="#">Spring Security演示</a>
           </div>
           <div id="navbar" class="collapse navbar-collapse">
               <ul class="nav navbar-nav">
                   <li><a th:href="@{/}">首页</a></li>
                   <li><a th:href="@{http://www.baidu.com}">百度</a></li>
               </ul>
           </div>
       </div>
   </nav>
   <div class="container">
       <div class="starter-template">
           <h1 th:text="${msg.title}"></h1>
           <p class="bg-primary" th:text="${msg.content}"></p>
           <div sec:authorize="hasRole('ROLE_ADMIN')">
               <p class="bg-info" th:text="${msg.extraInfo}"></p>
           </div>
           <div sec:authorize="hasRole('ROLE_USER')">
               <p class="bg-info">无更多显示信息</p>
           </div>
           <form th:action="@{/logout}" method="post">
               <input type="submit" class="btn btn-primary" value="注销"/>
           </form>
       </div>
   </div>
   </body>
   </html>
   ```

8. 测试

# 集成 swagger
1. 依赖
```xml
        <!-- Swagger -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.6.1</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.6.1</version>
        </dependency>
```

2. 配置类 SwaggerConfig.java
```java
@Configuration
@EnableSwagger2 // 启用 Swagger
public class SwaggerConfig {
    @Bean
    public Docket createRestApi() {
        Predicate<RequestHandler> predicate = new Predicate<RequestHandler>() {
            @Override
            public boolean apply(RequestHandler input) {
                Class<?> declaringClass = input.declaringClass();
                if (declaringClass == BasicErrorController.class)// 排除
                    return false;
                if(declaringClass.isAnnotationPresent(RestController.class)) // 被注解的类
                    return true;
                if(input.isAnnotatedWith(ResponseBody.class)) // 被注解的方法
                    return true;
                return false;
            }
        };
        return new Docket(DocumentationType.SWAGGER_2)
//                .groupName("test")
//                .genericModelSubstitutes(DeferredResult.class)
//                .genericModelSubstitutes(ResponseEntity.class)
                .apiInfo(apiInfo())
                .useDefaultResponseMessages(false)
//                .forCodeGeneration(true)
//                .pathMapping("/")// base，最终调用接口后会和paths拼接在一起
                .select()
//                .paths(or(regex("/api/.*")))//过滤的接口
                .apis(predicate)
                .build()
//                .apiInfo(apiInfo());
                ;
    }
    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("接口列表")//大标题
                .description("详细描述")//详细描述
                .version("1.0")//版本
                .termsOfServiceUrl("NO terms of service")
                .contact("wioo.tk")//作者
                .license("Version 2.0")
        .licenseUrl("")
                .build();
    }
}
```

3. design接口配置
```java
@RequestMapping("/user")
public interface User {
    @ApiIgnore//使用该注解忽略这个API
    @RequestMapping(value="/getAll",method = RequestMethod.GET, produces= MediaType.APPLICATION_JSON_VALUE)
    public List<UserPojo> getAllUsers();
    @RequestMapping(method = RequestMethod.POST)
    public UserPojo createUser(@Valid @RequestBody UserPojo user);
    @RequestMapping(value="{id}", method = RequestMethod.GET)
    @ApiOperation(value="查找用户", notes="根据url的id来查找用户")
    @ApiImplicitParam(name = "id", value = "用户ID", required = true, dataType = "Long",paramType = "path")
    public ResponseEntity<UserPojo> findOne(
            @ApiParam(required=true, name="name", value="人员Id")
            @RequestParam(name = "name", required=true)
            @PathVariable("id") Long id);
    @RequestMapping(value="{id}", method = RequestMethod.PUT)
    @ApiOperation(value="更新信息", notes="根据url的id来指定更新信息")
    @ApiImplicitParams({
            @ApiImplicitParam(name = "id", value = "用户ID", required = true, dataType = "Long",paramType = "path"),
            @ApiImplicitParam(name = "user", value = "用户实体user", required = true, dataType = "UserPojo")
    })
    public ResponseEntity<UserPojo> updateUser(@Valid @RequestBody UserPojo user, @PathVariable("id") Long id);
    @RequestMapping(value="{id}", method = RequestMethod.DELETE)
    public void deleteUser(@PathVariable("id") Long id) ;
}
```
4. swagger常用注解
```
@Api：修饰整个类，描述Controller的作用
@ApiOperation：描述一个类的一个方法，或者说一个接口
@ApiParam：单个参数描述
@ApiModel：用对象来接收参数
@ApiProperty：用对象接收参数时，描述对象的一个字段
@ApiResponse：HTTP响应其中1个描述
@ApiResponses：HTTP响应整体描述
@ApiIgnore：使用该注解忽略这个API
@ApiError ：发生错误返回的信息
@ApiParamImplicitL：一个请求参数
@ApiParamsImplicit 多个请求参数
```

# 集成 lombok

1. 依赖 pom.xml
   ```xml
     <dependency>
         <groupId>org.projectlombok</groupId>
         <artifactId>lombok</artifactId>
         <version>1.16.8</version>
         <scope>provided</scope>
     </dependency>
   ```

2. 使用 
```java
@Entity
@Table(name="user")
@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
@Log4j
public class UserEntity {
    @Id
    private long id;
    @NotBlank
    private String name;
}
```