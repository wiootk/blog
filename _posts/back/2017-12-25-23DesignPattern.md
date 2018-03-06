---
layout: post
title:  "23种设计模式（java版）"
date:   2017-12-25
desc: "23种设计模式（java版）"
keywords: "后端,java,设计模式"
categories: [Back]
tags: [后端,java,设计模式]
icon: icon-java
---

## 设计模式的六大原则
从大型软件架构出发，为了升级和维护方便。文中多次出现：降低依赖，降低耦合

1. 开闭原则：对扩展开放，对修改关闭（热插拔、使用接口和抽象类）  
2. 里氏代换原则：任何基类可以出现的地方，子类一定可以出现。 继承复用的基石，只有当衍生类可以替换掉基类，软件单位的功能不受到影响时，基类才能真正被复用，而衍生类也能够在基类的基础上增加新的行为。而基类与子类的继承关系就是抽象化的具体实现  
3. 依赖倒转原则：真对接口编程，依赖于抽象而不依赖于具体  
4. 接口隔离原则：使用多个隔离的接口，比使用单个接口要好。降低类之间的耦合度  
5. 迪米特法则（最少知道原则）：使系统功能模块相对独立  
6. 合成复用原则：尽量使用合成/聚合的方式，而不是继承。  
**设计模式**  
*创建型模式：* 工厂方法模式、抽象工厂模式、单例模式、建造者模式、原型模式
*结构型模式：* 适配器模式、装饰者模式、代理模式、外观模式、桥接模式、组合模式、享元模式  
*行为型模式：* 策略模式、模板方法模式、观察者模式、迭代子模式、责任链模式、命令模式、备忘录模式、状态模式、访问者模式、中介者模式、解释器模式  
*还有两类：* 并发型模式和线程池模式  


## 设计模式

从这一块开始，我们详细介绍Java中23种设计模式的概念，应用场景等情况，并结合他们的特点及设计模式的原则进行分析。

### 工厂方法模式

1. 普通工厂模式
```java
public interface Sender {  
    public void Send();  
}  
//实现类:
public class MailSender implements Sender {  
    @Override  
    public void Send() {  
        System.out.println("this is mailsender!");  
    }  
}
public class SmsSender implements Sender {   
    @Override  
    public void Send() {  
        System.out.println("this is sms sender!");  
    }  
}  
//工厂类：
public class SendFactory {   
    public Sender produce(String type) {
    //如果字符串有误，不能正确创建对象  
        if ("mail".equals(type)) {  
            return new MailSender();  
        } else if ("sms".equals(type)) {  
            return new SmsSender();  
        } else {  
            System.out.println("请输入正确的类型!");  
            return null;  
        }  
    }  
}  
//测试：
public class FactoryTest {    
    public static void main(String[] args) {  
        SendFactory factory = new SendFactory();  
        Sender sender = factory.produce("sms");  
        sender.Send();  
    }  
}  
//输出：this is sms sender!
```

2. 多个工厂方法模式
```java
public class SendFactory {  
   public Sender produceMail(){  
        return new MailSender();  
    }
    public Sender produceSms(){  
        return new SmsSender();  
    }  
}  
//测试类：
public class FactoryTest {   
    public static void main(String[] args) {  
        SendFactory factory = new SendFactory();  
        Sender sender = factory.produceMail();  
        sender.Send();  
    }  
}  
//输出：this is mailsender!
```

3. 静态工厂方法模式
```java
public class SendFactory {        
    public static Sender produceMail(){  
        return new MailSender();  
    }       
    public static Sender produceSms(){  
        return new SmsSender();  
    }  
}  
//测试类：
public class FactoryTest {   
    public static void main(String[] args) {      
        Sender sender = SendFactory.produceMail();  
        sender.Send();  
    }  
}  
//输出：this is mailsender!
```
工厂模式适合：凡是出现了大量的产品需要创建，并且具有共同的接口时，可以通过工厂方法模式进行创建。

