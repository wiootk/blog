---
layout: post
title:  "springCloud集成SSM"
date:   2018-01-06
desc: "springCloud集成SSM"
keywords: "后端,springCloud,微服务,mybaties,springMVC"
categories: [Back]
tags: [后端,springCloud,微服务,mybaties,springMVC]
icon: icon-java
---
springCloud集成SSM：其中mybaties为全注解式开发
# 基础工程

1. pom.xml
   ```xml
   <artifactId>demo_ssm</artifactId>
   <packaging>war</packaging>
   <name>ssm</name>
   <dependencies>
       <!-- mybatis分页插件 -->
       <dependency>
           <groupId>com.github.pagehelper</groupId>
           <artifactId>pagehelper-spring-boot-starter</artifactId>
           <version>1.1.1</version>
       </dependency>
       <!-- 数据库 -->
       <dependency>
           <groupId>mysql</groupId>
           <artifactId>mysql-connector-java</artifactId>
           <version>6.0.6</version>
       </dependency>
       <!-- freemarker -->
       <dependency>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-freemarker</artifactId>
       </dependency>
       <dependency>
           <groupId>com.alibaba</groupId>
           <artifactId>fastjson</artifactId>
           <version>1.2.44</version>
       </dependency>
       <dependency>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-aop</artifactId>
       </dependency>
   </dependencies>
   ```

2. 应用主类 SSMApplication.java
```java
@SpringBootApplication
//@ComponentScan("com.jun")  //扫描下面的包@service @controller 等
//@MapperScan("com.jun.mapper")  //扫面下面的mapper类
public class SSMApplication {
    public static void main(String[] args) {
        SpringApplication.run(SSMApplication.class, args);
    }
}
```

3. 配置文件 application.properties
```properties
spring.application.name=ssm
server.port=8002
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
spring.datasource.url=jdbc:mysql://127.0.0.1:3306/demo3?serverTimezone=UTC&characterEncoding=utf8&useUnicode=true&useSSL=false
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name= com.mysql.cj.jdbc.Driver
spring.datasource.max-active=20
spring.datasource.max-idle=8
spring.datasource.min-idle=8
spring.datasource.initial-size=10
#将数据库的NN_NN格式字段，在java结果集对象中自动转换成驼峰命名参数
mybatis.configuration.mapUnderscoreToCamelCase=true
logging.level.com.jun=debug
## springMvc视图
#设定静态文件路径，js,css等
spring.mvc.static-path-pattern=/static/**
#spring.mvc.view.prefix=/templates/
#spring.mvc.view.suffix=.ftl
spring.freemarker.allow-request-override=false
spring.freemarker.cache=true
spring.freemarker.check-template-location=true
spring.freemarker.charset=UTF-8
spring.freemarker.content-type=text/html
spring.freemarker.expose-request-attributes=false
spring.freemarker.expose-session-attributes=false
spring.freemarker.expose-spring-macro-helpers=false
#spring.freemarker.prefix=
spring.freemarker.suffix=.ftl
spring.freemarker.template-loader-path=classpath:/templates
spring.freemarker.order=1
#spring.freemarker.request-context-attribute=
#spring.freemarker.settings.*=
#spring.freemarker.view-names= #whitelistofviewnamesthatcanberesolved
# 打印日志
logging.level.root= INFO
logging.level.org.hibernate= INFO
logging.level.org.hibernate.type.descriptor.sql.BasicBinder= TRACE
logging.level.org.hibernate.type.descriptor.sql.BasicExtractor=TRACE
logging.level.com.springms=DEBUG
#Swagger2
eureka.instance.status-page-url=http://localhost:${server.port}/swagger-ui.html
```

## SSM集成

