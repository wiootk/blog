---
layout: post
title:  "js小知识"
date:   2018-01-28
desc: "js小知识"
keywords: "js,js小知识"
categories: [Front]
tags: [js,js小知识]
icon: icon-javaScript
---
[参考](http://www.jstips.co/zh_CN/){:target="_blank"}  

1. JS中定义类和对象
定义：
```js
function Person(name, age,) {    //var name;//局部变量
             this.name=name;
             this.age=age;
             this.show=function(){alert("show");}
               if ((typeof this.sayName) != "function") {
               //只初始化一次
                 Person.prototype.sayName = function () {alert(this.name);} 
            }
 }       
//Person.prototype = {
//     constructor: Person,
//     sayName: function () { alert(this.name);}
// };
```
使用：
```js
var ren = new Person('abc',10);
console.log(ren.name);
ren.show();
ren.sayName();
console.log(typeof  ren);// object
console.log(ren instanceof Person );//true
```

2. JS中定义定义或改写全局对象
```js
window.alert=function(ev){console.log(ev);}
```

3. JS为对象原形添加方法
```js
Array.prototype.removeByValue = function(val) {
  for(var i=0; i<this.length; i++) {
    if(this[i] == val) {
      this.splice(i, 1);
      break;
    }
  }
}
["mon", "tue", "wed", "thur"].removeByValue("tue");
```

4. 链式调用
```js
function A(num) {
  this.value = num || 0;
 }
//添加进行运算并返回this的方法
A.prototype.add = function(a) {this.value += a; return this;}
A.prototype.reduce = function(a) {this.value -= a; return this;}
A.prototype.valueOf = function() {return this.value;}
A.prototype.toString = function() {return this.value + '';}
//验证
var a = new A(2);
alert(a.add(1).reduce(2))
```

1. 向数组中插入元素(序号为效率排序)  
向数组结尾添加元素  
```js
arr[arr.length] = 6;//1.
arr.push(6);//2.
arr2 = arr.concat([6]);//3.
```
向数组的头部添加元素  
```js
[0].concat(arr); //返回新数组//1.
arr.unshift(0); //操作原始数组//2.
```
向数组中间添加元素  
```js
var items = ['one', 'two', 'three', 'four'];
items.splice(items.length / 2, 0, 'hello');
```

2. AngularJs - $digest vs $apply  
$apply显式启动digest循环，所有的watcher将会被检测。在内部会调用$rootScope.$digest();  
$digest在当前作用域及其子作用域启动$digest循环  
如果>AngularJS 1.2.X，使用$evalAsync, 这个方法将在当前循环或下一个循环执行表达式，这能提高你的应用的性能。  

3. 子容器的Key是很重要的  
key跟效率不是很相关，它更与身份有关系，确保子容器、对象是可保存而且不需要重复创建的  
当子组件的数量很大或者包含重量级的组件时，使用key来提高性能  
使用数组索引是一个坏习惯  

4. 优化嵌套的条件语句
```js
//待优化
if (color) {
  if (color === 'black') {
    printBlackBackground();
  } else if (color === 'red') {
    printRedBackground();
  } else {
    printYellowBackground();
  }
}
//使用switch，调试错误困难
switch(color) {
  case 'black':
    printBlackBackground();
    break;
  case 'red':
    printRedBackground();
    break;
  default:
    printYellowBackground();
}
//最有效率的方法：借助object
var colorObj = {
  'black': black,
  'red': red
};
if (color in colorObj) {
  colorObj[color]();
}
```

5. 排列含音节字母的字符串  
原生方法：`array.sort()`  
自定义排列：`array.sort(function (a, b) {  return a-b;});`  
非ASCII元素的数组  
`['único','árbol'].sort(function (a, b) { return a.localeCompare(b);});`  
`['Woche', 'wöchentlich'].sort(Intl.Collator().compare);`

6. undefined与null的区别  
undefined表示一个变量没有被声明，或者被声明了但没有被赋值，不是有效的JSON
null是一个表示“没有值”的值，是有效的JSON  
```
Boolean(undefined) // false   Boolean(null) // false
null == undefined // true     null === undefined // false
```
undefined的类型(typeof)是undefined
null的类型(typeof)是object. 
判断是否是undefined          `typeof variable === "undefined"`
判断是否是null               `variable === null`

7. 可以接受单参数也可以数组的方法
原理：Array.concat可以接受一个数组也可以接受单个参数
```js
function printUpperCase(words) {
  var elements = [].concat(words || []);
  for (var i = 0; i < elements.length; i++) {
    console.log(elements[i].toUpperCase());
  }
}
printUpperCase("cactus");
printUpperCase(["cactus", "bear", "potato"]);
```

8. 使用"use strict" 变得懒惰
```js
// 全脚本严格模式
"use strict";
var v = "Hi!  I'm a strict mode script!";
//或者放在一个方法内：
function f(){
  // 方法级严格模式
  'use strict';
  function nested() { return "And so am I!"; }
  return "Hi!  I'm a strict mode function!  " + nested();
}
function f2() { return "I'm not strict."; }
```
```
只有被”var”声明过的变量才可以引用
试图写只读变量时将会报错
只能通过”new”关键字调用构造方法
“this”不再隐式的指向全局变量
对eval()有更严格的限制
防止你使用预保留关键字命名变量
```

9. 将Node List转换为数组(Array)
querySelectorAll方法返回一个类数组对象称为node list(类数组,没有类似map、foreach这样的数组方法)
```js
const nodelist = document.querySelectorAll('div');
const array1 = Array.apply(null, nodelist);
const array2 = Array.prototype.slice.call(nodelist); 
const array3 = [...document.querySelectorAll('div')]; //(ES6) 返回一个真正的数组
//之后 ..
array1.forEach(...);
array2.map(...);
array3.slice(...);
```

10. 模板字符串ES6
```js
var name = 'Jake',a = 1, b = 2;;
console.log(`name: ${name}`,`${a} ${a < 2 ? '小于': '大于'} ${2}`);
```

11. 检查某对象是否有某属性
```js
//通常：
var myObject = {  name: '@tips_js'};
if (myObject.name) {  }
//原生方法
myObject.hasOwnProperty('name'); // 本身的属性
'name' in myObject; // 本身或继承的原型链
```

12. 变量提升
变量声明和方法声明都会被提升到顶部。变量的定义不会提升
```js
function doTheThing() {
  // 报错：undefined
  console.log(definedSimulateneously);
  var definedSimulateneously = 'I am defined!'
  ==
   var definedLater;
   console.log(definedSimulateneously);
  definedLater = 'I am defined!';
  //提升
  doSomethingElse();
  function doSomethingElse(){
    console.log('I did it!');
  }
  //报错：undefined
  functionVar();
  var functionVar = function(){
    console.log('I did it!');
  }
}
```

13. ES6中的伪强制参数
```js
const _err = function( message ){
//即时抛出错误的方法,参数中的任何一个没有值，参数默认的值将会被使用
  throw new Error( message );
}
const getSum = (a = _err('a is not defined'), b = _err('b is not defined')) => a + b
getSum( 10 ) // throws Error, b is not defined
getSum( undefined, 10 ) // throws Error, a is not defined
```

14. 测量javascript代码块性能的小知识
```js
console.time("Array initialize");
var arr = new Array(100),len = arr.length,i;
for (i = 0; i < len; i++) {
    arr[i] = new Object();
};
console.timeEnd("Array initialize"); 
```

15. 箭头函数
语法: 更少的代码行; 不再需要一遍一遍的打function了
```js
// 一般语法
param => expression
// 多参数
(param1 [, param2]) => expression
// 使用functions
arr.map(function(x) {  return x * x;});
arr.map((x) => x*x);
```
语义: 从上下文中捕获this关键字
```js
// 手动绑定 that = this
function CounterB() {
  this.i = 0;
  var _self = this;
  setInterval(function() {_self.i++;console.log(_self.i);}, 500);
}
// 使用 .bind(this)
function CounterC() {
  this.i = 0;
  setInterval(function() {this.i++;console.log(this.i);}.bind(this),500);
}
// 箭头函数
function CounterD() {
  this.i = 0;
  setInterval(() => {this.i++;console.log(this.i);},500);
}
```

16. 使用indexOf实现contains功能
```js
if ('js rules'.indexOf('js') !== -1) {}
if ('js rules'.indexOf('js') >= 0) {}
if (~['a', 'b', 'c'].indexOf('a'))
```
位操作符 ~,将-1转换为0
```js
!!~'text'.indexOf('tex'); // true
!~'text'.indexOf('tex'); //  false
~'text'.indexOf('asd'); //  false
~'text'.indexOf('ext'); //  true
'something'.includes('thing'); //(ES6) true
```

17. 向回调方法传递参数
```js
function callback(a, b) {return function() {console.log('sum = ',(a+b));}}
var alertText = function(text) {alert(text);};
//使用
alertText.bind(this, 'hello')
```

18. 快速（但危险）的取整方法
数字取整方法：`Math.trunc()`，正数`Math.floor()`而负数`Math.ceil()`
想得到离一个数“最近的整数”，你应该用`Math.round()`而不是`~~`  
`~~`比`Math.trunc()`快,32位以上出现问题
```js
// 数字输入
console.log(~~47.11)  // -> 47
console.log(~~1.9999) // -> 1
console.log(~~3)      // -> 3
//因为~~可以将任何非数字类型转换为0：
console.log(~~[])   // -> 0
console.log(~~NaN)  // -> 0
console.log(~~null) // -> 0
```

19. 不确定类型变量的字符串拼接
```js
var one = 1,two = 2,three = '3';
var result = ''.concat(one, two, three); //"123"
var result = one + two + three; //"33" instead of "123"
```

20. 返回对象，使方法可以链式调用
```js
function Person(name) {
  this.name = name;
  this.sayName = function() {
    console.log("Hello my name is: ", this.name);
    return this;
  };
  this.changeName = function(name) {
    this.name = name;
    return this;
  };
}
var person = new Person("John");
person.sayName().changeName("Timmy").sayName();
```

21. 对数组洗牌
```js
function shuffle(arr) {
    var i,j,temp;
    for (i = arr.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    return arr;    
};
//调用示例:
var a = [1, 2, 3, 4, 5, 6, 7, 8];
var b = shuffle(a);
console.log(b);
// [2, 7, 8, 6, 5, 3, 1, 4]
```

22. 转换为数字的更快方法
```js
var one = '1';
var numberOne = +one;
```

23. 清空数组的两种方法
```js
// 定义一个数组
var list = [1, 2, 3, 4];
function empty() {    list = [];}//引用
empty();
//效率更高
var list = [1, 2, 3, 4];
function empty() {    list.length = 0;}//删除数组里的所有内容,影响到其他引用
empty();
```

24. 使用 === 而不是 ==
== (或者 !=) 操作在需要的情况下自动进行了类型转换  
=== (或 !==)操作不会执行任何转换  
===在比较值和类型时，可以说比==更快 
```js
[10] ==  10      // 为 true
[10] === 10      // 为 false
'10' ==  10      // 为 true
'10' === 10      // 为 false
 []  ==  0       // 为 true
 []  === 0       // 为 false
 ''  ==  false   // 为 true 但 true == "a" 为false
 ''  === false   // 为 false
```
 
25. 立即执行函数表达式
```js
(function() { })()
(abc= function(msg) {   }) (); 
abc(); 
```

26. 过滤并排序字符串列表
```js
var abc = keywords
  .filter(function (keyword, index) {
      return keywords.lastIndexOf(keyword) === index;
    })
  .sort(function (a, b) {
      return a < b ? -1 : 1;
    });
//ES6
const abc = keywords
  .filter((keyword, index) => keywords.lastIndexOf(keyword) === index)
  .sort((a, b) => a < b ? -1 : 1);
```

27. JS中的短路求值
```js
//使用逻辑与 - &&.
var test = true;
// 普通的if语句
if(test){  isTrue(); }
//使用 '&&'
( test && isTrue() );
//使用逻辑或 - ||.
test = false;
if(!test){  isFalse(); }
( test || isFalse()); 
```
逻辑或可以用来给参数设置默认值  
`function theSameOldFoo(name){    name = name || 'Bar' ; }`  
逻辑与可以用来避免调用undefined参数的属性时报错  
`dog&&dog.bark();`  

28. 柯里化(currying)
柯里化将一个二元函数，转变为一元函数，这个函数将返回另一个一元函数
```js
function add(x) {
  return function (y) {return x + y;}
}
add(3)(5);
```

29. 将truthy/falsy转换为布尔值
```js
!!"" // false
!!0 // false
!!null // false
!!undefined // false
!!NaN // false
!!"hello" // true
!!1 // true
!!{} // true
!![] // true
```

30. Map()的营救；使对象属性有顺序
```js
//ES6
var myObject = new Map();
myObject.set('z', 1);
myObject.set('@', 2);
myObject.set('b', 3);
for (var [key, value] of myObject) {  console.log(key, value);}
// 使用分开的数组
var objectKeys = [z, @, b, 1, 5];
for (item in objectKeys) {  myObject[item]}
// 构建一个单属性对象(single-property objects)的数组
var myData = [{z: 1}, {'@': 2}, {b: 3}, {1: 4}, {5: 5}];
```

31. 仅用一行生成`[0, 1, ..., N-1]`数列
```js
// ES5
Array.apply(null, {length: N}).map(Function.call, Number);
Array.apply(null, {length: N}).map(function(value, index){return index;});
//简要说明
Array.apply(null, {length: N}) //返回一个由undefined填充的长度为N的数组
A.map(Function.call, Number) //返回一个长度为N的数组，它的索引为I的元素为Function.call.call(Number, undefined, I, A)的结果。
Function.call.call(Number, undefined, I, A)//可转化为Number(I)，正好就是I。
// ES6
Array.from(new Array(N),(val,index)=>index);
//简要说明
A = new Array(N) //返回一个有N个_小孔_的数组 (例如 A = [,,,...], 但是对于x in 0...N-1时A[x] = undefined)。
F = (val,index)=>index 即 function F (val, index) { return index; }。
Array.from(A, F) //返回一个长度为N的数组，它的索引为I的元素为F(A[I], I)的结果，也就是I。
```

32. 实现异步循环
```js
//自调用函数
for (var i=0; i<5; i++) {
    (function(num){
        setTimeout(function(){
            console.log(num); 
        }, 1000 * (i+1)); 
    })(i);  
}  
//使用let
for (let i=0; i<5; i++) {
    var temp = i;
    setTimeout(function(){
        console.log(i); 
    }, 1000 * (i+1));
}
```

33. 使用JSON.Stringify
```js
var str = JSON.stringify({'prop1': 'value1','prop2': 'value2','prop3': 'value3'}, ['prop1', 'prop2'], '\t\t');
```

34. 数组平均值与中值
```js
let values = [2, 56, 3, 41, 0, 4, 100, 23];
//取平均值
let sum = values.reduce((previous, current) => current += previous);
let avg = sum / values.length;
//取中值：
values.sort((a, b) => a - b);
let lowMiddle = Math.floor((values.length - 1) / 2);
let highMiddle = Math.ceil((values.length - 1) / 2);
let median = (values[lowMiddle] + values[highMiddle]) / 2;
//或者使用无符号右移操作符：
values.sort((a, b) => a - b);
let median = (values[(values.length - 1) >> 1] + values[values.length >> 1])/2
```

35. 计算数组中的最大值/最小值
```js
//内置函数Math.max()和Math.min()
Math.max(1, 2, 3, 4);
Math.min(1, 2, 3, 4);
var numbers = [1, 2, 3, 4];
Math.max.apply(null, numbers) // 4
Math.min.apply(null, numbers) // 1
//ES6
Math.max(...numbers)
Math.min(...numbers)
```

37. 纯JS监听document是否加载完成
```js
//使用document.readyState === 'interactive'监听DOM是否加载完成
if (document.readyState === 'complete') {  // 页面已完全加载}
document.onreadystatechange = () => {  if (document.readyState === 'complete'){  }}};
```

38. 复制到粘贴板
```js
document.querySelector('#input').select();
document.execCommand('copy');
```

39. 逗号操作符
```js
for(var i=0, j=0; i<5; i++, j++, j++){
  console.log("i:"+i+", j:"+j);
}
//当放一个表达式时，它由左到右计算每个表达式，并传回最右边的表达式。
function a(){console.log('a'); return 'a';}
function b(){console.log('b'); return 'b';}
function c(){console.log('c'); return 'c';}
var x = (a(), b(), c());
console.log(x);      // 输出「c」
//逗号（,）在所有的操作符里是最低的优先顺序:没有括号表达式将变为：(x = a()), b(), c();
```

40. break 或 continue 循环函数
```js
const a = [0, 1, 2, 3, 4];
for (var i = 0; i < a.length; i++) {
  if (a[i] === 2) {
    break; // 结束循环
  }
  console.log(a[i]);
}
[0, 1, 2, 3, 4].forEach(function(val, i) {
  if (val === 2) {
    // 实现continue的功能
    return true;
  }
});
const isTwoPresent = [0, 1, 2, 3, 4].some(function(val, i) {
//.every函数同样可以实现此功能。但需要返回与.some相反的布尔值
  if (val === 2) {
    return true; // break
  }
  return false;//continue
});
```

41. 三个实用的javascript小技巧
从后向前获取数组元素
```js
var newArray = [1, 2, 3, 4]
console.log(newArray.slice(-1)) // [4]
console.log(newArray.slice(-2)) // [3, 4]
console.log(newArray.slice(-3)) // [2, 3, 4]
console.log(newArray.slice(-4)) // [1, 2, 3, 4]
```
短路条件句
```js
if (condition) {  dosomething()}
//==
condition && dosomething()
```
用操作符 “||” 来设置默认值
```js
a = a || 'default value'
```

42. 给函数 Bind 对象
我们常常需要将一个对象绑定到一个方法的 this 上。
想要调用一个函数并指定它的 this 时可以使用 bind 方法。

43. Bind 语法
fun.bind(原函数运行时this指向[, arg1[, arg2[, ...]]])
返回由指定的this值和初始化参数改造的原函数拷贝
```js
const myCar = { brand: 'Ford'};
const getBrand = function () {
 console.log(this.brand);
};
getBrand(); // object not bind,undefined
getBrand(myCar); // object not bind,undefined
getType.bind(myCar)(); // Sedan
```

44. 处理 Websocket 超时问题
在 websocket 连接被建立后，如果一段时间未活动，服务器或防火墙可能会超时或终止连接。想要解决这个问题， 我们可以周期性地给服务器发消息。我们需要两个方法实现：一个来确保连接不会中断，，另一个用来取消此设定。同我们也需要一个 timerID 变量.
```js
var timerID = 0; 
function keepAlive() { 
    var timeout = 20000;  
    if (webSocket.readyState == webSocket.OPEN) {  
        webSocket.send('');  
    }  
    timerId = setTimeout(keepAlive, timeout);  
}  
function cancelKeepAlive() {  
    if (timerId) {  
        clearTimeout(timerId);  
    }  
}
```
现在我们实现了我们需要的两个方法，我们可以在 onOpen() 的最后面调用 keepAlive() ，在onClose() 的组后面调用 cancelKeepAlive()。

45. Array 的三个技巧
      1. 迭代一个空数组
      ```js
      const arr = new Array(4);//[undefined, undefined, undefined, undefined]
      arr.map((elem, index) => index);//[undefined, undefined, undefined, undefined]
      const arr = Array.apply(null, new Array(4));
      arr.map((elem, index) => index);//[0, 1, 2, 3]
      ```
      2. 给方法传一个空参数
      如果你想调用一个方法，并不填其中的一个参数时，JavaScript 就会。
      ```js
      method('parameter1', , 'parameter3');//报错
      //解决方法是传递 null 或 undefined
      method('parameter1', null, 'parameter3') // or
      method('parameter1', undefined, 'parameter3');
      method(...['parameter1', , 'parameter3']); // works!
      ```
      3. 数组去重
      ```js
      const arr = [...new Set([1, 2, 3, 3])];//[1, 2, 3]
      ```

46. 使用 tap 来快速 debug
```js
function tap(x) {console.log(x);return x;}.filter(c => tap(c.balance > 25000))
//更先进的 tap
function tap(x, fn = x => x) {console.log(fn(x));return x;}
```

47. 在相等比较中使用 Object.is()
```js
0 == ' ' //true
null == undefined //true
[1] == true //true
NaN === NaN //false
Object.is(0 , ' '); //false
Object.is(null, undefined); //false
Object.is([1], true); //false
Object.is(NaN, NaN); //true
```

48. 赋值技巧
```js
x += 23; // x = x + 23;
y -= 15; // y = y - 15;
z *= 10; // z = z * 10;
k /= 7; // k = k / 7;
p %= 3; // p = p % 3;
d **= 2; // d = d ** 2;
m >>= 2; // m = m >> 2;
n <<= 2; // n = n << 2;
n ++; // n = n + 1;
n --; n = n - 1;
//++ 与 -- 操作符
var a = 2;var b = a++;
// 现在 a == 3  b == 2
//a++做了如下工作：返回a的值,a增加1
var a = 2;var b = ++a;
// 现在a和b都是3
var newValue = (value > 10) ? 5 : 2;
//检测Null、Undefined、空
var variable2 = variable1  || '';
//对象数组
var a = ["myString1", "myString2"];
//关联数组
var skillSet = {
    'Document language' : 'HTML5', 
    'Styling language' : 'CSS3'
};
```

49. 传值机制
```js
var me = {'partOf' : 'A Team'}; 
function myTeam(me) {
    me = {'belongsTo' : 'A Group'}; //对象，创建新的引用
    me.partOf = 'A Group';//基本数据类型，改变值
}
myTeam(me); 
console.log(me);
```

50. Javascript高级特性
```js
var a = {};
Object.defineProperty(a, 'propName', { 
 value: 15,//如果参数不是getter，value是必须的
 writable: false;//只读,只限于基本数据类型
 enumerable:false;//设为隐藏。for ... of和stringify不会包含这些参数,但可从外界访问
 configurable:false;//不能更改
 });
a.propName = 20;
console.log(a.propName); // 15
定义多个：
Object.defineProperties(dest, {
  propA: optionsA,
  propB: optionsB, //...
});
```
私有静态变量
```js
Object.defineProperty(obj, 'myPrivateProp', {value: val, enumerable: false, writable: false, configurable: false});
```
创建getter和setter
```js
function Foobar () {
  var _foo; //  true private property
  Object.defineProperty(obj, 'foo', {
    get: function () { return _foo; }
    set: function (value) { _foo = value }
  });
};
var foobar = new Foobar();
foobar.foo; // 15
foobar.foo = 20; // _foo = 20
```
多层嵌套对象
```js
var obj = {a: {b: {c: [{d: 10}, {d: 20}] } } };
Object.defineProperty(obj, 'firstD', {
  get: function () { return a && a.b && a.b.c && a.b.c[0] && a.b.c[0].d }
});
console.log(obj.firstD); // 10
```

51. 数组去重
```js
//数组只包含原始变量
[ 1, 1, 'a', 'a' ].filter(function (el, i, arr) {
    return arr.indexOf(el) === i;
});
//ES2015
[ 1, 1, 'a', 'a' ].filter( (el, i, arr) => arr.indexOf(el) === i);
//Sets和from方法
var deduped = Array.from( new Set([ 1, 1, 'a', 'a' ]) );
//Objects，使用哈希表
function dedup(arr) {
    var hashTable = {};
    return arr.filter(function (el) {
        var key = JSON.stringify(el);
        var match = Boolean(hashTable[key]);
        return (match ? false : hashTable[key] = true);
    });
}
var deduped = dedup([{ a: 1 },{ a: 1 },[ 1, 2 ],[ 1, 2 ]]);
console.log(deduped); // [ {a: 1}, [1, 2] ]
```

52. 简单获取unix时间戳
```js
const timestamp = Math.floor((+Date.now()) / 1000);
//或
const timestamp = Math.floor(new Date().getTime() / 1000);
```

53. 实用的`log`技巧
```js
//使用条件断点输出log
console.log(data.value) && false
//打印函数到控制台
console.log(funcVariable + '');
```

54. 简单监听DOM事件
```js
//使用引用：
const handler = function () {
  console.log("Tada!")
}
element.addEventListener("click", handler)
// 之后
element.removeEventListener("click", handler)
//命名的函数移除它本身:
element.addEventListener('click', function click(e) {
  if (someCondition) {
    return e.currentTarget.removeEventListener('click', click);
  }
});
//更好的写法：
function handleEvent (eventName, {onElement, withCallback, useCapture = false} = {}, thisArg) {
  const element = onElement || document.documentElement
  function handler (event) {
    if (typeof withCallback === 'function') {
      withCallback.call(thisArg, event)
    }
  }
  handler.destroy = function () {
    return element.removeEventListener(eventName, handler, useCapture)
  }
  element.addEventListener(eventName, handler, useCapture)
  return handler
}
// 你需要的时候
const handleClick = handleEvent('click', {
  onElement: element,
  withCallback: (event) => {
    console.log('Tada!')
  }
})
// 你想删除它的时候
handleClick.destroy()
```

55. 取得文件扩展名
```js
var file1 = "50.xsl";
getFileExtension(file1); //returs xsl
//解决方法 1: 正则表达式
function getFileExtension1(filename) {
  return (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename)[0] : undefined;
}
//解决方法 2: String的split方法
function getFileExtension2(filename) {
  return filename.split('.').pop();
}
//解决方法 3: String的slice、lastIndexOf方法
function getFileExtension3(filename) {
  return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
}
```


56. 函数中如何使用可选参数（包括可选回调函数）
```js
    function example( err, optionalA, optionalB, callback ) {
        // 使用数组取出arguments
        var args = new Array(arguments.length);
        for(var i = 0; i < args.length; ++i) {
            args[i] = arguments[i];
        };        
        // 第一个参数为错误参数
        // shift() 移除数组中第一个参数并将其返回
        err = args.shift();
        // 如果最后一个参数是函数，则它为回调函数
        // pop() 移除数组中最后一个参数并将其返回
        if (typeof args[args.length-1] === 'function') { 
            callback = args.pop();
        }        
        // 如果args中仍有元素，那就是你需要的可选参数
        // 你可以像这样一个一个的将其取出：
        if (args.length > 0) optionalA = args.shift(); else optionalA = null;
        if (args.length > 0) optionalB = args.shift(); else optionalB = null;
        // 像正常一样继续：检查是否有错误
        if (err) { 
            return callback && callback(err);
        }       
    }

    // ES6语法书写更简短
    function example(...args) {
        // 第一个参数为错误参数
        const err = args.shift();
        // 如果最后一个参数是函数，则它为回调函数
        const callback = (typeof args[args.length-1] === 'function') ? args.pop() : null;
        // 如果args中仍有元素，那就是你需要的可选参数你可以像这样一个一个的将其取出：
        const optionalA = (args.length > 0) ? args.shift() : null;
        const optionalB = (args.length > 0) ? args.shift() : null;
        if (err && callback) return callback(err);
    }
```

57. Javascript多维数组扁平化
```js
[[1, 2],[3, 4, 5], [6, 7, 8, 9]]==>[1, 2, 3, 4, 5, 6, 7, 8, 9]
//concat  apply
[].concat.apply([], myArray);
//reduce  concat
myArray.reduce(function(prev,curr){return prev.concat(curr);});
// for 循环
var Array3 = [];
for (var i = 0; i < myArray.length; ++i) {
  for (var j = 0; j < myArray[i].length; ++j)
    Array3.push(myArray[i][j]);
}
 //ES6 
[].concat(...myArray);
console.log(myNewArray4);
```

58. 函数参数内使用解构
```js
// = {}表示此参数需要解构的默认对象是一个{} 无默认值可不用
var sayHello = function({ name , surname = "Moose" } = {}, times) {  console.log(`Hello ${name} ${surname}! How are you?`);};
sayHello({ name: 'John', surname: 'Smith' }, 5678)
```

59. 避免修改和传递`arguments`给其他方法
arguments参数可以让你访问传递给该方法的所有参数。arguments是一个类数组对象；arguments可是使用数组标记访问，而且它有length参数，但是它没有filter、map和forEach这样内建到数组内的方法
将arguments转换为数组的办法
```js
var args = Array.prototype.slice.call(arguments);
var args = [].slice.call(arguments);//slice方法返回一个对arguments浅复制后的数组对象
```

60. 变量声明
```js
var y, x = y = 1 //== var x; var y; x = y = 1
;(() => { 
  var x = y = 2 // == var x; y = 2;
})()
;(() => { //var声明,仅在闭包内有作用
  var x, y = 3 // == var x; var y = 3;
})()
;(() => { 
  var y, x = y = 4 // == var x; var y; x = y = 4  
})()
```








