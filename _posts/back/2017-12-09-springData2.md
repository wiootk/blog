---
layout: post
title:  "SpringDataJPA 使用"
date:   2017-12-09
desc: "SpringDataJPA 使用"
keywords: "后端,SpringDataJPA"
categories: [Back]
tags: [后端,SpringDataJPA]
icon: icon-java
---

**根据[SpringMVC+SpringDataJPA+Hibernate搭建教程 ](/blog/back/2017/12/09/springData1.html)搭建环境**  
# 一、 构建自己的repo 实现逻辑删除（构建删除表存储删除的数据）
1. 构建repo
```java
@NoRepositoryBean
public interface MyRepo<T, ID extends Serializable> extends JpaRepository<T, ID>, JpaSpecificationExecutor<T> {
    void logicDelete(ID id);
    void logicDelete(T t);
    T recover(ID id) throws ClassNotFoundException;
}
```
2. 创建删除数据存储表
```java
@Entity
@Table(name = "recover")
public class RecoverEntity implements Serializable {
    private static final long serialVersionUID = 7077267778320168471L;
    @Id
    private  String id= Common.getUUIDStr();
    private  String entityName;
    private String entity;
    private  long deleteTime;
    private String deleteOperorId;
    private String deleteOperorName;
    @Column(name = "recoverTime",nullable =true )
    private  long recoverTime=0;
    private String recoverOperorId;
    private String recoberOperorName;
    set/get...
}
```
3. 实现repo中自定义方法
```java
//@Repository
@Transactional
public class MyRepoImpl<T, ID extends Serializable> extends SimpleJpaRepository<T, ID> implements MyRepo<T, ID> {
    private final EntityManager entityManager;
    public MyRepoImpl(JpaEntityInformation<T, ?> entityInformation, EntityManager entityManager) {
        super(entityInformation, entityManager);
        this.entityManager = entityManager;
    }
    public MyRepoImpl(Class<T> domainClass, EntityManager em) {
        super(domainClass, em);
        this.entityManager = em;
    }
    String insertSql = "insert into recover(deleteOperorId, deleteOperorName, deleteTime, entity, entityName,recoverTime,id) values (?, ?, ?, ?, ?, ?,?)";
    String updateSql = "update RecoverEntity as r set  r.recoberOperorName=:operorName,r.recoverOperorId=:operorId,r.recoverTime=:rtime  where r.id=:id";
    String selectSql = "select o from RecoverEntity o where o.id=:id";
//    @Autowired
//    private RecoverRepo recoverRepo;

    public void logicDelete(ID id) {
        T t = this.findOne(id);
        this.logicDelete(t);
    }
    //@Transactional(readOnly = false, propagation = Propagation.REQUIRED)
    public void logicDelete(T t) {
//        Query query = entityManager.createNativeQuery(insertSql, RecoverEntity.class);
//        query.setParameter(1, recover.getEntityName());
//        query.executeUpdate();
        RecoverEntity recover = new RecoverEntity();
        recover.setDeleteTime(System.currentTimeMillis());
        recover.setEntityName(t.getClass().getName());
        recover.setEntity(JSON.toJSONString(t));
        entityManager.persist(recover);
        entityManager.flush();
//      entityManager.merge(entity); update
        this.delete(t);
    }
    @Transactional
    public T recover(ID id) throws ClassNotFoundException {
//        Query query = entityManager.createQuery(selectSql, RecoverEntity.class);
//        query.setParameter("id", id);
//        RecoverEntity recover = (RecoverEntity) query.getResultList().get(0);
////        Assert.isNull(recover, ProjectErrorCodes.FAIL, "包车牌不存在！！！");
//        recover.setRecoverTime(System.currentTimeMillis());
//        Query query2 = entityManager.createQuery(updateSql);
//        query2.setParameter("id", recover.getId());
//        query2.executeUpdate();
        RecoverEntity recover = entityManager.find(RecoverEntity.class,id);
        recover.setRecoverTime(System.currentTimeMillis());
        entityManager.merge(recover);
//        Class <T>  entityClass  =  (Class <T> ) ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[ 0 ];
        Class clazz = Class.forName(recover.getEntityName());
        T t = (T) JSON.parseObject(recover.getEntity(), clazz);
//        this.save(t);
        entityManager.persist(t);
        entityManager.flush();
        return t;
    }
}
```
4. 扩展jpaRepository,让所有的repository共享起自定义的方法
```java
public class MyRepoFactoryBean <R extends JpaRepository<T, I>, T, I extends Serializable> extends JpaRepositoryFactoryBean<R, T, I> {
    @SuppressWarnings("rawtypes")
    protected RepositoryFactorySupport createRepositoryFactory(EntityManager em) {
        return new CustomRepositoryFactory(em);
    }
    private static class CustomRepositoryFactory<T, I extends Serializable>
            extends JpaRepositoryFactory {
        private final EntityManager em;
        public CustomRepositoryFactory(EntityManager em) {
            super(em);
            this.em = em;
        }
        @SuppressWarnings("unchecked")
        protected Object getTargetRepository(RepositoryMetadata metadata) {
            return new MyRepoImpl<T, I>(
                    (Class<T>) metadata.getDomainType(), em);
        }
        protected Class<?> getRepositoryBaseClass(RepositoryMetadata metadata) {
            return MyRepoImpl.class;
        }
    }
}
```
5. xml文件中配置
```xml
    <jpa:repositories
            factory-class="com.jun.util.MyRepoFactoryBean"
            transaction-manager-ref="transactionManager"
            entity-manager-factory-ref="entityManagerFactory" base-package="com.jun.dao" />
```