1. mybaties的配置文件 MyBatisConfiguration.java
```java
@Configuration
public class MyBatisConfiguration {
    @Bean
    public PageHelper pageHelper() {
        System.out.println("MyBatisConfiguration.pageHelper()");
        PageHelper pageHelper = new PageHelper();
        Properties p = new Properties();
        p.setProperty("offsetAsPageNum", "true");
        p.setProperty("rowBoundsWithCount", "true");
        p.setProperty("reasonable", "true");
        pageHelper.setProperties(p);
        return pageHelper;
    }
}
```

2. com.jun.entity 实体 
```java
public class User {
    private long id;
    private String name;
    private int age;
    public User() {  }
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
// 省略 get/set ...
}
```

3. com.jun.mapper.provider 动态sql  
本例使用`\{\{` 代表双括号，使用时请去掉  
```java
public class UserDaoProvider {
    public String findUserById(User user) {
        String sql = "SELECT * FROM user";
        if(user.getId()!=0){
            sql += " where id = #{id}";
        }
        return sql;
    }
    public String findUser(User user) {
        return new SQL()\{\{
            SELECT("id,name");
            SELECT("other");
            FROM("user");
            if(user.getId()!=0){
                WHERE("id = #{id}");
            }
            if(user.getName()!=null){
                WHERE("name = #{name}");
            }
        }}.toString();
    }
    public String find(Map map) {
        List<User> list = (List<User>) map.get("list");
        return new SQL()\{\{
            SELECT("id,name");
            SELECT("other");
            FROM("user");
            StringBuilder ids=new StringBuilder();
            ids.append(" ( ");
            for(User u:list){
                ids.append("#{id} ,");
            }
            if(ids.lastIndexOf(",")>1){
                ids.subSequence(0,ids.length()-1);
                ids.append(" )");
                WHERE("id in "+ids.toString());
            }
        }}.toString();
    }
}
```

4. com.jun.mapper 相当于DAO 
```java
@Mapper
public interface UserMapper {
    @Delete("drop table user if exists")
    void dropTable();
    @Insert("create table user (id bigint generated by default as identity, age integer, name varchar(255), primary key (id))")
    void createTable();
    //三种传参方式
    @Insert("insert into user(name,age) values(#{name},#{age})")
//    id递增，回传ID
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    long insert(User user);
    @Insert("insert into user(name,age) values(#{name},#{age})")
    int insertByParm(@Param("name") String name, @Param("age") String age);
    @Insert("insert into user(name,age) values(#{name, jdbcType=VARCHAR}, #{age, jdbcType=INTEGER})")
    int insertByMap(Map<String, Object> map);
    @Select("select id,name,age from user")
    List<User> findAll();
    //使用UserDaoProvider类的findUser方法来生成动态sql
    @SelectProvider(type = UserDaoProvider.class, method = "findUser")
    List<User> findAll2(User user);
    //动态sql的List参数处理
    @SelectProvider(type = UserDaoProvider.class, method = "find")
    public List<Map> findAll3(List<User> list);
    @Select("select id,name,age from user where name like #{name}")
    List<User> findByNameLike(String name);
//    @Results(id="userResp",value={
//            @Result(property="nnNn",column="NN_NN")
//    })
//////    在其他方法重复使用
////    @ResultMap("userResp")
    //返回结果处理
    @Results({
//            @Result(property = "id", column = "ID"),
            @Result(property = "name", column = "NAME"),
            @Result(property = "age", column = "AGE")
    })
    @Select("select id, name,age from user where id = #{id}")
    User getById(long id);
    @Delete("delete from user")
    void deleteAll();
}
```

5. com.jun.service
```java
@Service
public class UserService {
    @Autowired
    private UserMapper mapper;
    public List<User> likeName(String name){
        return mapper.findByNameLike(name);
    }
    public long save(User user){
        return mapper.insert(user);
    }
    public User getById(long id){
        return mapper.getById(id);
    }
}
```