### 抽象工厂模式
工厂方法模式:违背了闭包原则
抽象工厂模式:创建多个工厂类，增加新功能时，直接增加新的工厂类,拓展性较好
```java
public interface Sender {  
    public void Send();  
}  
//实现类：
public class MailSender implements Sender {  
    @Override  
    public void Send() {  
        System.out.println("this is mailsender!");  
    }  
}  
public class SmsSender implements Sender {    
    @Override  
    public void Send() {  
        System.out.println("this is sms sender!");  
    }  
}  
//工厂类：
public class SendMailFactory implements Provider {      
    @Override  
    public Sender produce(){  
        return new MailSender();  
    }  
}  
public class SendSmsFactory implements Provider{    
    @Override  
    public Sender produce() {  
        return new SmsSender();  
    }  
}  
//提供接口：
public interface Provider {  
    public Sender produce();  
}  
//测试类：
public class Test {   
    public static void main(String[] args) {  
        Provider provider = new SendMailFactory();  
        Sender sender = provider.produce();  
        sender.Send();  
    }  
}
```

### 单例模式
在一个JVM中，该对象只有一个实例存在  
**好处：**  
1、某些类创建比较频繁，对于一些大型的对象，这是一笔很大的系统开销。  
2、省去了new操作符，降低了系统内存的使用频率，减轻GC压力。  
3、有些类如交易所的核心交易引擎，控制着交易流程，如果该类可以创建多个的话，系统完全乱了。  
```java
//多线程的环境下，无线程安全保护类
public class Singleton {    
    /* 持有私有静态实例，防止被引用，此处赋值为null，目的是实现延迟加载 */  
    private static Singleton instance = null;    
    /* 私有构造方法，防止被实例化 */  
    private Singleton() {    } 
     /* 此处使用一个内部类来维护单例 */  
    private static class SingletonFactory {  
        private static Singleton instance = new Singleton();  
    }    
    /* 静态工程方法，创建实例 */  
    public static Singleton getInstance() {  
      //  if (instance == null) {  
      //      instance = new Singleton();  
      //  }  
      //  return instance; 
        return SingletonFactory.instance;   
    }  
    /* 如果该对象被用于序列化，可以保证对象在序列化前后保持一致 */  
    public Object readResolve() {  
        return instance;  
    }  
}
```
测试
```java
public class SingletonTest {
    private static SingletonTest instance = null;
    private Vector properties = null;
    public Vector getProperties() {
        return properties;
    }  
    private SingletonTest() {    }   
    private static synchronized void syncInit() {  
        if (instance == null) {  
            instance = new SingletonTest();  
        }  
    } 
    public static SingletonTest getInstance() {  
        if (instance == null) {  
            syncInit();  
        }  
        return instance;  
    }
    public void updateProperties() {  
        SingletonTest shadow = new SingletonTest();  
        properties = shadow.getProperties();  
    }  
}  
```

### 建造者模式
将各种产品集中起来管理，创建复合对象
```java
public class Builder {       
    private List<Sender> list = new ArrayList<Sender>();        
    public void produceMailSender(int count){  
        for(int i=0; i<count; i++){  
            list.add(new MailSender());  
        }  
    }        
    public void produceSmsSender(int count){  
        for(int i=0; i<count; i++){  
            list.add(new SmsSender());  
        }  
    }  
}  
//测试类：
public class Test {    
    public static void main(String[] args) {  
        Builder builder = new Builder();  
        builder.produceMailSender(10);  
    }  
}
```

### 原型模式
```java
创建一个原型类：
public class Prototype implements Cloneable {  
  
    public Object clone() throws CloneNotSupportedException {  
        Prototype proto = (Prototype) super.clone();  
        return proto;  
    }  
}  
```
浅复制：基本数据类型的变量都会重新创建，而引用类型，指向的还是原对象所指向的。  
深复制：将一个对象复制后，不论是基本数据类型还有引用类型，都是重新创建的  
```java
public class Prototype implements Cloneable, Serializable {
    private static final long serialVersionUID = 1L;  
    private String string;    
    private SerializableObject obj;    
    /* 浅复制 */  
    public Object clone() throws CloneNotSupportedException {  
        Prototype proto = (Prototype) super.clone();  
        return proto;  
    }    
    /* 深复制 */  
    public Object deepClone() throws IOException, ClassNotFoundException {   
        /* 写入当前对象的二进制流 */  
        ByteArrayOutputStream bos = new ByteArrayOutputStream();  
        ObjectOutputStream oos = new ObjectOutputStream(bos);  
        oos.writeObject(this);    
        /* 读出二进制流产生的新对象 */  
        ByteArrayInputStream bis = new ByteArrayInputStream(bos.toByteArray()); 
        ObjectInputStream ois = new ObjectInputStream(bis);  
        return ois.readObject();  
    }    
  //  get/set...  
}  
  
class SerializableObject implements Serializable {  
    private static final long serialVersionUID = 1L;  
}
```

