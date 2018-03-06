---
layout: post
title:  "springBoot+OAuth2+security集成单点登录项目（sso）"
date:   2018-01-15
desc: "springBoot+OAuth2+security集成单点登录项目（sso）"
keywords: "后端,springCloud,微服务,koa2"
categories: [Back]
tags: [后端,springCloud,微服务,koa2]
icon: icon-java
---
# 构建maven多模块项目
1. 创建基础maven项目及其子项目：auth、resource、client  
2. pom.xml  
```xml
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.2.RELEASE</version>
        <relativePath/>
    </parent>
    <dependencies>

    </dependencies>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    </properties>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>Dalston.SR1</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <!-- maven 打包插件-->
    <build>
        <!--<finalName>springCloud</finalName>-->
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
    <!-- 阿里云私服-->
    <repositories>
        <repository>
            <id>nexus-aliyun</id>
            <name>Nexus aliyun</name>
            <url>http://maven.aliyun.com/nexus/content/groups/public</url>
        </repository>
    </repositories>
```

# 授权服务器 auth

1. 依赖文件 pom.xml
```xml
    <artifactId>auth</artifactId>
    <packaging>jar</packaging>
    <name>AuthServer</name>
    <dependencies>
        <!-- 注意是starter,自动配置 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <!-- 不是starter,手动配置 -->
        <dependency>
            <groupId>org.springframework.security.oauth</groupId>
            <artifactId>spring-security-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
```

2. 主类 
```java
@SpringBootApplication
@RestController
@EnableAuthorizationServer
@EnableResourceServer
public class AuthApplication {
    @RequestMapping("/user")
    public Principal user(Principal user) {
        return user;
    }
    public static void main(String[] args) {
        SpringApplication.run(AuthApplication.class, args);
    }
}
```
 
3. 配置文件 application.properties
```properties
server.port=9999
server.contextPath= /uaa
#security.basic.enabled=false
security.user.name= admin
security.user.password= password
security.sessions=if-required
security.oauth2.client.clientId=acme
security.oauth2.client.clientSecret=pwd
security.oauth2.client.authorized-grant-types=authorization_code,refresh_token,password
security.oauth2.client.scope=openid
```

4. 测试

    1. 获取 code  
    `http://localhost:9999/uaa/oauth/authorize?response_type=code&client_id=acme&redirect_uri=http://baidu.com`  
    2.  获取token  
    `http://acme:pwd@localhost:9999/uaa/oauth/token?grant_type=authorization_code&client_id=acme&redirect_uri=http://baidu.com&code=gmtr9d`  
    `post` 提交   `Content-Type:application/x-www-from-urlencoded`  
    3. 访问接口  
    `http://localhost:9999/uaa/user`  
    请求头添加(token)： `Authorization: Bearer 91cab7a2-2f91-4639-858b-30d6aa7e5f9c`  

# 资源服务器 resource
1. 依赖文件 pom.xml
```xml
    <artifactId>resource</artifactId>
    <packaging>jar</packaging>
    <name>ResourceServer</name>
    <dependencies>
        <!-- 不是starter,手动配置 -->
        <dependency>
            <groupId>org.springframework.security.oauth</groupId>
            <artifactId>spring-security-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
```

2. 主类 
```java
@SpringBootApplication
@RestController
@EnableResourceServer
public class ResourceApplication {
    @RequestMapping("/")
    public String home() {
        return "Hello World";
    }
    public static void main(String[] args) {
        SpringApplication.run(ResourceApplication.class, args);
    }
}
```
 
3. 配置文件 application.properties
```properties
server.port=9999
server.contextPath= /uaa
#security.basic.enabled=false
security.user.name= admin
security.user.password= password
security.sessions=if-required
security.oauth2.client.clientId=acme
security.oauth2.client.clientSecret=pwd
security.oauth2.client.authorized-grant-types=authorization_code,refresh_token,password
security.oauth2.client.scope=openid
```

4. 测试  
    访问 `http://localhost:9998/res/`  
    头部信息(token) `Authorization: Bearer 91cab7a2-2f91-4639-858b-30d6aa7e5f9c`  

# 客户端

1. 依赖文件 pom.xml
```xml
    <artifactId>client</artifactId>
    <packaging>jar</packaging>
    <name>Client</name>
    <dependencies>
        <!-- 不是starter,手动配置 -->
        <dependency>
            <groupId>org.springframework.security.oauth</groupId>
            <artifactId>spring-security-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
    </dependencies>
```

2. 主类 
```java
@SpringBootApplication
@EnableOAuth2Sso
public class ClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(ClientApplication.class, args);
    }
}
```
 
3. 配置文件 application.properties
```properties
server.port=9997
server.contextPath= /
security.basic.enabled=false
security.oauth2.client.client-id= acme
security.oauth2.client.client-secret= pwd
security.oauth2.client.access-token-uri= http://localhost:9999/uaa/oauth/token
security.oauth2.client.user-authorization-uri=http://localhost:9999/uaa/oauth/authorize
security.oauth2.resource.userInfoUri= http://localhost:9999/uaa/user
security.oauth2.resource.tokenInfoUri= http://localhost:9999/uaa/oauth/token
#更倾向于用哪个
security.oauth2.resource.prefer-token-info=false
```

4. 控制类
```java
@RestController
public class Controller {
    @RequestMapping("/")
    public String index() {
        return "hello word !";
    }
    @RequestMapping("/abc")
    public String abc() {
        return "Hello abc";
    }
    @RequestMapping("/logout")
    public String logout() {
        return "goodBye";
    }
}
```