6. com.jun.controller
```java
@Controller
public class UserController {
    @Autowired
    private UserService service;
    //    http://localhost:8002/testError
    @GetMapping("/testError")
    public void testError() {
        int i = 1 / 0;
    }
//    http://localhost:8002/find/name
    @GetMapping("/find/{name}")
    @ResponseBody
    public PageInfo<User> likeName(@PathVariable(value="name")String name) {
        PageHelper.startPage(1, 2);
        List<User> list=service.likeName("%"+name+"%");
        PageInfo<User> p=new PageInfo<User>(list);
        return  p;
    }
    //    http://localhost:8002/save {"name":"test","age":10}
    @PostMapping("/save")
    public ModelAndView save(@RequestBody User user) {
        ModelAndView model = new ModelAndView();
        service.save(user);
        model.addObject("user", service.getById(user.getId()));
        model.setViewName("userInfo");
        return model;
    }
//    http://localhost:8002/getById/1
    @RequestMapping("/getById/{id}")
    public String getById(Model model,@PathVariable(value="id")Integer id) {
        model.addAttribute("user", service.getById(id));
        return "userInfo";
    }
}
```

7. 启动程序访问
`http://localhost:8002/getById/1`  
`http://localhost:8002/find/name`  
`http://localhost:8002/save` 参数`{"name":"test","age":10}`  

## 全局异常处理
**utils下为工具类**  
```java
@ControllerAdvice
//全局异常处理
public class ErrorController {
    private static final Logger log = LoggerFactory.getLogger(ErrorController.class);
    class ErrorMag{
        private String code;
        private String message;
        private String exception;
        private String  time;
        public String DateConver(Long time){
            if(time!=null&&time==0){
                time=System.currentTimeMillis();
            }
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date date = new Date(time);
            return simpleDateFormat.format(date);
        }
        public String DateConver(){
           return DateConver(System.currentTimeMillis());
        }
        public ErrorMag( String code,String message,Exception e){
            this.code=code;
            this.message=message;
            this.exception=e.getMessage();
            this.time= DateConver();
        }
        public void setTime(long time) {
            this.time = DateConver(time);
        }
        public void setTime() {
            this.time = DateConver();
        }
    //    省略 set/get ...
    }
    //捕获除0异常
    @ExceptionHandler(ArithmeticException.class)
    @ResponseBody
    public ErrorMag exception1(ArithmeticException e){
        System.out.println("处理除0异常");
//        //继续抛出异常，才能被logback的error级别日志捕获
//        throw e;
        return new ErrorMag("001","处理除0异常", e);
    }
    //捕获空指针异常
    @ExceptionHandler(NullPointerException.class)
    public String exception2(NullPointerException e){
        System.out.println("处理空指针异常");
        //手动将异常写入logback的error级别日志
        log.error("空指针异常",e);
        return "/null.html";
    }
}
```
启动程序访问`http://localhost:8002/testError`  