### 适配器模式
消除由于接口不匹配所造成的类的兼容性问题  
1. 类的适配器模式  
```java
public class Source {    
    public void method1() {  
        System.out.println("this is original method!");  
    }  
}
public interface Targetable {    
    /* 与原类中的方法相同 */  
    public void method1();    
    /* 新类的方法 */  
    public void method2();  
}
public class Adapter extends Source implements Targetable {    
    @Override  
    public void method2() {  
        System.out.println("this is the targetable method!");  
    }  
}  
//测试类：
public class AdapterTest {    
    public static void main(String[] args) {  
        Targetable target = new Adapter();  
        target.method1();  
        target.method2();  
    }  
}  
//输出：
//this is original method!
//this is the targetable method!
```

2. 对象的适配器模式
```java
public class Wrapper implements Targetable {  
    private Source source;      
    public Wrapper(Source source){  
        super();  
        this.source = source;  
    }  
    @Override  
    public void method2() {  
        System.out.println("this is the targetable method!");  
    }  
    @Override  
    public void method1() {  
        source.method1();  
    }  
}  
//测试类
public class AdapterTest {  
    public static void main(String[] args) {  
        Source source = new Source();  
        Targetable target = new Wrapper(source);  
        target.method1();  
        target.method2();  
    }  
}  
```

3. 接口的适配器模式
```java
public interface Sourceable {        
    public void method1();  
    public void method2();  
}  
//抽象类Wrapper2：
public abstract class Wrapper2 implements Sourceable{        
    public void method1(){}  
    public void method2(){}  
}  
public class SourceSub1 extends Wrapper2 {  
    public void method1(){  
        System.out.println("the sourceable interface's first Sub1!");  
    }  
}  
public class SourceSub2 extends Wrapper2 {  
    public void method2(){  
        System.out.println("the sourceable interface's second Sub2!");  
    }  
}  
public class WrapperTest {    
    public static void main(String[] args) {  
        Sourceable source1 = new SourceSub1();  
        Sourceable source2 = new SourceSub2();            
        source1.method1();  
        source1.method2();  
        source2.method1();  
        source2.method2();  
    }  
}  
```

**应用场景：**  
**类的适配器模式：**当希望将一个类转换成满足另一个新接口的类时，可以使用类的适配器模式，创建一个新类，继承原有的类，实现新的接口即可。  
**对象的适配器模式：**当希望将一个对象转换成满足另一个新接口的对象时，可以创建一个Wrapper类，持有原类的一个实例，在Wrapper类的方法中，调用实例的方法就行。  
**接口的适配器模式：**当不希望实现一个接口中所有的方法时，可以创建一个抽象类Wrapper，实现所有方法，我们写别的类的时候，继承抽象类即可  

### 装饰模式（Decorator）
给一个对象增加一些新的功能，而且是动态的
```java
public interface Sourceable {  
    public void method();  
} 
//被装饰类
public class Source implements Sourceable {  
    @Override  
    public void method() {  
        System.out.println("the original method!");  
    }  
}
//装饰类 
public class Decorator implements Sourceable {  
    private Sourceable source;      
    public Decorator(Sourceable source){  
        super();  
        this.source = source;  
    }  
    @Override  
    public void method() {  
        System.out.println("before decorator!");  
        source.method();  
        System.out.println("after decorator!");  
    }  
}  
//测试类：
public class DecoratorTest {  
    public static void main(String[] args) {  
        Sourceable source = new Source();  
        Sourceable obj = new Decorator(source);  
        obj.method();  
    }  
}  
//输出：
//before decorator!
//the original method!
//after decorator!
```

### 代理模式
调用原有的方法，且对产生的结果进行控制
```java
public interface Sourceable {  
    public void method();  
}
public class Source implements Sourceable {  
    @Override  
    public void method() {  
        System.out.println("the original method!");  
    }  
}
public class Proxy implements Sourceable {  
    private Source source;  
    public Proxy(){  
        super();  
        this.source = new Source();  
    }  
    @Override  
    public void method() {  
        before();  
        source.method();  
        atfer();  
    }  
    private void atfer() {  
        System.out.println("after proxy!");  
    }  
    private void before() {  
        System.out.println("before proxy!");  
    }  
}  
//测试类：
public class ProxyTest {  
    public static void main(String[] args) {  
        Sourceable source = new Proxy();  
        source.method();  
    }  
}  
//输出：
//before proxy!
//the original method!
//after proxy!
```