# 二、 注解生成日志  
1. 编写日志存储表
```java
@Entity
@Table(name = "bizLog")
public class BizLogEntity implements Serializable {
    private static final long serialVersionUID = 7077267778320168471L;
    @Id
    private  String id= UUID.randomUUID().toString();
    private  long bizTime;
    private  String bizType;
    @Column(length = 4000)
    private  String remark;
    private String objType;
    private String  objId;
    private String operatorId;
    private String operatorName;
  //  get/set...    
}
```
2. 编写repo
```java
public interface BizLogRepo extends MyRepo<BizLogEntity,String> {
}
```
3. 编写注解
```java
@Target({ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface LogService {
    //描述
    String desc() default "";
    String oprateType() default "";
    String objId() default "";
    String objType() default "";
}
```
4. 编写注解实现
    ```java
    package com.jun.util;
    import com.alibaba.fastjson.JSON;
    import com.jun.dao.BizLogRepo;
    import com.jun.entity.BizLogEntity;
    import org.apache.commons.logging.Log;
    import org.apache.commons.logging.LogFactory;
    import org.aspectj.lang.JoinPoint;
    import org.aspectj.lang.annotation.*;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Component;
    import java.lang.reflect.Method;
    import java.util.HashMap;
    import java.util.Map;
    
    @Aspect
    @Component
    public class InterfaceRecord {
    
        @Autowired
        private BizLogRepo logRepo;
        // 初始化日志类
        private static final Log logger = LogFactory.getLog(InterfaceRecord.class);
        private static String operId = "";
        // Service层切点
        // TODO: 2017-05-05  biz层全部包括
    //    @Pointcut("execution(* com.jun.controller.*.insert(..))")
        //  @Around("within(@org.springframework.stereotype.Controller *) && @annotation(is)")
        @Pointcut("@annotation(com.jun.util.LogService)")
        public void serviceAspect() {   }
    
        @Before(value = "serviceAspect()")
        public void doBefore(JoinPoint joinPoint) {
            long now = System.currentTimeMillis();
            logger.info("接口拦截开始时间：" + now);
        }
    
        @AfterReturning(value = "serviceAspect()", argNames = "retVal", returning = "retVal")
        public void doAfterReturning(JoinPoint joinPoint, Object retVal) {
            long now = System.currentTimeMillis();
            logger.info("接口拦截结束时间：" + now);
            BizLogEntity log = new BizLogEntity();
            try {
                // 补充数据
                log = supplementEntity(log, joinPoint);
                // 返回参数
                String responseStr = "";
                if (retVal != null && "".equals(operId)) {
                    responseStr = JSON.toJSONString(retVal);
                    operId = JSON.parseObject(responseStr).getString("id");
                    log.setObjId(operId);
                }
                logRepo.save(log);
            } catch (Exception e) {
                logger.error("==异常通知异常==");
                logger.error("异常信息:{}", e);
            }
        }
    
        //异常统一处理
        @AfterThrowing(pointcut = "serviceAspect()", throwing = "e")
        public void doAfterThrowing(JoinPoint joinPoint, Throwable e) {
            long now = System.currentTimeMillis();
            logger.error(e);
            logger.error("接口异常拦截时间：" + now);
            BizLogEntity log = new BizLogEntity();
            try {
                // 补充数据
                log = supplementEntity(log, joinPoint);
                String responseStr = "";
                if (e != null) {
                    responseStr = JSON.toJSONString(e);
                }
                // 响应信息
    //            logger.error("接口异常信息：" + responseStr);
            } catch (Exception ee) {
                logger.error("==异常通知异常==");
                logger.error("异常信息:{}", ee);
            }
        }
    
        // 匹配com.owenapp.service.impl包下所有类的、
        // 所有方法的执行作为切入点
        @AfterThrowing(throwing = "ex"
                , pointcut = "execution(* com.jun.service.impl.*.*(..))")
        // 声明ex时指定的类型会限制目标方法必须抛出指定类型的异常
        // 此处将ex的类型声明为Throwable，意味着对目标方法抛出的异常不加限制
        public void doRecoveryActions(Throwable ex) {
    
            System.out.println("目标方法中抛出的异常:" + ex);
            System.out.println("模拟Advice对异常的修复...");
        }
    
        /**
        * TODO 填充数据
        */
        private BizLogEntity supplementEntity(BizLogEntity log, JoinPoint joinPoint) {
            // 请求的IP
    //        try {
    //            HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder
    //                    .getRequestAttributes()).getRequest();
    //            String ip = request.getRemoteAddr();
    //        } catch (Exception ee) {
    //            logger.error("获取不到httprequest：" + ee);
    //        }
            // 注解
            Map<String, String> annos = getServiceMthodAnnotatin(joinPoint);
            log.setBizTime(System.currentTimeMillis());
            log.setBizType(annos.get("bizType"));
            log.setRemark(annos.get("remark"));
            log.setObjId(annos.get("objId"));
            log.setObjType(annos.get("objType"));
            log.setOperatorId("操作人Id");
            log.setOperatorName("操作人");
            return log;
        }
    
        public static String getParms(JoinPoint joinPoint) {
            StringBuffer requestStr = new StringBuffer();
            if (joinPoint.getArgs() != null && joinPoint.getArgs().length > 0) {
                for (int i = 0; i < joinPoint.getArgs().length; i++) {
                    if (i != joinPoint.getArgs().length - 1) {
                        requestStr.append(JSON.toJSONString(joinPoint.getArgs()[i]));
                        requestStr.append(",");
                    } else {
                        requestStr.append(JSON.toJSONString(joinPoint.getArgs()[i]));
                    }
                }
            }
    //    System.out.println(joinPoint.getSignature().getName());
            return "[" + requestStr.toString() + "]";
    
        }
    
        /**
        * 获取注解中对方法的描述信息 用于service层注解
        */
        @SuppressWarnings("rawtypes")
        public static Map<String, String> getServiceMthodAnnotatin(JoinPoint joinPoint) {
            Map<String, String> result = new HashMap<String, String>();
            // 获取target class名称
            String targetName = joinPoint.getTarget().getClass().getName();
            // 获取target method名称
            String methodName = joinPoint.getSignature().getName();
            // 获取请求参数
            Object[] arguments = joinPoint.getArgs();
            // 注解类
            try {
                Class targetClass = Class.forName(targetName);
                Method[] methods = targetClass.getMethods();
                // 注解方法
                String description = "";
                String oprateType = "";
                String objId = "";
                String objType = "";
                for (Method method : methods) {
                    if (method.getName().equals(methodName)) {
                        Class[] clazzs = method.getParameterTypes();
                        if (clazzs.length == arguments.length) {
                            description = method.getAnnotation(LogService.class).desc();
                            oprateType = method.getAnnotation(LogService.class).oprateType();
                            objType = method.getAnnotation(LogService.class).objType();
                            objId = method.getAnnotation(LogService.class).objId();
                            // 接口描述
                            if ("".equals(description)) {
    //  String requestMethod = joinPoint.getTarget().getClass().getName() + "." + joinPoint.getSignature().getName() + "()";
                                result.put("remark", targetName + "." + methodName + ":" + getParms(joinPoint));
                            } else {
                                result.put("remark", description + ":" + getParms(joinPoint));
                            }
                            result.put("bizType", oprateType);
    //                        System.out.println(joinPoint.getArgs()[0].getClass().getName());
                            if (!"".equals(objId) && joinPoint.getArgs().length > 0 && joinPoint.getArgs()[0] != null) {
                                operId = JSON.parseObject(JSON.toJSONString(joinPoint.getArgs()[0])).getString(objId);
                            }
                            result.put("objId", operId);
                            result.put("objType", objType);
                            break;
                        }
                    }
                }
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            }
            return result;
        }
    }
    ```
5. 编写log4J 配置文件
    ```properties
    log4j.rootLogger = DEBUG, console
    
    log4j.logger.org.springframework = WARN
    log4j.logger.org.hibernate = WARN
    log4j.logger.com.mchange = WARN
    
    log4j.appender.console=org.apache.log4j.ConsoleAppender
    log4j.appender.console.layout=org.apache.log4j.PatternLayout
    log4j.appender.console.layout.ConversionPattern=%-d{yyyy-MM-dd HH:mm:ss} [%l]%n[%p] %m%n%n
    
    #log4j.appender.STDOUT.Threshold=trace
    #log4j.category.org.hibernate.SQL=trace
    #log4j.category.org.hibernate.type=trace
    ```

