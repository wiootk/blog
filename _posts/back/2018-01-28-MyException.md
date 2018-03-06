---
layout: post
title:  "Java自定义异常"
date:   2018-01-28
desc: "Java自定义异常"
keywords: "Java,自定义异常"
categories: [Back]
tags: [Java,自定义异常]
icon: icon-javaScript
---
1. 所有异常都必须是 Throwable 的子类  
异常分为：检查性异常类 Exception 类，运行时异常类 RuntimeException 类。

2. 自定义异常类：
```java
 public class MyException extends RuntimeException { 
     private static final long serialVersionUID = 1L; 
     //错误编码
     private String errorCode; 
     //消息是否为属性文件中的Key
     private boolean propertiesKey = true; 
     // 构造函数
     public MyException(String message){
         super(message);
     }
     public MyException(String errorCode, String message){
         this(errorCode, message, true);
     }
     public MyException(String errorCode, String message, Throwable cause){
         this(errorCode, message, cause, true);
     }
     public MyException(String errorCode, String message, boolean propertiesKey){
         super(message);
         this.setErrorCode(errorCode);
         this.setPropertiesKey(propertiesKey);
     }
     public MyException(String errorCode, String message, Throwable cause, boolean propertiesKey){
         super(message, cause);
         this.setErrorCode(errorCode);
         this.setPropertiesKey(propertiesKey);
     }
     public MyException(String message, Throwable cause){
         super(message, cause);
     }     
     public String getErrorCode(){
         return errorCode;
     } 
     public void setErrorCode(String errorCode){
         this.errorCode = errorCode;
     } 
     public boolean isPropertiesKey(){
         return propertiesKey;
     } 
     public void setPropertiesKey(boolean propertiesKey){
         this.propertiesKey = propertiesKey;
     }     
 }
```

3. 使用自定义异常抛出异常信息
```java
public class MyExceptionTest { 
     public static void main(String[] args) {         
          String[] sexs = {"男性","女性","中性"};
          for(int i = 0; i < sexs.length; i++){
              if("中性".equals(sexs[i])){
                  throw new MyException("你全家都是中性！");
              }else{
                  System.out.println(sexs[i]);
              }
          } 
     }
 }
```