5. 测试
    `http://localhost:9997/`
    `http://localhost:9997/abc`

# 自定义登录页面和授权确认页面

1. 依赖 pom.xml
```xml
 <!--freemarker模板引擎-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-freemarker</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.45</version>
        </dependency>
```
2. 修改接口
```java
@Configuration
public class MvcConfig extends WebMvcConfigurerAdapter {
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/login").setViewName("login");
        registry.addViewController("/oauth/confirm_access").setViewName("authorize");
    }
}
```

3. UserDetailsService
```java
@Service
public class MyUserDetailsService implements UserDetailsService {
    @Override
    public UserDetails loadUserByUsername(String name) throws UsernameNotFoundException {
        if ("admin".equalsIgnoreCase(name)) {
            User user = mockUser();
            return user;
        }
        return null;
    }
    private User mockUser() {
        Collection<GrantedAuthority> authorities = new HashSet<>();
        authorities.add(new SimpleGrantedAuthority("admin"));//用户所拥有的角色信息
        User user = new User("admin","123456",authorities);
        return user;
    }
}
```

4. WebSecurityConfigurerAdapter
```java
@Order(10)
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private MyUserDetailsService userDetailsFitService;
    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
//                .authorizeRequests()
//                .antMatchers("/user").permitAll()
//                .anyRequest().authenticated()
//                .and()
                .formLogin().loginPage("/login").permitAll().and().authorizeRequests().antMatchers("/health", "/css/**")
                .anonymous().and().authorizeRequests().anyRequest().authenticated();
    }
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsFitService);
        auth.parentAuthenticationManager(authenticationManagerBean());
    }
}@Order(10)
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private MyUserDetailsService userDetailsFitService;
    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
//                .authorizeRequests()
//                .antMatchers("/user").permitAll()
//                .anyRequest().authenticated()
//                .and()
                .formLogin().loginPage("/login").permitAll().and().authorizeRequests().antMatchers("/health", "/css/**")
                .anonymous().and().authorizeRequests().anyRequest().authenticated();
    }
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsFitService);
        auth.parentAuthenticationManager(authenticationManagerBean());
    }
}
```

5. AuthorizationServerConfigurerAdapter
```java
@Configuration
@EnableAuthorizationServer
public class AuthConfig extends AuthorizationServerConfigurerAdapter {
    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired
    private MyUserDetailsService userDetailsService;
    @Override
    public void configure(final AuthorizationServerSecurityConfigurer oauthServer) throws Exception {
        oauthServer.tokenKeyAccess("permitAll()").checkTokenAccess("isAuthenticated()");
    }
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory() // 使用in-memory存储
                .withClient("acme") // client_id
                .secret("pwd") // client_secret
                .authorizedGrantTypes("authorization_code","password","client_credentials") // 该client允许的授权类型
                .scopes("read","write","trust") // 允许的授权范围
                .accessTokenValiditySeconds(1800000);
    }
    @Override
    public void configure(final AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        // @formatter:off
        endpoints.authenticationManager(authenticationManager)
                .userDetailsService(userDetailsService);
        // @formatter:on
    }
}
```

6. 模板 resources/templates/authorize.ftl
   ```html
   <html>
   <head>
       <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.js"></script>
       <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.css" rel="stylesheet">
   </head>
   <body>
   <div class="container">
       <h2>Please Confirm</h2>
       <p>
           Do you authorize "${authorizationRequest.clientId}" at "${authorizationRequest.redirectUri}" to access your
           protected resources
           with scope ${authorizationRequest.scope?join(", ")}.
       </p>
       <form id="confirmationForm" name="confirmationForm" action="../oauth/authorize" method="post">
       <#list authorizationRequest.scope as scop>
           <input type="hidden" name="scope.${scop}" value="true"/>
       </#list>
           <input name="user_oauth_approval" value="true" type="hidden"/>
           <input type="hidden" id="csrf_token" name="${_csrf.parameterName}" value="${_csrf.token}"/>
           <button class="btn btn-primary" type="submit">Approve</button>
       </form>
       <form id="denyForm" name="confirmationForm"  action="../oauth/authorize" method="post">
           <input name="user_oauth_approval" value="false" type="hidden"/>
           <input type="hidden" id="csrf_token" name="${_csrf.parameterName}" value="${_csrf.token}"/>
           <button class="btn btn-primary" type="submit">Deny</button>
       </form>
   </div>
   </body>
   </html>
   ```

7.  模板 resources/templates/login.ftl
   ```html
      <html>
      <head>
          <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
      </head>
      <body>
      <div class="container">
          <form role="form" action="login" method="post">
              <div class="form-group">
                  <label for="username">Username:</label>
                  <input type="text" class="form-control" id="username" name="username"/>
              </div>
              <div class="form-group">
                  <label for="password">Password:</label>
                  <input type="password" class="form-control" id="password" name="password"/>
              </div>
              <input type="hidden" id="csrf_token" name="${_csrf.parameterName}" value="${_csrf.token}"/>
              <button type="submit" class="btn btn-primary">Submit</button>
          </form>
      </div>
      <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
      </body>
      </html>
   ```

8. 测试
    1. `http://localhost:9999/uaa/oauth/authorize?response_type=code&client_id=acme&redirect_uri=http://baidu.com&state=123`  
    2. `https://www.baidu.com/?code=GS5qu8&state=123`
    3. `http://localhost:9999/uaa/oauth/token?client_id=acme&grant_type=authorization_code&redirect_uri=http://baidu.com&code=GS5qu8`
(使用的是内存模式无法用客户端测试，应使用数据库等持久化模式)

# JDBC

# redis