6. 在springmvc-servlet.xml 加入注解支持
    ```xml
    <aop:aspectj-autoproxy proxy-target-class="true"/>
    ```
7. 在pom.xml添加依赖
```xml
   <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjrt</artifactId>
      <version>1.7.4</version>
    </dependency>
    <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjweaver</artifactId>
      <version>1.7.4</version>
    </dependency>
```

8. 使用
```java
    @RequestMapping("/doLog")
    @ResponseBody
    @LogService(desc = "操作日志demo", oprateType = "oprateType", objId = "1",objType="12")
    public Map<String, Object> doLog(String id){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data","操作日志demo");
        return map;
    }
```

# 三、swagger
1. 添加依赖
```xml
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
2. SwaggerConfig 
```java
@EnableWebMvc
@EnableSwagger2
@Configuration
@ComponentScan(basePackages="com.jun.controller")//com.*.controller
public class SwaggerConfig {
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
//                .apis(RequestHandlerSelectors.basePackage("com.jun.controller"))
                .paths(PathSelectors.any())
                .build();
    }
    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("接口列表") // 任意，请稍微规范点
                .description("接口测试") // 任意，请稍微规范点
                .termsOfServiceUrl("http://localhost:8080/swagger-ui.html") // 将“url”换成自己的ip:port
                .contact("wioo") // 无所谓（这里是作者的别称）
                .version("1.1.0")
                .build();
    }
}
```
3. 在springmvc-servlet.xml配置
```xml
   <!-- &lt;!&ndash; 拦截器 &ndash;&gt;
    <mvc:interceptors>
        &lt;!&ndash; 登录拦截 &ndash;&gt;
        <mvc:interceptor>
            <mvc:mapping path="/**"/>
            <mvc:exclude-mapping path="/swagger*/**"></mvc:exclude-mapping>
            <mvc:exclude-mapping path="/v2/**"></mvc:exclude-mapping>
            <mvc:exclude-mapping path="/webjars/**"></mvc:exclude-mapping>
            <bean class="com.jun.util.LoginInterceptor"/>
        </mvc:interceptor>
    </mvc:interceptors>-->

    <mvc:resources mapping="swagger-ui.html" location="classpath:/META-INF/resources/"/>
    <mvc:resources mapping="/webjars/**" location="classpath:/META-INF/resources/webjars/"/>