### 外观模式
外观模式是为了解决类与类之家的依赖关系的,将他们的关系放在一个Facade类中，降低了类类之间的耦合度
```java
public class CPU {      
    public void startup(){  
        System.out.println("cpu startup!");  
    }
    public void shutdown(){  
        System.out.println("cpu shutdown!");  
    }  
}
public class Memory {      
    public void startup(){  
        System.out.println("memory startup!");  
    }      
    public void shutdown(){  
        System.out.println("memory shutdown!");  
    }  
}
public class Disk {      
    public void startup(){  
        System.out.println("disk startup!");  
    }      
    public void shutdown(){  
        System.out.println("disk shutdown!");  
    }  
}
public class Computer {  
    private CPU cpu;  
    private Memory memory;  
    private Disk disk;      
    public Computer(){  
        cpu = new CPU();  
        memory = new Memory();  
        disk = new Disk();  
    }      
    public void startup(){  
        System.out.println("start the computer!");  
        cpu.startup();  
        memory.startup();  
        disk.startup();  
        System.out.println("start computer finished!");  
    }      
    public void shutdown(){  
        System.out.println("begin to close the computer!");  
        cpu.shutdown();  
        memory.shutdown();  
        disk.shutdown();  
        System.out.println("computer closed!");  
    }  
}  
//User类如下:
public class User {  
    public static void main(String[] args) {  
        Computer computer = new Computer();  
        computer.startup();  
        computer.shutdown();  
    }  
}
```

### 桥接模式
将抽象化与实现化解耦
```java
//定义接口：
public interface Sourceable {  
    public void method();  
}  
//分别定义两个实现类：
public class SourceSub1 implements Sourceable {
    @Override  
    public void method() {  
        System.out.println("this is the first sub!");  
    }  
}
public class SourceSub2 implements Sourceable {
    @Override  
    public void method() {  
        System.out.println("this is the second sub!");  
    }  
}  
//定义一个桥
public abstract class Bridge {  
    private Sourceable source;  
    public void method(){  
        source.method();  
    }      
    public Sourceable getSource() {  
        return source;  
    }  
    public void setSource(Sourceable source) {  
        this.source = source;  
    }  
}  
public class MyBridge extends Bridge {  
    public void method(){  
        getSource().method();  
    }  
}  
//测试类：
public class BridgeTest {
    public static void main(String[] args) {
        Bridge bridge = new MyBridge();
        /*调用第一个对象*/  
        Sourceable source1 = new SourceSub1();  
        bridge.setSource(source1);  
        bridge.method();
        /*调用第二个对象*/  
        Sourceable source2 = new SourceSub2();  
        bridge.setSource(source2);  
        bridge.method();  
    }  
}  
```

### 组合模式（Composite）
又叫部分-整体模式在处理类似树形结构的问题时比较方便
```java
public class TreeNode {
    private String name;  
    private TreeNode parent;  
    private Vector<TreeNode> children = new Vector<TreeNode>();      
    public TreeNode(String name){  
        this.name = name;  
    }  
    // get/set...      
    //添加孩子节点  
    public void add(TreeNode node){  
        children.add(node);  
    }      
    //删除孩子节点  
    public void remove(TreeNode node){  
        children.remove(node);  
    }      
    //取得孩子节点  
    public Enumeration<TreeNode> getChildren(){  
        return children.elements();  
    }
}  

public class Tree {  
    TreeNode root = null;  
    public Tree(String name) {  
        root = new TreeNode(name);  
    }  
    public static void main(String[] args) {  
        Tree tree = new Tree("A");  
        TreeNode nodeB = new TreeNode("B");  
        TreeNode nodeC = new TreeNode("C");
        nodeB.add(nodeC);  
        tree.root.add(nodeB);  
        System.out.println("build the tree finished!");  
    }  
}
```

