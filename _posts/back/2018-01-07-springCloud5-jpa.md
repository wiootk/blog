---
layout: post
title:  "springCloud集成jpa(使用Swagger2自动生成文档)"
date:   2018-01-06
desc: "springCloud集成jpa(使用Swagger2自动生成文档)"
keywords: "后端,springCloud,微服务,jpa,Swagger2"
categories: [Back]
tags: [后端,springCloud,微服务,jpa,Swagger2]
icon: icon-java
---
# 基础项目

1. 父项目pom.xml
   ```xml
   <!--  Swagger2自动生成api -->
   <dependency>
       <groupId>io.springfox</groupId>
       <artifactId>springfox-swagger2</artifactId>
       <version>2.2.2</version>
   </dependency>
   <dependency>
       <groupId>io.springfox</groupId>
       <artifactId>springfox-swagger-ui</artifactId>
       <version>2.2.2</version>
   </dependency>
   ```

2. pom.xml
   ```xml
   <modelVersion>4.0.0</modelVersion>
   <artifactId>demo_jpa</artifactId>
   <packaging>jar</packaging>
   <name>jpa</name>
   <dependencies>
       <dependency>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-data-jpa</artifactId>
       </dependency>
       <dependency>
           <groupId>mysql</groupId>
           <artifactId>mysql-connector-java</artifactId>
       </dependency>
       <dependency>
           <groupId>javax.inject</groupId>
           <artifactId>javax.inject</artifactId>
           <version>1</version>
       </dependency>
   </dependencies>
   ```

3. 启动类JpaApplication.java
```java
@SpringBootApplication
//服务注册客户端
@EnableEurekaClient
//@EnableWebMvc
//@EnableDiscoveryClient
//激活Eureka中的DiscoveryClient实现
public class JpaApplication {
    public static void main(String[] args) {
//        SpringApplication.run(ClientApplication.class, args);
        new SpringApplicationBuilder(JpaApplication.class).web(true).run(args);
    }
}
```

4. Swagger2的配置文件
```java
//http://localhost:{port}/swagger-ui.html 或在注册服务的列表点击超链接
@Configuration
@EnableSwagger2 // 启用Swagger2
public class Swagger2 implements EnvironmentAware {
    private String basePackage;
    private RelaxedPropertyResolver propertyResolver;

    //  public void addResourceHandlers(ResourceHandlerRegistry registry) {
//    registry.addResourceHandler("swagger-ui.html")
//            .addResourceLocations("classpath:/META-INF/resources/");
//    registry.addResourceHandler("/webjars/**")
//            .addResourceLocations("classpath:/META-INF/resources/webjars/");
//}
    @Bean
    public Docket createRestApi() {// 创建API基本信息
        return new Docket(DocumentationType.SWAGGER_2)
                //.pathMapping("/get/")
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.jun"))
                // 扫描该包下的所有需要在Swagger中展示的API(包括实现的包)，@ApiIgnore注解标注的除外
                .paths(PathSelectors.any())
//              .paths(Predicates.or(
//                        //这里添加你需要展示的接口
//                        PathSelectors.ant("/qqq/**"),
//                        PathSelectors.ant("/eee/**")
//                        )
//                )
                .build();
    }
    private ApiInfo apiInfo() {// 创建API的基本信息，这些信息会在Swagger UI中进行显示
        return new ApiInfoBuilder()
                .title("Swagger2构建RESTful APIs")// API 标题
                .description("jpa提供的API")// API描述
                .contact("jun@")// 联系人
                .version("1.0")// 版本号
                .build();
    }
    @Override
    public void setEnvironment(Environment environment) {
        this.propertyResolver = new RelaxedPropertyResolver(environment, (String) null);
        this.basePackage = this.propertyResolver.getProperty("swagger.basepackage");
    }
}
```

5. 配置文件applicaton.properties
```properties
spring.application.name=jpa
server.port=8001
eureka.client.serviceUrl.defaultZone=http://admin:123@localhost:1111/eureka/
#eureka.instance.hostname=localhost
#eureka.instance.metadata-map.instanceId=${spring.application.name}:${spring.application.instance_id:${random.value}}
#eureka.instance.instance-id=
#eureka.instance.prefer-ip-address=true
eureka.instance.lease-expiration-duration-in-seconds=1
eureka.instance.lease-renewal-interval-in-seconds=1
eureka.client.fetchRegistry= true
eureka.client.registry-fetch-interval-seconds=1
# mysql 属性配置
spring.datasource.url=jdbc:mysql://localhost:3306/demo3
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.jpa.database-platform=org.hibernate.dialect.MySQL5InnoDBDialect
# create  create-drop  update validate
spring.jpa.properties.hibernate.hbm2ddl.auto=update
jpa.hibernate.show.show-sql=true
# 打印日志
logging.level.root= INFO
logging.level.org.hibernate= INFO
logging.level.org.hibernate.type.descriptor.sql.BasicBinder= TRACE
logging.level.org.hibernate.type.descriptor.sql.BasicExtractor=TRACE
logging.level.com.springms=DEBUG
#Swagger2
eureka.instance.status-page-url=http://localhost:${server.port}/swagger-ui.html
swagger.basepackage= com.jun.desion
```