```
4. 使用
```java
@Controller
@RequestMapping("/demo2")
//@Api(description="swagger版块", value = "swagger版块")
public class Demo2Controller {
    @RequestMapping("/swagger")
    @ResponseBody
    @ApiOperation(value = "swagger 测试", httpMethod = "POST", notes = "测试 swagger")
    public Map<String, Object> swagger( @ApiParam(required = true, name = "id", value = "参数")@RequestParam("id")String id){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data","swagger demo");
        return map;
    }
}
```
访问：http://localhost:8080/swagger-ui.html

# 四、使用Lombok简化代码

1. 安装  
**eclipse：**[下载](https://projectlombok.org/)->安装->重启(报错->clean一下项目)  
**IDEA：**setting->plugins->lombok->安装（需要重启）  
**pom.xml 引入 jar**
    ```xml
    <dependencies>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.16.10</version>
        </dependency>
    </dependencies>
    ```

2. Lombok用法
    ```java
    //1. 
    val sets = new HashSet<String>();
        //=>相当于如下
    final Set<String> sets2 = new HashSet<>();
    //2.
    @NonNull
    public void notNullExample(@NonNull String string) {
    string.length();
    }
    //=>相当于
    public void notNullExample(String string) {
    if (string != null) {
        string.length();
    } else {
        throw new NullPointerException("null");
    }
    }
    //3.
    @Cleanup
    public static void main(String[] args) {
        try {
            @Cleanup InputStream inputStream = new FileInputStream(args[0]);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        //=>相当于
        InputStream inputStream = null;
        try {
            inputStream = new FileInputStream(args[0]);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } finally {
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    
    //4. @Getter/@Setter
    @Setter(AccessLevel.PUBLIC)
    @Getter(AccessLevel.PROTECTED)
    private int id;
    private String shap;
    
    //5. @ToString
    @ToString(exclude = "id", callSuper = true, includeFieldNames = true)
    public class LombokDemo {
        private int id;
        private String name;
        private int age;
    
        public static void main(String[] args) {
            //输出LombokDemo(super=LombokDemo@48524010, name=null, age=0)
            System.out.println(new LombokDemo());
        }
    }
    //6.
    @EqualsAndHashCode(exclude = {"id", "shape"}, callSuper = false)
    public class LombokDemo {
        private int id;
        private String shap;
    }
    //7.
    //自动生成无参和所有参数的构造函数以及把所有@NonNull属性作为参数的构造函数，如果指定staticName = “of”参数，同时还会生成一个返回类对象的静态工厂方法
    @NoArgsConstructor
    @RequiredArgsConstructor(staticName = "of")
    @AllArgsConstructor
    public class LombokDemo {
        @NonNull
        private int id;
        @NonNull
        private String shap;
        private int age;
        public static void main(String[] args) {
            new LombokDemo(1, "circle");
            //使用静态工厂方法
            LombokDemo.of(2, "circle");
            //无参构造
            new LombokDemo();
            //包含所有参数
            new LombokDemo(1, "circle", 2);
        }
    }
    //8.
    import lombok.Data;
    @Data
    //同时用@ToString、@EqualsAndHashCode、@Getter、@Setter和@RequiredArgsConstrutor
    public class Menu {
        private String shopId;
        private String skuMenuId;
        private String skuName;
        private String normalizeSkuName;
        private String dishMenuId;
        private String dishName;
        private String dishNum;
        //默认阈值
        private float thresHold = 0;
        //新阈值
        private float newThresHold = 0;
        //总得分
        private float totalScore = 0;
    }
    //在IntelliJ中按下Ctrl+F12就可以看到Lombok已经为我们自动生成了一系列的方法。
    //9.
    @Value
    //为属性添加final声明，只提供getter方法
    public class LombokDemo {
        @NonNull
        private int id;    
        //相当于
        private final int id;
        public int getId() {
            return this.id;
        }
        ...
    }
    //10. 
    @Builder
    //用在类、构造器、方法上
    public class BuilderExample {
        private String name;
        private int age;
        @Singular
        private Set<String> occupations;
        public static void main(String[] args) {
            BuilderExample test = BuilderExample.builder().age(11).name("test").build();
        }
    }
    //11. 
    public class Test {
    //自动抛受检异常，而无需显式在方法上使用throws语句
        @SneakyThrows()
        public void read() {
            InputStream inputStream = new FileInputStream("");
        }    
        //相当于
        public void read() throws FileNotFoundException {
            InputStream inputStream = new FileInputStream("");
        }    
    }
    //12. 
    public class SynchronizedDemo {
    //将方法声明为同步的，并自动加锁，而锁对象是一个私有的属性$lock或$LOCK
        @Synchronized
        public static void hello() {
            System.out.println("world");
        }
        //相当于
        private static final Object $LOCK = new Object[0];
        public static void hello() {
            synchronized ($LOCK) {
                System.out.println("world");
            }
        }
    }
    //13. 
    public class GetterLazyExample {
    @Getter(lazy = true)
    private final double[] cached = expensive();
    private double[] expensive() {
        double[] result = new double[1000000];
        for (int i = 0; i < result.length; i++) {
            result[i] = Math.asin(i);
        }
        return result;
    }
    }
    //14.@Log：根据不同的注解生成不同类型的log对象，但是实例名称都是log，有六种可选实现类
    @CommonsLog Creates log = org.apache.commons.logging.LogFactory.getLog(LogExample.class);
    @Log Creates log = java.util.logging.Logger.getLogger(LogExample.class.getName());
    @Log4j Creates log = org.apache.log4j.Logger.getLogger(LogExample.class);
    @Log4j2 Creates log = org.apache.logging.log4j.LogManager.getLogger(LogExample.class);
    @Slf4j Creates log = org.slf4j.LoggerFactory.getLogger(LogExample.class);
    @XSlf4j Creates log = org.slf4j.ext.XLoggerFactory.getXLogger(LogExample.class);
    ```

# 五、基于拦截器的注解权限控制(springmvc)
1. 添加依赖
```xml
    <dependency>
      <groupId>javax</groupId>
      <artifactId>javaee-api</artifactId>
      <version>7.0</version>
      <scope>provided</scope>
    </dependency>
```
2. 注解文件
```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Domain {
    String value() default "";
}
@Target({ElementType.METHOD,ElementType.TYPE})
// @Target(value={TYPE,FIELD,METHOD,PARAMETER,CONSTRUCTOR,LOCAL_VARIABLE})
@Retention(RetentionPolicy.RUNTIME)//生命周期
@Documented
@Inherited
public @interface AccessAllow {
    String EVERYBODY = "EVERYBODY";
    String PREROGATIVE = "*";
    String[] value() default {};
}
```
3. 注解实现
```java
@Component
public class AccessAllowInterceptor extends HandlerInterceptorAdapter {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        if (handler.getClass().isAssignableFrom(HandlerMethod.class)) {
            HandlerMethod method = (HandlerMethod) handler;
//            Domain domain = method.getMethod().getDeclaringClass().getAnnotation(Domain.class);
            Domain domain =  AnnotationUtils.findAnnotation(method.getBeanType(), Domain.class);
            AccessAllow allow = method.getMethodAnnotation(AccessAllow.class);
            if (allow == null) {
                allow = AnnotationUtils.findAnnotation(method.getBeanType(), AccessAllow.class);
            }
            if(domain!=null){
                System.out.println("domain    "+JSON.toJSONString(domain.value()));
            }
            if(domain!=null){
                System.out.println("allow    "+JSON.toJSONString(allow.value()));
            }
        }
        return true;
    }
}
```
4. 配置拦截器 springmvc-servlet.xml
```xml
    <mvc:interceptors>
        <!-- 国际化操作拦截器 如果采用基于（请求/Session/Cookie）则必需配置 -->
        <bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor" />
        <bean class="com.jun.util.AccessAllowInterceptor"></bean>
    </mvc:interceptors>
```

5. 使用
    ```java
    @Controller
    @RequestMapping("/demo2")
    @Domain("domain")
    @AccessAllow({"cc","dd","ee"})
    public class Demo2Controller {
        @RequestMapping("/AccessAllow")
        @ResponseBody
    //    @AccessAllow({"aa","bb","cc"})
        public Map<String, Object> AccessAllow( String id){
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("state", "success");
            map.put("data","swagger demo");
            return map;
        }
    }
    ```

# 六、 与h2 内存数据库整合
**H2是一个开源的嵌入式内存数据库引擎，用java编写，可兼容一些主流的数据库**
1. 添加依赖pom.xml  
    ```xml
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <version>1.4.193</version>
    </dependency>
    ```
2. 配置文件 h2.properties
``` properties
h2.driver=org.h2.Driver
#嵌入式，持久化存储为单个文件
#h2.url=jdbc:h2:file:~/.h2/quickstart;AUTO_SERVER=TRUE;DB_CLOSE_DELAY=-1
#内存中运行，关闭连接后数据库将被清空
h2.url=jdbc:h2:mem:demo;DB_CLOSE_DELAY=-1
h2.username=root
h2.password=root
#connection pool settings
h2.pool.maxIdle=5
h2.pool.maxActive=40
h2hibernate.dialect=org.hibernate.dialect.H2Dialect
```
3. 在Spring中初始化数据库
``` xml
 <context:property-placeholder ignore-resource-not-found="true"
 location="classpath:/jdbc.properties,classpath:/h2.properties" /> 
    <bean  id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="${h2.driver}"/>
        <property name="url" value="${h2.url}"/>
        <property name="username" value="${h2.username}"/>
        <property name="password" value="${h2.password}"/>
    </bean>
    <!-- 初始化数据表结构 -->
    <jdbc:initialize-database data-source="dataSource" ignore-failures="ALL">
        <jdbc:script location="classpath:h2/H2_TYPE.sql"/>
        <jdbc:script location="classpath:h2/import-data.sql" encoding="UTF-8"/>
    </jdbc:initialize-database>
```
*H2_TYPE.sql设置数据库*
``` sql
SET MODE MySQL;
-- 兼容模式DB2、Derby、HSQLDB、MSSQLServer、MySQL、Oracle、PostgreSQL
-- SET AUTO_RECONNECT=TRUE;
-- --连接丢失后自动重新连接
-- SET AUTO_SERVER=TRUE;
-- --允许开启多个连接，该参数不支持在内存中运行模式
--  SET TRACE_LEVEL_SYSTEM_OUT=2;
-- --输出跟踪日志到控制台
-- SET TRACE_LEVEL_FILE=2;
-- --输出日志到文件，0:OFF，1（默认）:ERROR，2:INFO，3:DEBUG
-- SET TRACE_MAX_FILE_SIZE=16;
-- --设置跟踪日志文件的大小，默认为16M
```
*在create-db.sql中创建表*
*在import-data.sql中导入数据*
```sql
insert into user3 ( select * from csvread('src/test/resources/data.csv') ) ; 
---从MySQL导入数据到H2
insert into user3 AS  ( select * from user2 ) ;
```
*src/test/resources/data.csv*
```csv
"id","name"
"1","名字aa"
"2","名字bb"
"3","名字cc"
```

4. 创建user3
```java
@Entity
@Table
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User3 {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private String name;
    public User3(String name){
        this.name=name;
    }
}
@Repository
public interface User3Dao extends MyRepo<User3, Serializable> {
    User3 findById(Integer id);
    List<User3> findAll();
}
public interface User3Service {
    User3 findById(Integer id);
    User3 save(String name);
    List<User3> findAll();
//    List<User3>  findAllToCopy();
    void save(List<User3> list);
}
@Service
public class User3ServiceImpl implements User3Service {
    @Autowired
    private User3Dao userDao;
    public User3 findById(Integer id) {
        return userDao.findById(id);
    }
    public User3 save(String name) {
        return userDao.save(new User3(name));
    }
    public List<User3> findAll() {
        return userDao.findAll();
    }
    public User3 getUser(Integer id, String name) {
        return null;
    }
//    public List<User3> findAllToCopy() {
//        return mysqlUser3Dao.findAll();
//    }
    public void save(List<User3> list) {
        userDao.save(list);
    }
}
```

**5. 跑测试:**
``` java
@RunWith(SpringJUnit4ClassRunner.class)
@WebAppConfiguration// swagger 需要
@ContextHierarchy({
        @ContextConfiguration(locations = {"classpath*:applicationContext.xml"})
})
@Transactional
public class H2Test{
    @Autowired
    User3Service userService;
    @Test
    public void test(){
        userService.save("hello word");
        System.out.println(userService.findAll());
    }
}
```
swagger 需要
```xml
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>3.0.1</version>
</dependency>
```


## 六、动态数据源（2个mysql）
1.定义DataSource 注解：
``` java
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD,ElementType.TYPE})
public @interface DataSource {
    String value();
}
```
  
2.实现spring抽象类AbstractRoutingDataSource的determineCurrentLookupKey方法：
``` java
public class DynamicDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DynamicDataSourceHolder.getDataSouce();
    }
}