### 享元模式（Flyweight）
实现对象的共享，即共享池
FlyWeightFactory负责创建和管理享元单元，当一个客户端请求时，工厂需要检查当前对象池中是否有符合条件的对象，如果有，就返回已经存在的对象，如果没有，则创建一个新对象，FlyWeight是超类  
数据库连接池的代码：  
```java
public class ConnectionPool {
    private Vector<Connection> pool;
    /*公有属性*/  
    private String url = "jdbc:mysql://localhost:3306/test";  
    private String username = "root";  
    private String password = "root";  
    private String driverClassName = "com.mysql.jdbc.Driver";  
  
    private int poolSize = 100;  
    private static ConnectionPool instance = null;  
    Connection conn = null;  
  
    /*构造方法，做一些初始化工作*/  
    private ConnectionPool() {  
        pool = new Vector<Connection>(poolSize);  
  
        for (int i = 0; i < poolSize; i++) {  
            try {  
                Class.forName(driverClassName);  
                conn = DriverManager.getConnection(url, username, password);  
                pool.add(conn);  
            } catch (ClassNotFoundException e) {  
                e.printStackTrace();  
            } catch (SQLException e) {  
                e.printStackTrace();  
            }  
        }  
    }  
  
    /* 返回连接到连接池 */  
    public synchronized void release() {  
        pool.add(conn);  
    }  
  
    /* 返回连接池中的一个数据库连接 */  
    public synchronized Connection getConnection() {  
        if (pool.size() > 0) {  
            Connection conn = pool.get(0);  
            pool.remove(conn);  
            return conn;  
        } else {  
            return null;  
        }  
    }  
}  
```

### 策略模式（strategy）
策略模式定义了一系列算法，并将每个算法封装起来，使他们可以相互替换，且算法的变化不会影响到使用算法的客户
```java
//首先统一接口
public interface ICalculator {  
    public int calculate(String exp);  
}  
//辅助类
public abstract class AbstractCalculator {      
    public int[] split(String exp,String opt){  
        String array[] = exp.split(opt);  
        int arrayInt[] = new int[2];  
        arrayInt[0] = Integer.parseInt(array[0]);  
        arrayInt[1] = Integer.parseInt(array[1]);  
        return arrayInt;  
    }  
}  
//三个实现类
public class Plus extends AbstractCalculator implements ICalculator { 
    @Override  
    public int calculate(String exp) {  
        int arrayInt[] = split(exp,"\\+");  
        return arrayInt[0]+arrayInt[1];  
    }  
}
public class Minus extends AbstractCalculator implements ICalculator {  
    @Override  
    public int calculate(String exp) {  
        int arrayInt[] = split(exp,"-");  
        return arrayInt[0]-arrayInt[1];  
    }  
  
}  
public class Multiply extends AbstractCalculator implements ICalculator {
    @Override  
    public int calculate(String exp) {  
        int arrayInt[] = split(exp,"\\*");  
        return arrayInt[0]*arrayInt[1];  
    }  
}  
//简单的测试类：
public class StrategyTest {
    public static void main(String[] args) {  
        String exp = "2+8";  
        ICalculator cal = new Plus();  
        int result = cal.calculate(exp);  
        System.out.println(result);  
    }  
}  
```

### 模板方法模式（Template Method）
一个抽象类中，有一个主方法，再定义1...n个方法，可以是抽象的，也可以是实际的方法，定义一个类，继承该抽象类，重写抽象方法，通过调用抽象类，实现对子类的调用
```java
public abstract class AbstractCalculator {      
    /*主方法，实现对本类其它方法的调用*/  
    public final int calculate(String exp,String opt){  
        int array[] = split(exp,opt);  
        return calculate(array[0],array[1]);  
    }      
    /*被子类重写的方法*/  
    abstract public int calculate(int num1,int num2);      
    public int[] split(String exp,String opt){  
        String array[] = exp.split(opt);  
        int arrayInt[] = new int[2];  
        arrayInt[0] = Integer.parseInt(array[0]);  
        arrayInt[1] = Integer.parseInt(array[1]);  
        return arrayInt;  
    }  
}
public class Plus extends AbstractCalculator {
    @Override  
    public int calculate(int num1,int num2) {  
        return num1 + num2;  
    }  
}  
//测试类
public class StrategyTest {  
    public static void main(String[] args) {  
        String exp = "8+8";  
        AbstractCalculator cal = new Plus();  
        int result = cal.calculate(exp, "\\+");  
        System.out.println(result);  
    }  
} 
```

### 观察者模式（Observer）
类似于邮件订阅和RSS订阅，当一个对象变化时，其它依赖该对象的对象都会收到通知，并且随着变化！对象之间是一种一对多的关系   
解释下这些类的作用：MySubject类就是我们的主对象，Observer1和Observer2是依赖于MySubject的对象，当MySubject变化时，Observer1和Observer2必然变化。AbstractSubject类中定义着需要监控的对象列表，可以对其进行修改：增加或删除被监控对象，且当MySubject变化时，负责通知在列表内存在的对象。  