## aop实现日志管理
1. 定义注解
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Log {
    String[] value() default {};
    String desc() default "";
    String func() default "";
    String type() default "001";
}
```
2. 编写切片AOP
```java
@Component
@Aspect
public class LogAspect {
    private static final Logger logger = LoggerFactory.getLogger(AccessInterceptor.class);
    @Pointcut(value = "@annotation(com.jun.utils.Log)")
    public void log() {
    }
    @Before("log()")
    public void deBefore(JoinPoint joinPoint) throws Throwable {
        // 接收到请求，记录请求内容
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes.getRequest();
        // 记录下请求内容
        logger.error("URL : {}\r\nHTTP_METHOD :{}\r\nIP : {}\r\nCLASS_METHOD :{}\r\nARGS :{}\r\n", request.getRequestURL().toString(),
                request.getMethod(), request.getRemoteAddr(), (joinPoint.getSignature().getDeclaringTypeName() + "." + joinPoint.getSignature().getName()),
                JSON.toJSONString(joinPoint.getArgs()));
    }
    @AfterReturning(returning = "ret", pointcut = "log()")
    public void doAfterReturning(Object ret) throws Throwable {
        // 处理完请求，返回内容
        logger.error("方法的返回值 : {}", ret);
    }
    //后置异常通知
    @AfterThrowing("log()")
    public void throwss(JoinPoint jp) {
        logger.error("方法异常时执行.....");
    }
    //后置最终通知,final增强，不管是抛出异常或者正常退出都会执行
    @After("log()")
    public void after(JoinPoint jp) {
        logger.error("方法最后执行.....");
    }
    //环绕通知,环绕增强，相当于MethodInterceptor
    @Around("@annotation(log)")
    public Object arround(ProceedingJoinPoint pjp, Log log) {
        logger.error("注解里的值:\r\n 描述：{}\r\n功能：{} \r\n类型：{}", log.desc(), log.func(), log.type());
        try {
            Object o = pjp.proceed();
            logger.error("方法环绕proceed，结果是 :" + o);
            return o;
        } catch (Throwable throwable) {
            throwable.printStackTrace();
            return null;
        }
    }
}
```
3. 使用
```java
@Log(desc="日志测试",func="功能",type="002")
```

## 自定义注解进行权限控制
说明：`模块和方法上的注解合并组成可访问的权限列表`  
1. 定义模块注解,写在类上
```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface AccessModule {
    String[] value() default {};
    String[] module() default {};
    String desc() default "";
}
```
2. 定义方法注解，写在方法上
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Access {
    String[] value() default {};
    String[] roles() default {};
    String[] powers() default {};
    String[] absPowers() default {};
    String desc() default "";
}
```
3. 注解的处理类
```java
@Component
public class AccessInterceptor extends HandlerInterceptorAdapter {
    private static final Logger log = LoggerFactory.getLogger(AccessInterceptor.class);
    // 在调用方法之前执行拦截
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String moduleDesc = "";
        List<String> modules = new ArrayList<>();
        String methodDesc = "";
        List<String> roles = new ArrayList<>();
        List<String> powers = new ArrayList<>();
        List<String> absPowers = new ArrayList<>();
        // 将handler强转为HandlerMethod
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        // 从方法处理器中获取所在的类
        Class clazz = handlerMethod.getBeanType();
        if (clazz.isAnnotationPresent(AccessModule.class)) {
            //类上的权限
            AccessModule pAccess = (AccessModule) clazz.getAnnotation(AccessModule.class);
            log.error("类权限的描述：{},模块：{}", pAccess.desc(), pAccess.module());
            moduleDesc = pAccess.desc();
            modules = Arrays.asList(pAccess.module());
        }
        // 从方法处理器中获取出要调用的方法
        Method method = handlerMethod.getMethod();
        // 获取出方法上的Access注解
        Access access = method.getAnnotation(Access.class);
        if (access == null) {
            // 如果注解为null, 说明不需要拦截, 直接放过
            return true;
        }
        log.error("方法权限的描述：{},角色：{},权限:{},绝对权限:{}", access.desc() , access.roles(), access.powers(), access.absPowers());
        methodDesc = access.desc();
        roles = Arrays.asList(access.roles());
        powers = Arrays.asList(access.powers());
        absPowers = Arrays.asList(access.absPowers());
        Set<String> powerSet = new HashSet<>();
        if (powers.size() > 0) {
            if (modules.size() > 0) {
                for (String module : modules) {
                    for (String power : powers) {
                        powerSet.add(module + "." + power);
                    }
                }
            } else {
                for (String power : powers) {
                    powerSet.add(power);
                }
            }
        }
        if (absPowers.size() > 0) {
            for (String power : absPowers) {
                powerSet.add(power);
            }
        }
        String desc = methodDesc;
        if (!StringUtils.isEmpty(moduleDesc)) {
            desc = moduleDesc + "(" + desc + ")";
        }
        log.error("权限描述：{},角色：{},权限:{}",desc,JSON.toJSONString(roles), JSON.toJSONString(powerSet));
        // 拦截之后应该返回公共结果, 这里没做处理
        return true;
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,ModelAndView modelAndView) throws Exception {
        log.debug(">>>>>>>请求处理之后进行调用，但是在视图被渲染之前（Controller方法调用之后）");

    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
            throws Exception {
        log.debug(">>>>>>>在整个请求结束之后被调用，也就是在DispatcherServlet 渲染了对应的视图之后执行（主要是用于进行资源清理工作）");
    }
}
```
4. 在controller上使用
```java
@Controller
@AccessModule(module = {"module"},desc="类的描述")
public class UserController {
    @GetMapping("/find/{name}")
    @ResponseBody
    @Access(roles = {"角色"},powers = {"power"},desc="方法的描述",absPowers={"absPowers"})
    public PageInfo<User> likeName(@PathVariable(value="name")String name) {    }
    @PostMapping("/save")
    @Access(roles = {"角色"},powers = {"power"},desc="方法的描述",absPowers={"absPowers"})
    public ModelAndView save(@RequestBody User user) {}
}
```