public  class DynamicDataSourceHolder {
    public static final ThreadLocal<String> holder = new ThreadLocal<String>();
    public static void setDataSource(String name) {
        holder.set(name);
    }
    public static String getDataSouce() {
        return holder.get();
    }
    public static void  clearDataSouce() {
       holder.remove();
    }
}
```
 
3.核心（AOP）部分
```java
public class DataSourceAspect {
    public void before(JoinPoint point)      {
        Object target = point.getTarget();
        String method = point.getSignature().getName();
        Class<?>[] classz = target.getClass().getInterfaces();
        Class<?>[] parameterTypes = ((MethodSignature) point.getSignature())
                .getMethod().getParameterTypes();
        try {
            Method m = classz[0].getMethod(method, parameterTypes);
            if(m != null){
                if(m.isAnnotationPresent(DataSource.class)){
                    DataSource data = m.getAnnotation(DataSource.class);
                    DynamicDataSourceHolder.setDataSource(data.value());
                }else if(classz[0].isAnnotationPresent(DataSource.class)){
                 DataSource data = classz[0].getAnnotation(DataSource.class);
                    DynamicDataSourceHolder.setDataSource(data.value());
                }
            }
        } catch (Exception e) {
          //  System.out.println(e.getMessage());
        }
    }
}
```

4.数据库配置：
```xml
<!-- 数据库连接 -->
    <context:property-placeholder location="classpath:jdbc.properties,classpath:h2.properties,classpath:jdbc2.properties" ignore-unresolvable="true"/>
    <!-- 数据源 -->
    <bean id="mysqlDataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource" primary="true">
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>

    <bean id="mysql2DataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource" primary="true">
        <property name="driverClassName" value="${jdbc2.driver}"/>
        <property name="url" value="${jdbc2.url}"/>
        <property name="username" value="${jdbc2.username}"/>
        <property name="password" value="${jdbc2.password}"/>
    </bean>

    <bean id="dataSource" class="com.jun.util.DynamicDataSource">
        <property name="targetDataSources">
            <map key-type="java.lang.String">
                <entry key="mysql" value-ref="mysqlDataSource"/>
                <entry key="mysql2" value-ref="mysql2DataSource"/>
            </map>
        </property>
        <property name="defaultTargetDataSource" ref="mysqlDataSource"/>
    </bean>
    <!-- 配置数据库注解aop -->
    <aop:aspectj-autoproxy></aop:aspectj-autoproxy>
    <bean id="manyDataSourceAspect" class="com.jun.util.DataSourceAspect" />
    <aop:config>
        <aop:aspect id="c" ref="manyDataSourceAspect">
            <aop:pointcut id="tx" expression="execution(* com.jun.dao.*.*(..))"/>
            <aop:before pointcut-ref="tx" method="before"/>
        </aop:aspect>
    </aop:config> 