```java
//一个Observer接口
public interface Observer {  
    public void update();  
}  
//两个实现类
public class Observer1 implements Observer {  
    @Override  
    public void update() {  
        System.out.println("observer1 has received!");  
    }  
}  
public class Observer2 implements Observer {
    @Override  
    public void update() {  
        System.out.println("observer2 has received!");  
    }  
  
}  
// Subject接口及实现类
public interface Subject {
    /*增加观察者*/  
    public void add(Observer observer);
    /*删除观察者*/  
    public void del(Observer observer);
    /*通知所有的观察者*/  
    public void notifyObservers();
    /*自身的操作*/  
    public void operation();  
}
public abstract class AbstractSubject implements Subject {
    private Vector<Observer> vector = new Vector<Observer>();  
    @Override  
    public void add(Observer observer) {  
        vector.add(observer);  
    }
    @Override  
    public void del(Observer observer) {  
        vector.remove(observer);  
    }
    @Override  
    public void notifyObservers() {  
        Enumeration<Observer> enumo = vector.elements();  
        while(enumo.hasMoreElements()){  
            enumo.nextElement().update();  
        }  
    }  
}  
public class MySubject extends AbstractSubject {
    @Override  
    public void operation() {  
        System.out.println("update self!");  
        notifyObservers();  
    }
}
//测试类
public class ObserverTest {
    public static void main(String[] args) {  
        Subject sub = new MySubject();  
        sub.add(new Observer1());  
        sub.add(new Observer2()); 
        sub.operation();  
    }  
  
}  
//输出
//update self!
//observer1 has received!
//observer2 has received!
```

### 迭代子模式（Iterator）
迭代器模式就是顺序访问聚集中的对象：一是需要遍历的对象，即聚集对象，二是迭代器对象，用于对聚集对象进行遍历访问。
```java
public interface Collection {      
    public Iterator iterator();      
    /*取得集合元素*/  
    public Object get(int i);      
    /*取得集合大小*/  
    public int size();  
}
public interface Iterator {  
    //前移  
    public Object previous();      
    //后移  
    public Object next();  
    public boolean hasNext();      
    //取得第一个元素  
    public Object first();  
}  
//两个实现：
public class MyCollection implements Collection {
    public String string[] = {"A","B","C","D","E"};  
    @Override  
    public Iterator iterator() {  
        return new MyIterator(this);  
    }
    @Override  
    public Object get(int i) {  
        return string[i];  
    }
    @Override  
    public int size() {  
        return string.length;  
    }  
}  
public class MyIterator implements Iterator {
    private Collection collection;  
    private int pos = -1;     
    public MyIterator(Collection collection){  
        this.collection = collection;  
    }
    @Override  
    public Object previous() {  
        if(pos > 0){  
            pos--;  
        }  
        return collection.get(pos);  
    }
    @Override  
    public Object next() {  
        if(pos<collection.size()-1){  
            pos++;  
        }  
        return collection.get(pos);  
    }
    @Override  
    public boolean hasNext() {  
        if(pos<collection.size()-1){  
            return true;  
        }else{  
            return false;  
        }  
    }
    @Override  
    public Object first() {  
        pos = 0;  
        return collection.get(pos);  
    }
}  
//测试类：
public class Test {
    public static void main(String[] args) {  
        Collection collection = new MyCollection();  
        Iterator it = collection.iterator(); 
        while(it.hasNext()){  
            System.out.println(it.next());  
        }  
    }  
}  
//输出：A B C D E
```