# 代码
## 1. com.jun.design.pojo 展现层的bean

1. UserInfo
```java
public class UserInfo {
    @ApiModelProperty(value = "主键", hidden = false, notes = "主键，隐藏", required = true, dataType = "Long")
    // 使用该注解描述属性信息,当hidden=true时，该属性不会在api中显示
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    @ApiModelProperty(value = "名字")
    @Column(nullable = false)
    private String name;
    @Column(nullable = false)
    private Integer age;
    // 省略 get/set...
}
```

2. PageableQueryParam:分页查询条件
```java
public class PageableQueryParam implements Serializable {
    private static final long serialVersionUID = -3633225672081343653L;
    private int pageNo = 0, pageSize = 10;
    @ApiModelProperty(value = "页码", hidden = false, notes = "页码", required = true, dataType = "int")
    public int getPageNo() {
        return pageNo;
    }
    public void setPageNo(int pageNo) {
        this.pageNo = pageNo;
    }
    @ApiModelProperty(value = "每页多少条", hidden = false, notes = "每页多少条", required = true, dataType = "int")
    public int getPageSize() {
        return pageSize;
    }
    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }
}
```

3. PageableList 返回的分页列表
```java
public class PageableList<T> implements Serializable {
    private static final long serialVersionUID = 768859725396601724L;
    private int pageNo=1, totalPages, pageSize=10;
    private long totalRecords;
    private List<T> records = new ArrayList<T>();
    @ApiModelProperty(value = "页码", hidden = false, notes = "页码", required = true, dataType = "int")
    public int getPageNo() {
        return pageNo;
    }
    public void setPageNo(int pageNo) {
        this.pageNo = pageNo;
    }
    @ApiModelProperty(value = "总页数", hidden = false, notes = "总页数", required = true, dataType = "int")
    public int getTotalPages() {
        return totalPages;
    }
    public void setTotalPages(int totalPages) {
        this.totalPages = totalPages;
    }
    @ApiModelProperty(value = "每页多少条", hidden = false, notes = "每页多少条", required = true, dataType = "int")
    public int getPageSize() {
        return pageSize;
    }
    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }
    @ApiModelProperty(value = "总条数", hidden = false, notes = "总条数", required = true, dataType = "int")
    public long getTotalRecords() {
        return totalRecords;
    }
    public void setTotalRecords(long totalRecords) {
        this.totalRecords = totalRecords;
    }
    @ApiModelProperty(value = "数据列表", hidden = false, notes = "数据列表", required = true, dataType = "List")
    public List<T> getRecords() {
        return records;
    }
    public void setRecords(List<T> records) {
        this.records = records;
    }
}
```

## 2. com.jun.design.design 接口设计
```java
@RestController
@Api(value = "API - UserController")
public interface User {
    @ApiOperation(value = "获取User信息", notes = "根据id获取User信息")// 描述接口方法信息
    @ApiImplicitParams({
            @ApiImplicitParam(name = "id", value = "User表ID", required = true, dataType = "Long", paramType = "path")
    })//描述方法参数信息，paramType值path
    @GetMapping("/get/{id}")
    UserInfo get(@PathVariable Long id);

    @ApiOperation(value = "所有user列表", notes = "根据分页信息获取User列表")
    @ApiImplicitParams({
            @ApiImplicitParam(name = "param", value = "{\r\"pageNo\":第几页,\r\"pageSize\":每页多少条\r}", required = true, dataType = "PageableQueryParam", paramType = "body")
    })//描述方法参数信息，paramType值path
    @PostMapping("/find/all")
    PageableList<UserInfo> getAll(PageableQueryParam param);
}
```

## 3. com.jun.data.entity 数据库实体
```java
@Entity
@Table(name="user")
public class UserEntity implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    @Column(nullable = false)
    private String name;
    @Column(nullable = false)
    private Integer age;
 // 省略 get/set...
}
```