```

5. 使用：
    在dao的类或者其方法上:使用注解`@DataSource("mysql2")`

### 七、不同库（一个H2、2个mysql）数据源实践
*设置各自库不同的dao（名字一定要不同），spring配置文件的事务、数据源、jpa实体管理工厂等要配置两份*
1. spring 配置文件
```xml
    <!-- 开启IOC注解扫描 -->
    <context:component-scan base-package="com.jun">
        <!-- 排除@controller由springmvc扫描-->
        <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
    </context:component-scan>
    <!-- 数据库连接 -->
    <context:property-placeholder location="classpath:jdbc.properties,classpath:h2.properties,classpath:jdbc2.properties" ignore-unresolvable="true"/>
    <!-- 数据源 -->
    <bean id="mysqlDataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource" primary="true">
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
    <bean id="mysql2DataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="${jdbc2.driver}"/>
        <property name="url" value="${jdbc2.url}"/>
        <property name="username" value="${jdbc2.username}"/>
        <property name="password" value="${jdbc2.password}"/>
    </bean>
    <bean  id="h2DataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="${h2.driver}"/>
        <property name="url" value="${h2.url}"/>
        <property name="username" value="${h2.username}"/>
        <property name="password" value="${h2.password}"/>
    </bean>
  <!--  总数据源-->
    <bean id="dataSource" class="com.jun.util.DynamicDataSource">
        <property name="targetDataSources">
            <map key-type="java.lang.String">
                <entry key="mysql" value-ref="mysqlDataSource"/>
                <entry key="h2" value-ref="h2DataSource"/>
                <entry key="mysql2" value-ref="mysql2DataSource"/>
            </map>
        </property>
        <property name="defaultTargetDataSource" ref="mysqlDataSource"/>
    </bean>
  <!--  mysql数据源-->
    <bean id="dataSourceMysql" class="com.jun.util.DynamicDataSource">
        <property name="targetDataSources">
            <map key-type="java.lang.String">
                <entry key="mysql" value-ref="mysqlDataSource"/>
                <entry key="mysql2" value-ref="mysql2DataSource"/>
            </map>
        </property>
        <property name="defaultTargetDataSource" ref="mysqlDataSource"/>
    </bean>
    <!-- 初始化数据表结构 -->
    <jdbc:initialize-database data-source="h2DataSource" ignore-failures="ALL">
        <jdbc:script location="classpath:h2/H2_TYPE.sql"/>
        <jdbc:script location="classpath:h2/import-data.sql" encoding="UTF-8"/>
    </jdbc:initialize-database>
    <!-- 配置数据库注解aop -->
    <aop:aspectj-autoproxy></aop:aspectj-autoproxy>
    <bean id="manyDataSourceAspect" class="com.jun.util.DataSourceAspect" />
    <aop:config>
        <aop:aspect id="c" ref="manyDataSourceAspect">
            <aop:pointcut id="tx" expression="execution(* com.jun.*.*.*(..))"/>
            <aop:before pointcut-ref="tx" method="before"/>
        </aop:aspect>
    </aop:config>
    <!-- JPA实体管理器工厂 -->
    <bean id="mysqlEntityManagerFactory"
          class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
        <property name="dataSource" ref="dataSourceMysql"/>
        <property name="jpaVendorAdapter" ref="mysqlHibernateVendor"/>
        <property name="packagesToScan" value="com.jun.entity"/>
        <property name="jpaProperties">
            <props>
                <prop key="hibernate.current_session_context_class">thread</prop>
                <prop key="hibernate.hbm2ddl.auto">update</prop><!-- validate/update/create -->
                <prop key="hibernate.show_sql">false</prop>
                <prop key="hibernate.format_sql">false</prop>
                <!-- 建表的命名规则 -->
                <prop key="hibernate.ejb.naming_strategy">org.hibernate.cfg.ImprovedNamingStrategy</prop>
                 <!-- 定义延迟加载-->
                <prop key="hibernate.enable_lazy_load_no_trans">false</prop>
            </props>
        </property>
    </bean>

    <bean id="h2EntityManagerFactory"
          class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
        <property name="dataSource" ref="h2DataSource"/>
        <property name="jpaVendorAdapter" ref="h2HibernateVendor"/>
        <property name="packagesToScan" value="com.jun.entity"/>
        <property name="jpaProperties">
            <props>
                <prop key="hibernate.current_session_context_class">thread</prop>
                <prop key="hibernate.hbm2ddl.auto">update</prop><!-- validate/update/create -->
                <prop key="hibernate.show_sql">false</prop>
                <prop key="hibernate.format_sql">false</prop>
                <!-- 建表的命名规则 -->
                <prop key="hibernate.ejb.naming_strategy">org.hibernate.cfg.ImprovedNamingStrategy</prop>
                 <!-- 定义延迟加载-->
                <prop key="hibernate.enable_lazy_load_no_trans">false</prop>
            </props>
        </property>
    </bean>
    <!-- 设置JPA实现厂商的特定属性 -->
    <bean id="mysqlHibernateVendor" class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter">
        <property name="databasePlatform" value="${hibernate.dialect}"/>
        <property name="generateDdl" value="true"/>
        <property name="database" value="MYSQL"/>
    </bean>
    <bean id="h2HibernateVendor" class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter">
    <property name="databasePlatform" value="${h2hibernate.dialect}"/>
    <property name="generateDdl" value="true"/>
    <property name="database" value="H2"/>
    </bean>
    <!-- Jpa 事务配置 -->
    <bean id="transactionManager" class="org.springframework.orm.jpa.JpaTransactionManager">
        <property name="entityManagerFactory" ref="mysqlEntityManagerFactory"/>
    </bean>
    <bean id="H2transactionManager" class="org.springframework.orm.jpa.JpaTransactionManager">
        <property name="entityManagerFactory" ref="h2EntityManagerFactory"/>
    </bean>
    <!-- Spring Data Jpa配置 -->
    <jpa:repositories factory-class="com.jun.util.MyRepoFactoryBean" base-package="com.jun.dao" transaction-manager-ref="transactionManager" entity-manager-factory-ref="mysqlEntityManagerFactory"/>    
    <jpa:repositories factory-class="com.jun.util.MyRepoFactoryBean" base-package="com.jun.daoH2" transaction-manager-ref="H2transactionManager" entity-manager-factory-ref="h2EntityManagerFactory"/>
    <!-- 使用annotation定义事务 -->
    <tx:annotation-driven transaction-manager="transactionManager" proxy-target-class="true"/>
```
*使用同一份entity，但 dao要做两份，注意添加数据源注解，spring其他配置均为两份，详见上文*
2. dao  
**mysql dao**
``` java
@Repository
public interface MysqlUser3Dao extends JpaRepository<User3, Serializable> {
    User3 findById(Integer id);
    List<User3> findAll();
}
```
**h2 dao**
``` java
@Repository
@DataSource("h2")
public interface User3Dao extends JpaRepository<User3, Serializable> {
    User3 findById(Integer id);
    List<User3> findAll();
}
```
3. service
``` java
public interface User3Service {
    User3 findById(Integer id);
    User3 save(String name);
    List<User3> findAll();
    List<User3>  findAllToCopy();
    void save(List<User3> list);
}
```
User3ServiceImpl
``` java
@Service
public class User3ServiceImpl implements User3Service {
   @Autowired
    private User3Dao userDao;
    @Autowired
    private MysqlUser3Dao mysqlUser3Dao;
    public User3 findById(Integer id) {
        return userDao.findById(id);
    }
    public User3 save(String name) {
        return userDao.save(new User3(name));
    }
    public List<User3> findAll() {
        return userDao.findAll();
    }
    public User3 getUser(Integer id, String name) {
        return null;
    }
    public List<User3> findAllToCopy() {
        return mysqlUser3Dao.findAll();
    }
    public void save(List<User3> list) {
         userDao.save(list);
    }
}
```
4. controller
```java
@Controller
@RequestMapping("/demo3")
public class Demo3Controller {
    @Autowired
    User3Service userService;   
    @RequestMapping("/findall")
    @ResponseBody
    @Transactional
    public Map<String, Object> getUser(){
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data", userService.findAll());
        return map;
    }   
    @RequestMapping("/copy")
    @ResponseBody
    public Map<String, Object> copy(){
        userService.save( userService.findAllToCopy());
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("state", "success");
        map.put("data", userService.findAll());
        map.put("dataCopy", userService.findAllToCopy());
        return map;
    }
}
```

5. **启动服务器**访问：`http://localhost:8080/demo3/findall` -->`http://localhost:8080/demo3/copy`

## 八、Spring启动时初始化函数