### 责任链模式（Chain of Responsibility）
有多个对象，每个对象持有对下一个对象的引用，这样就会形成一条链，请求在这条链上传递，直到某一对象决定处理该请求  
Abstracthandler类提供了get和set方法，方便MyHandle类设置和修改引用对象，MyHandle类是核心，实例化后生成一系列相互持有的对象，构成一条链。
```java
public interface Handler {  
    public void operator();  
}
public abstract class AbstractHandler {
    private Handler handler;
    public Handler getHandler() {  
        return handler;  
    }
    public void setHandler(Handler handler) {  
        this.handler = handler;  
    }
}  
public class MyHandler extends AbstractHandler implements Handler {
    private String name;
    public MyHandler(String name) {  
        this.name = name;  
    }
    @Override  
    public void operator() {  
        System.out.println(name+"deal!");  
        if(getHandler()!=null){  
            getHandler().operator();  
        }  
    }  
}  
public class Test {
    public static void main(String[] args) {  
        MyHandler h1 = new MyHandler("h1");  
        MyHandler h2 = new MyHandler("h2");  
        MyHandler h3 = new MyHandler("h3"); 
        h1.setHandler(h2);  
        h2.setHandler(h3);
        h1.operator();  
    }  
}  
//输出
//h1deal!
//h2deal!
//h3deal!
```

### 命令模式（Command）
司令员的作用是，发出口令，口令经过传递，传到了士兵耳朵里，士兵去执行
```java
public interface Command {  
    public void exe();  
}  
//命令，持有接收对象
public class MyCommand implements Command { 
    private Receiver receiver;
    public MyCommand(Receiver receiver) {  
        this.receiver = receiver;  
    }
    @Override  
    public void exe() {  
        receiver.action();  
    }  
}  
//被调用者（士兵）
public class Receiver {  
    public void action(){  
        System.out.println("command received!");  
    }  
}
//调用者（司令员） 
public class Invoker {
    private Command command;
    public Invoker(Command command) {  
        this.command = command;  
    }
    public void action(){  
        command.exe();  
    }  
}
public class Test {
    public static void main(String[] args) {  
        Receiver receiver = new Receiver();  
        Command cmd = new MyCommand(receiver);  
        Invoker invoker = new Invoker(cmd);  
        invoker.action();  
    }  
}  
//输出：command received!
```

### 备忘录模式（Memento）
保存一个对象的某个状态，以便在适当的时候恢复对象，个人觉得叫备份模式更形象些，通俗的讲下：假设有原始类A，A中有各种属性，A可以决定需要备份的属性，备忘录类B是用来存储A的一些内部状态，类C呢，就是一个用来存储备忘录的，且只能存储，不能修改等操作  
Memento类是，Storage类是，持有Memento类的实例，该模式很好理解。
```java
//原始类
public class Original {       
    private String value;        
    public String getValue() {  
        return value;  
    }    
    public void setValue(String value) {  
        this.value = value;  
    }    
    public Original(String value) {  
        this.value = value;  
    }    
    public Memento createMemento(){  
        return new Memento(value);  
    }        
    public void restoreMemento(Memento memento){  
        this.value = memento.getValue();  
    }  
}  
//备忘录类
public class Memento {        
    private String value;    
    public Memento(String value) {  
        this.value = value;  
    }    
    public String getValue() {  
        return value;  
    }    
    public void setValue(String value) {  
        this.value = value;  
    }  
}  
//存储备忘录的类
public class Storage {        
    private Memento memento;        
    public Storage(Memento memento) {  
        this.memento = memento;  
    }    
    public Memento getMemento() {  
        return memento;  
    }    
    public void setMemento(Memento memento) {  
        this.memento = memento;  
    }  
}  
//测试类：
public class Test {    
    public static void main(String[] args) {            
        // 创建原始类  
        Original origi = new Original("egg");    
        // 创建备忘录  
        Storage storage = new Storage(origi.createMemento());    
        // 修改原始类的状态  
        System.out.println("初始化状态为：" + origi.getValue());  
        origi.setValue("niu");  
        System.out.println("修改后的状态为：" + origi.getValue());   
        // 回复原始类的状态  
        origi.restoreMemento(storage.getMemento());  
        System.out.println("恢复后的状态为：" + origi.getValue());  
    }  
}  
//输出：
//初始化状态为：egg
//修改后的状态为：niu
//恢复后的状态为：egg
```

### 状态模式（State）
当对象的状态改变时，同时改变其行为  
1. 可以通过改变状态来获得不同的行为。  
2. 你的好友能同时看到你的变化。  
```java
//状态类
public class State {       
    private String value;      
    public String getValue() {  
        return value;  
    }
    public void setValue(String value) {  
        this.value = value;  
    }
    public void method1(){  
        System.out.println("execute the first opt!");  
    } 
    public void method2(){  
        System.out.println("execute the second opt!");  
    }  
}  
//实现切换
public class Context {
    private State state;
    public Context(State state) {  
        this.state = state;  
    }
    public State getState() {  
        return state;  
    }
    public void setState(State state) {  
        this.state = state;  
    }
    public void method() {  
        if (state.getValue().equals("state1")) {  
            state.method1();  
        } else if (state.getValue().equals("state2")) {  
            state.method2();  
        }  
    }  
}  
//测试类：
public class Test {
    public static void main(String[] args) {
        State state = new State();  
        Context context = new Context(state);
        //设置第一种状态  
        state.setValue("state1");  
        context.method();
        //设置第二种状态  
        state.setValue("state2");  
        context.method();  
    }  
}  
//输出
//execute the first opt!
//execute the second opt!
```