##  3. com.jun.data.repo 数据仓库相当于DAO
```java
@Repository
public interface UserRepo extends JpaRepository<UserEntity, Long> {
    UserEntity findByName(String name);
    UserEntity findByNameAndAge(String name, Integer age);
    @Query("from UserEntity u where u.name=:name")
    UserEntity findUser(@Param("name") String name);
}
```

## 4. com.jun.biz.utils 工具类

1. 呈现层与实体对象属性拷贝
   ```java
   public interface DataCopier<V, E> {
       /**
        * 创建呈现层对象的实例，带默认值
        * @return
        */
       V newViewObject();
       /**
        * 创建实体对象实例
        * @return
        */
       E newEntity();
       /**
        * 将呈现层对象的属性值拷贝到实体对象的对应属性中，以便新增实体时使用
        * @param vo        呈现层对象
        * @param entity    实体对象
        */
       void copyToEntityForInsert(V vo, E entity);
       /**
        * 将呈现层对象的属性值拷贝到实体对象的对应属性中，以便修改实体时使用
        * @param vo        呈现层对象
        * @param entity    实体对象
        */
       void copyToEntityForUpdate(V vo, E entity);
       /**
        * 将实体对象的属性拷贝到呈现层对象的对应属性中
        * @param entity    实体对象
        * @param vo        呈现层对象
        */
       void copyToViewObject(E entity, V vo);
   }
   ```

2. PageableListMaker 组装分页信息
   ```java
   @Named
   public class PageableListMaker<E, V> {
       /**
        * 获取PageableList，并将实体转换成VO
        * @param page          分页查询结果
        * @param dataCopier    数据拷贝器
        * @return
        */
       public PageableList<V> get(Page<E> page, DataCopier<V, E> dataCopier) {
           PageableList<V> pl = get(page);
           List<V> list = pl.getRecords();
           if(dataCopier != null) {
               List<E> pList = page.getContent();
               for(E entity : pList) {
                   V vo = dataCopier.newViewObject();
                   dataCopier.copyToViewObject(entity, vo);
                   list.add(vo);
               }
           }
           return pl;
       }
       /**
        * 获取PageableList，不进行VO转换
        * @param page  分页查询结果
        * @return
        */
       public PageableList<V> get(Page<E> page) {
           PageableList<V> pl = new PageableList<V>();
           pl.setPageNo(page.getNumber() + 1);
           pl.setPageSize(page.getSize());
           pl.setTotalPages(page.getTotalPages());
           pl.setTotalRecords(page.getTotalElements());
           List<V> list = new ArrayList<V>();
           pl.setRecords(list);
           return pl;
       }
   }
   ```

## 5. com.jun.biz.copier 呈现层与实体对象属性拷贝的实现
```java
@Named
public class UserCopier implements DataCopier<UserInfo, UserEntity> {
    @Override
    public UserInfo newViewObject() {
        UserInfo info=new UserInfo();
        return info;
    }
    @Override
    public UserEntity newEntity() {
        UserEntity entity=new UserEntity();
        return entity;
    }
    @Override
    public void copyToEntityForInsert(UserInfo vo, UserEntity entity) {
        BeanUtils.copyProperties(vo,entity,"id");

    }
    @Override
    public void copyToEntityForUpdate(UserInfo vo, UserEntity entity) {
        BeanUtils.copyProperties(vo,entity,"id");
    }
    @Override
    public void copyToViewObject(UserEntity entity, UserInfo vo) {
        BeanUtils.copyProperties(entity,vo);
    }
}
```

## 6. com.jun.biz.biz 业务逻辑
```java
@Service
public class UserImpl implements User {
    @Inject
    private UserRepo repo;
    @Inject
    private UserCopier copier;
    @Inject
    private PageableListMaker<UserEntity,UserInfo> maker;
    @Override
    public UserInfo get(@PathVariable Long id) {
        UserEntity  entity=repo.findOne(id);
        UserInfo info=new UserInfo();
        copier.copyToViewObject(entity,info);
        return info;
    }
    @Override
    public PageableList<UserInfo> getAll(PageableQueryParam param) {
        PageRequest pageRequest=new PageRequest(param.getPageNo(), param.getPageSize(), Sort.Direction.DESC, "age");
        Page<UserEntity> entityPage=repo.findAll(pageRequest);
        return maker.get(entityPage,copier);
    }
}
```

## 7. 测试
`http://localhost:8001/get/1`  
`http://localhost:8001/find/all`  
`http://localhost:8001/swagger-ui.html`  