``` java
@Component
public class StartAddDataListener  implements ApplicationListener<ContextRefreshedEvent>{    
    public void onApplicationEvent(ContextRefreshedEvent event)  {
        if(event.getApplicationContext().getParent() == null) {
            long a=System.currentTimeMillis();
            //需要执行的逻辑代码，当spring容器初始化完成后就会执行该方法。
            System.out.println("\n\n\n\n\n______\n\n\n加载了\n\n______\n\n");
            System.out.println("\r执行耗时 : "+(System.currentTimeMillis()-a)/1000f+" 秒 "+(System.currentTimeMillis()-a)+"毫秒");
        }
        //或者下面这种方式
        if(event.getApplicationContext().getDisplayName().equals("Root WebApplicationContext")){
            System.out.println("\n\n\n_____\n\n加载一次的 \n\n _____\n\n\n\n");
        }
    }
}
```

## 九、jpa Entity数据变化监控冗

```java
public class User3EntityListener {
    @PrePersist
    public void beforePersist(Object entity) {
        System.out.println("PrePersist :  "+ JSON.toJSONString(entity));
    }

    @PreUpdate
    public void beforeUpdate(Object entity) {
        System.out.println("PreUpdate :  "+ JSON.toJSONString(entity));
    }

    @PreRemove
    public void beforeRemove(Object entity) {
        System.out.println("PreRemove :  "+ JSON.toJSONString(entity));
    }

    @PostPersist
    public void afterPersist(Object entity) {
        System.out.println("PostPersist :  "+ JSON.toJSONString(entity));
    }

    @PostUpdate
    public void afterUpdate(Object entity) {
        System.out.println("PostUpdate :  "+ JSON.toJSONString(entity));
    }

    @PostRemove
    public void afterRemove(Object entity) {
        System.out.println("PostRemove :  "+ JSON.toJSONString(entity));
    }

    @PostLoad
    public void afterLoad(Object entity) {
        System.out.println("PostLoad :  "+ JSON.toJSONString(entity));
    }

}

```

使用在User3 上添加注解: `@EntityListeners({User3EntityListener.class})` 

## 十、dataJpa 复杂查询
1. repo文件添加 @Query 注解
*nativeQuery = true 使用数据库原生表*
```java
  @Query("SELECT MAX(o.archiveNo) FROM StaffArchiveEntity o WHERE o.archiveNo LIKE ?1 AND LENGTH(o.archiveNo) <= 12 AND o.valid = true")
    String getMaxArchiveNo(String prefix);
 @Query(value = "select d.label from dictionary d where d.groupType = 'CYZGLB_D' and d.code in ?1",nativeQuery = true)
    List<String> getQualificationStr(String[] code);
```

2. 使用entityManager.createNativeQuery
```java
   public AllOwnerQueryReturn findOwner(AllOwnerparam param) {
        List<Specification<OwnerEntity>> lst = new ArrayList<>();
        StringBuffer sql = new StringBuffer();
        String sqlB = "select o.id,o.name from owner o left join archive oa on o.ownerId = oa.ownerId where 1 = 1 ";
        sql.append(sqlB);
        if (param != null) {
            if (param.getName()!=null&&!"".equals(param.getName())) {
                sql.append(" and o.ownerName like '%" + param.getOwnerName() + "%'");
                //long time1 = DateConvert.toMillis(param.getTimeStart());
            }
            if (param.getAreaCode() != null && param.getAreaCode().length > 0){
                sql.append(" and o.mgmtAreaCode in ( ");
                for(var i =0;i<param.getAreaCode().length;i++){
                sql.append(param.getAreaCode()[i]).append(i==(param.getAreaCode().length-1)?"":",");
                sql.append(" ) ");
                }
            }          
        }       
        String sqlCount = "select count(distinct a.id) from (" + sql.toString() + ") as a";
        sql.append(" limit " + param.getPageNum() * param.getPageSize() + "," + param.getPageSize());
        Query qCount = entityManager.createNativeQuery(sqlCount.toString());
        Query q = entityManager.createNativeQuery(sql.toString());
        List<Object[]> list = q.getResultList();
        int pageNum = param.getPageNum();
        int pageSize = param.getPageSize();
        int totalRecords = ((BigInteger) qCount.getSingleResult()).intValue();
        int remainder = totalRecords % pageSize;
        //int totalPages = totalRecords % pageSize == 0 ? (totalRecords / pageSize) : (totalRecords / pageSize + 1);  
        int totalPages =(int)math.ceil(totalRecords % pageSize);
        AllOwnerQueryReturn data = new AllOwnerQueryReturn();
        data.setPageNum(pageNum + 1);
        data.setPageSize(pageSize);
        data.setTotalPages(totalPages);
        data.setTotalRecords(totalRecords);
        data.setAlList(list);
        return data;
    }
```
3. Criteria 查询：是一种类型安全和更面向对象的查询，
接口是JpaSpecificationExecutor
```java
 @Transactional
    public Page<EasT1Term> dynamicFind(EasT1Term term,Pageable pageable) {
        Page<EasT1Term> result = termRepository.findAll(new Specification<EasT1Term>() {
            public Predicate toPredicate(Root<EasT1Term> root, CriteriaQuery<?> query, CriteriaBuilder cb) {
                List<Predicate> list = new ArrayList<>();
                 //大于等于
                if (StringUtils.isNotBlank(term.getYearStart())) {
                    list.add(cb.greaterThanOrEqualTo(root.get("yearStart").as(String.class),term.getYearStart()));
                }
                //小于等于
                if (StringUtils.isNotBlank(term.getYearEnd())) {
                    list.add(cb.lessThanOrEqualTo(root.get("yearEnd").as(Date.class), DateUtils.getDateWithLastSecond(term.getYearEnd())));
                }
                // list.add(cb.between(root.<String>get("yearEnd"), term.getYearStart(), term.getYearStart()));
                 //等于
                if (StringUtils.isNotBlank(term.getStatus())) {
                    list.add(cb.equal(root.get("status").as(String.class), term.getStatus()));
                }
               // null notNull
            list.add(cb.isNull(root.get("name")));
            list.add(cb.isNotNull(root.get("name")));
                // like
            if (StringUtils.isNotBlank( term.getName())) {
                    list.add(cb.like(root.get("name").as(String.class), "%" +  term.getName() + "%"));
                }
            //or 查询
            list.add( cb.or(cb.like(root.<String>get("name"), term.getName()),
                       cb.like(root.<String>get("name"), term.getName())));
            //忽略大小写(全大写)
            list.add(cb.like(cb.upper(root.get(term.getName)), StringUtils.upperCase(StringUtils.trim(term.getName())) + "%"));            
             //in
            list.add(scheduleRequest.get("createdBy").in(list));            
            // not in
            list.add(Restrictions.not(Restrictions.in("id", callbackIds)));
            //两表连接
            Join<EasT1Term, EasT1Term> joinTable = root.join("table2");
            list.add(cb.equal(joinTable.get("id").as(Boolean.class), true));
            list.add(cb.equal(root.fetch(table2.id, JoinType.LEFT))); 
            //排序
            query.orderBy(cb.desc(root.get("updateTime")), cb.desc(root.get("createTime")));
            Predicate[] predicates = new Predicate[list.size()];
            predicates = list.toArray(predicates);
            return cb.and(predicates);
            }
        }, pageable);
        return result;
    }
```
3.1 作为工具类 拆分
```java
public class BetweenSpecification<T, ATTR extends Comparable<ATTR>> implements Specification<T> {
    private String attrName;
    private ATTR lowerBound, upperBound;
    public BetweenSpecification(String attrName, ATTR lowerBound, ATTR upperBound) {
        super();
        this.attrName = attrName;
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
    }
    @Override
    public Predicate toPredicate(Root<T> root, CriteriaQuery<?> query, CriteriaBuilder cb) {
        Path<ATTR> path = SpecificationHelper.getPath(root, attrName);
        return cb.between(path, lowerBound, upperBound);
    }
}
```
4. 使用EntityManager
```java
    @Inject
    EntityManager em; 
    CriteriaBuilder cb = em.getCriteriaBuilder();
    CriteriaQuery<Qfsqmx> q = cb.createQuery(Qfsqmx.class);
    Root<Qfsqmx> root = q.from(Qfsqmx.class);
    List<Predicate> predicate = new ArrayList<>();
    //in条件拼接
    In<String> in = cb.in(root.get("qfsqid").as(String.class));
    for (int i = 0; i < list.size(); i++) {
        in.value(list.get(i).getId());
    }
   //设定select字段
    q.multiselect(
        root.get("qfmc"),
        root.get("qfcc"),
        root.get("jldw"),
        cb.sum(root.get("sl").as(Integer.class))
    );
    predicate.add(in);
    //predicate.add(exp.in(list));
    //设定where条件
    q.where(predicate.toArray(new Predicate[predicate.size()]));
//  query.where(cb.and(p3,cb.or(p1,p2))); 
    //设定groupby条件
    q.groupBy(
        root.get("qflxid").as(String.class),
        root.get("qfccid").as(String.class),
        root.get("qfmc").as(String.class),
        root.get("qfcc").as(String.class),
        root.get("jldw").as(String.class)
    );
     q.having(q.like(root.get("name"), "N%"));
 //设定orderby条件
     q.orderBy(q.asc(root.get(root_.age).as(Integer.class)));
    List<Qfsqmx> rs = em.createQuery(q).getResultList();
    return rs;
}
```