### 访问者模式（Visitor）
把数据结构和作用于结构上的操作解耦合，使得操作集合可相对自由地演化。访问者模式适用于数据结构相对稳定算法又易变化的系统。
```java
//存放要访问的对象
public interface Visitor {  
    public void visit(Subject sub);  
}  
public class MyVisitor implements Visitor {  
    @Override  
    public void visit(Subject sub) {  
        System.out.println("visit the subject："+sub.getSubject());  
    }  
}  
public interface Subject {
    //接受将要访问它的对象
    public void accept(Visitor visitor);
    //获取将要被访问的属性   
    public String getSubject();  
}
public class MySubject implements Subject { 
    @Override  
    public void accept(Visitor visitor) {  
        visitor.visit(this);  
    } 
    @Override  
    public String getSubject() {  
        return "love";  
    }  
}  
//测试：
public class Test { 
    public static void main(String[] args) { 
        Visitor visitor = new MyVisitor();  
        Subject sub = new MySubject();  
        sub.accept(visitor);      
    }  
}  
//输出：visit the subject：love
```

### 中介者模式（Mediator）
如果使用中介者模式，只需关心和Mediator类的关系，具体类类之间的关系及调度交给Mediator就行,解耦类与类的关系
```java
public interface Mediator {  
    public void createMediator();  
    public void workAll();  
}
public class MyMediator implements Mediator {  
    private User user1;  
    private User user2;      
    public User getUser1() {  
        return user1;  
    }  
    public User getUser2() {  
        return user2;  
    }  
    @Override  
    public void createMediator() {  
        user1 = new User1(this);  
        user2 = new User2(this);  
    }  
    @Override  
    public void workAll() {  
        user1.work();  
        user2.work();  
    }  
}  

public abstract class User {
    private Mediator mediator;
    public Mediator getMediator(){  
        return mediator;  
    }
    public User(Mediator mediator) {  
        this.mediator = mediator;  
    }
    public abstract void work();  
}
public class User1 extends User {
    public User1(Mediator mediator){  
        super(mediator);  
    }
    @Override  
    public void work() {  
        System.out.println("user1 exe!");  
    }  
}
public class User2 extends User {
    public User2(Mediator mediator){  
        super(mediator);  
    }
    @Override  
    public void work() {  
        System.out.println("user2 exe!");  
    }  
}  
//测试类：
public class Test {
    public static void main(String[] args) {  
        Mediator mediator = new MyMediator();  
        mediator.createMediator();  
        mediator.workAll();  
    }  
}  
//输出：
//user1 exe!
//user2 exe!
```

### 解释器模式（Interpreter）
一般主要应用在OOP开发中的编译器的开发中，适用面比较窄。用来做各种各样的解释器
```java
public interface Expression {  
    public int interpret(Context context);  
}
public class Plus implements Expression {  
    @Override  
    public int interpret(Context context) {  
        return context.getNum1()+context.getNum2();  
    }  
}
public class Minus implements Expression {  
    @Override  
    public int interpret(Context context) {  
        return context.getNum1()-context.getNum2();  
    }  
}
//上下文环境类
public class Context {
    private int num1;  
    private int num2;
    public Context(int num1, int num2) {  
        this.num1 = num1;  
        this.num2 = num2;  
    }
    public int getNum1() {  
        return num1;  
    }  
    public void setNum1(int num1) {  
        this.num1 = num1;  
    }  
    public int getNum2() {  
        return num2;  
    }  
    public void setNum2(int num2) {  
        this.num2 = num2;  
    }
}  
public class Test {
    public static void main(String[] args) { 
        // 计算9+2-8的值  
        int result = new Minus().interpret((new Context(new Plus()  
                .interpret(new Context(9, 2)), 8)));  
        System.out.println(result);  
    }  
}  
//结果：3
```

 