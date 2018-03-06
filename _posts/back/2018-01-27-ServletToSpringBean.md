---
layout: post
title:  "将Servlet转为Spring管理的Servlet Bean"
date:   2018-01-27
desc: "将Servlet转为Spring管理的Servlet Bean"
keywords: "后端,Servlet,Spring"
categories: [Back]
tags: [后端,Servlet,Spring]
icon: icon-java
---
1. web.xml
   ```xml
   <servlet>
       <servlet-name>XB0101SendServlet</servlet-name>
       <servlet-class>
           com.jun.ServletToBeanProxy
       </servlet-class>
       <load-on-startup>1</load-on-startup>
   </servlet>
   <servlet-mapping>
       <servlet-name>XB0101SendServlet</servlet-name>
       <url-pattern>/XB0101Send</url-pattern>
   </servlet-mapping>
   ```

2. 代理类ServletToBeanProxy
   ```java
   public class ServletToBeanProxy extends GenericServlet {
       // 当前客户端请求的Servlet名字
       private String targetBean;
       // 代理Servlet
       private Servlet proxy;
       @Override
       public void init() throws ServletException {
           super.init();
           // 初始化Spring容器
           WebApplicationContext wac = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
           // 获取Servlet名
           this.targetBean = getServletName();
           // 调用ServletBean
           this.proxy = (Servlet) wac.getBean(targetBean);
           // 调用初始化方法将ServletConfig传给Bean
           proxy.init(getServletConfig());
       }
       @Override
       public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
           // 在service方法中调用bean的service方法，servlet会根据客户的请求去调用相应的请求方法(Get/Post)
           proxy.service(request, response);
       }
   }
   ```

3. 使用XB0101SendServlet
   ```java
   public class XB0101SendServlet extends HttpServlet {
       @Inject
       XB0101Send xb0101Send;
       //http://localhost:8080/yz-trans-ws/XB0101Send?vehicleNo=123456\&plateColorCode=1\&province=640000
       protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
           //进入请求前的数据准备：业户查询
           xb0101Send.SendXB0101(request.getParameter("no"),request.getParameter("code"));
       }
       protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
           doPost(request,response);
       }
   }
   ```

4. xb0101Send 结构
   ```java
   @Named
   public class XB0101Send {
       private static Logger log = LoggerFactory.getLogger(XB0101Send.class);
       @Inject
       protected LoginUser loginUser;
       public QB0101Resp SendXB0101(String no,String code){   };
   }
   ```