## 十一、基于拦截器打印（修改）sql语句

1. Sql.java
```java
@Component("Sql")
public class Sql extends EmptyInterceptor {
    public Sql(){ }
    public Sql(Date startTime, Date endTime){ }
    @Override
    public String onPrepareStatement(String sql) {
//        修改sql
        System.err.println("statement..............");
        System.err.println(sql);
        return super.onPrepareStatement(sql);
    }
    @Override
    public void onDelete(Object entity, Serializable id, Object[] state,
                         String[] propertyNames, Type[] types) {
        System.err.println("delete..............");
        System.err.println("entity :   "+ JSON.toJSONString(entity));
        System.err.println("id :   "+ JSON.toJSONString(id));
        System.err.println("state :   "+ JSON.toJSONString(state));
        System.err.println("propertyNames :   "+ JSON.toJSONString(propertyNames));
        System.err.println("types :   "+ JSON.toJSONString(types));
        super.onDelete(entity, id, state, propertyNames, types);
    }
    @Override
    public boolean onFlushDirty(Object entity, Serializable id,
                                Object[] currentState, Object[] previousState,
                                String[] propertyNames, Type[] types) {
        System.err.println("flushDirty..............");
        System.err.println("entity :   "+ JSON.toJSONString(entity));
        System.err.println("id :   "+ JSON.toJSONString(id));
        System.err.println("currentState :   "+ JSON.toJSONString(currentState));
        System.err.println("previousState :   "+ JSON.toJSONString(previousState));
        System.err.println("propertyNames :   "+ JSON.toJSONString(propertyNames));
        System.err.println("types :   "+ JSON.toJSONString(types));
        return super.onFlushDirty(entity, id, currentState, previousState,
                propertyNames, types);
    }
    @Override
    public boolean onSave(Object entity, Serializable id, Object[] state,
                          String[] propertyNames, Type[] types) {
        System.err.println("save..............");
        System.err.println("entity :   "+ JSON.toJSONString(entity));
        System.err.println("id :   "+ JSON.toJSONString(id));
        System.err.println("state :   "+ JSON.toJSONString(state));
        System.err.println("propertyNames :   "+ JSON.toJSONString(propertyNames));
        System.err.println("types :   "+ JSON.toJSONString(types));
        return super.onSave(entity, id, state, propertyNames, types);
    }
    @Override
    public void onCollectionRecreate(Object collection, Serializable key)
            throws CallbackException {
        System.err.println("recreate..............");
        System.err.println("collection :   "+ JSON.toJSONString(collection));
        System.err.println("key :   "+ JSON.toJSONString(key));
        super.onCollectionRecreate(collection, key);
    }
    @Override
    public void onCollectionRemove(Object collection, Serializable key)
            throws CallbackException {
        System.err.println("remove..............");
        System.err.println("collection :   "+ JSON.toJSONString(collection));
        System.err.println("key :   "+ JSON.toJSONString(key));
        super.onCollectionRemove(collection, key);
    }
    @Override
    public void onCollectionUpdate(Object collection, Serializable key)
            throws CallbackException {
        System.err.println("collectionUpdate..............");
        System.err.println("collection :   "+ JSON.toJSONString(collection));
        System.err.println("key :   "+ JSON.toJSONString(key));
        super.onCollectionUpdate(collection, key);
    }
    @Override
    public boolean onLoad(Object entity, Serializable id, Object[] state,
                          String[] propertyNames, Type[] types) {
        System.err.println("load..............");
        System.err.println("entity :   "+ JSON.toJSONString(entity));
        System.err.println("id :   "+ JSON.toJSONString(id));
        System.err.println("state :   "+ JSON.toJSONString(state));
        System.err.println("propertyNames :   "+ JSON.toJSONString(propertyNames));
        System.err.println("types :   "+ JSON.toJSONString(types));
        return super.onLoad(entity, id, state, propertyNames, types);
    }
    @Override
    public void postFlush(Iterator entities) {
        System.err.println("flush..............");
        System.err.println("types :   "+ JSON.toJSONString(entities));
        super.postFlush(entities);
    }
    @Override
    public void preFlush(Iterator entities) {
        System.err.println("preflush..............");
        System.err.println("types :   "+ JSON.toJSONString(entities));
        super.preFlush(entities);
    }
}
```

2. 注入 applicationContext.xml
   ```xml
    <!-- JPA实体管理器工厂 -->
     <bean id="entityManagerFactory" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">       
           <property name="jpaProperties">
               <props>
                   <!-- 逻辑处理拦截器 -->
                   <prop key="hibernate.ejb.interceptor">com.jun.utils.Sql</prop>
               </props>
           </property>
       </bean>
   ```