5. 启动程序并访问,查看控制台信息

## 获取某包下所有的注解及其值
例子：`获取所有的权限`  

1. 工具类
```java
public class GetApi<Ann,PAnn> {
    private static final Logger log = LoggerFactory.getLogger(GetApi.class);
    public static Set<Class<?>> getClasses(String pack) {
        // 第一个class类的集合
        Set<Class<?>> classes = new LinkedHashSet<Class<?>>();
        // 是否循环迭代
        boolean recursive = true;
        // 获取包的名字 并进行替换
        String packageName = pack;
        String packageDirName = packageName.replace('.', '/');
        // 定义一个枚举的集合 并进行循环来处理这个目录下的things
        Enumeration<URL> dirs;
        try {
            dirs = Thread.currentThread().getContextClassLoader().getResources(
                    packageDirName);
            // 循环迭代下去
            while (dirs.hasMoreElements()) {
                // 获取下一个元素
                URL url = dirs.nextElement();
                // 得到协议的名称
                String protocol = url.getProtocol();
                // 如果是以文件的形式保存在服务器上
                if ("file".equals(protocol)) {
                    // 获取包的物理路径
                    String filePath = URLDecoder.decode(url.getFile(), "UTF-8");
                    // 以文件的方式扫描整个包下的文件 并添加到集合中
                    findAndAddClassesInPackageByFile(packageName, filePath,
                            recursive, classes);
                } else if ("jar".equals(protocol)) {
                    // 如果是jar包文件
                    // 定义一个JarFile
                    System.err.println("jar类型的扫描");
                    JarFile jar;
                    try {
                        // 获取jar
                        jar = ((JarURLConnection) url.openConnection())
                                .getJarFile();
                        // 从此jar包 得到一个枚举类
                        Enumeration<JarEntry> entries = jar.entries();
                        // 同样的进行循环迭代
                        while (entries.hasMoreElements()) {
                            // 获取jar里的一个实体 可以是目录 和一些jar包里的其他文件 如META-INF等文件
                            JarEntry entry = entries.nextElement();
                            String name = entry.getName();
                            // 如果是以/开头的
                            if (name.charAt(0) == '/') {
                                // 获取后面的字符串
                                name = name.substring(1);
                            }
                            // 如果前半部分和定义的包名相同
                            if (name.startsWith(packageDirName)) {
                                int idx = name.lastIndexOf('/');
                                // 如果以"/"结尾 是一个包
                                if (idx != -1) {
                                    // 获取包名 把"/"替换成"."
                                    packageName = name.substring(0, idx)
                                            .replace('/', '.');
                                }
                                // 如果可以迭代下去 并且是一个包
                                if ((idx != -1) || recursive) {
                                    // 如果是一个.class文件 而且不是目录
                                    if (name.endsWith(".class")
                                            && !entry.isDirectory()) {
                                        // 去掉后面的".class" 获取真正的类名
                                        String className = name.substring(
                                                packageName.length() + 1, name
                                                        .length() - 6);
                                        try {
                                            // 添加到classes
                                            classes.add(Class
                                                    .forName(packageName + '.'
                                                            + className));
                                        } catch (ClassNotFoundException e) {
                                            // log
                                            // .error("添加用户自定义视图类错误 找不到此类的.class文件");
                                            e.printStackTrace();
                                        }
                                    }
                                }
                            }
                        }
                    } catch (IOException e) {
                 // log.error("在扫描用户定义视图时从jar包获取文件出错");
                        e.printStackTrace();
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return classes;
    }
    // 以文件的形式来获取包下的所有Class
    public static void findAndAddClassesInPackageByFile(String packageName,String packagePath, final boolean recursive, Set<Class<?>> classes) {
        // 获取此包的目录 建立一个File
        File dir = new File(packagePath);
        // 如果不存在或者 也不是目录就直接返回
        if (!dir.exists() || !dir.isDirectory()) {
            // log.warn("用户定义包名 " + packageName + " 下没有任何文件");
            return;
        }
        // 如果存在 就获取包下的所有文件 包括目录
        File[] dirfiles = dir.listFiles(new FileFilter() {
            // 自定义过滤规则 如果可以循环(包含子目录) 或则是以.class结尾的文件(编译好的java类文件)
            public boolean accept(File file) {
                return (recursive && file.isDirectory())
                        || (file.getName().endsWith(".class"));
            }
        });
        // 循环所有文件
        for (File file : dirfiles) {
            // 如果是目录 则继续扫描
            if (file.isDirectory()) {
                findAndAddClassesInPackageByFile(packageName + "."
                                + file.getName(), file.getAbsolutePath(), recursive,
                        classes);
            } else {
                // 如果是java类文件 去掉后面的.class 只留下类名
                String className = file.getName().substring(0,
                        file.getName().length() - 6);
                try {
                    // 添加到集合中去
                    //classes.add(Class.forName(packageName + '.' + className));
                    //经过回复同学的提醒，这里用forName有一些不好，会触发static方法，没有使用classLoader的load干净
                    classes.add(Thread.currentThread().getContextClassLoader().loadClass(packageName + '.' + className));
                } catch (ClassNotFoundException e) {
                    // log.error("添加用户自定义视图类错误 找不到此类的.class文件");
                    e.printStackTrace();
                }
            }
        }
    }
public   void  getApis(Class javaClass,Class AnnClass,Class PAnnClass){
        if(PAnnClass!=null){
            // 从方法处理器中获取所在的类
            if (javaClass.isAnnotationPresent(AccessModule.class)) {
                //类上的权限
                PAnn pAccess = (PAnn) javaClass.getAnnotation(AccessModule.class);
                log.error("类注解：{}",JSON.toJSONString(pAccess));
            }
        }
        Method[] methods =javaClass.getMethods();
        for (Method method : methods) {
            // 获取出方法上的Access注解
            Access access = method.getAnnotation(Access.class);
            if(access==null){
                continue;
            }
            log.error("方法注解：{}",JSON.toJSONString(access));
            log.error("参数：{}",JSON.toJSONString(method.getGenericParameterTypes()));
            log.error("返回值：{}",JSON.toJSONString(method.getGenericReturnType()));
            GetMapping getMapping = method.getAnnotation(GetMapping.class);
            if(getMapping!=null){
                log.error("请求地址：{}",JSON.toJSONString(getMapping));
            }
            PostMapping postMapping = method.getAnnotation(PostMapping.class);
            if(postMapping!=null){
                log.error("请求地址：{}",JSON.toJSONString(postMapping));
            }
        }
    }
}
```

2. 测试
```java
public class Tests {
    public static void main(String[] args) {
        GetApi<Access,AccessModule> api=new GetApi();
        Set<Class<?>> classSet= api.getClasses("com.jun.controller");
        for(Class cla:classSet){
            api.getApis(cla,Access.class,AccessModule.class);
        }
    }
}
```







