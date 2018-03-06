---
layout: post
title:  "js的函数式编程"
date:   2018-01-28
desc: "js的函数式编程"
keywords: "js,函数式编程"
categories: [Front]
tags: [js,函数式编程]
icon: icon-javaScript
---
[参考](https://www.gitbook.com/book/llh911001/mostly-adequate-guide-chinese/details){:target="_blank"}  
函数可以像任何其他数据类型一样，可以存在数组里，当作参数传递，赋值给变量...等
# 函数式编程示例
```js
var add = function(x, y) { return x + y };
var multiply = function(x, y) { return x * y };
var flock_a = 4;
var flock_b = 2;
var flock_c = 0;
var result = add(multiply(flock_b, add(flock_a, flock_c)), multiply(flock_a, flock_b));//=>16
// 结合律（assosiative）
add(add(x, y), z) == add(x, add(y, z));
// 交换律（commutative）
add(x, y) == add(y, x);
// 同一律（identity）
add(x, 0) == x;
// 分配律（distributive）
multiply(x, add(y,z)) == add(multiply(x, y), multiply(x, z));
```

# 写函数正确方式
减少代码量，维护和检索代码成本，删除不必要的函数，正确命名参数，不用this

1. 减少代码量
```js
var getServerStuff = function(callback){
return ajaxCall(callback);
};
//重写
var getServerStuff = ajaxCall;
```

2. 维护和检索代码成本，删除不必要的函数
```js
var BlogController = (function() {
var show = function(post) {return Views.show(post);};
var create = function(attrs) {return Db.create(attrs);};
return {show: show, create: create};
})();
//重写,或者直接全部删掉
var BlogController = {show: Views.show, create: Db.create};
```

3. 正确命名参数
```js
httpGet('/post/2', function(json){
return renderPost(json);
});
//添加参数
httpGet('/post/2', function(json, err){
return renderPost(json, err);
});
// 重写
httpGet('/post/2', renderPost);
```

4. 非常小心this（函数式编程不用this）
```js
var fs = require('fs');
// 太可怕了
fs.readFile('freaky_friday.txt', Db.save);
//好一点
fs.readFile('freaky_friday.txt', Db.save.bind(Db));
```

# 纯函数
**纯函数：**对相同的输入能返回相同的输出，自给自足  
**副作用：**更改文件系统，往数据库插入记录，发送一个 http 请求，可变数据，打印/log，获取用户输入，DOM 查询，访问系统状态  
只要是跟函数外部环境发生的交互就都是副作用  
纯函数必须要能够根据相同的输入返回相同的输出；如果函数需要跟外部事物打交道，那么就无法保证这一点了  
```js
var xs = [1,2,3,4,5];
// 纯的
xs.slice(0,3);//=> [1,2,3]
xs.slice(0,3);//=> [1,2,3]
// 不纯的
xs.splice(0,3);//=> [1,2,3]
xs.splice(0,3);//=> [4,5]
// 不纯的
var minimum = 21;
var checkAge = function(age) {return age >= minimum;};
// 纯的
var checkAge = function(age) {
var minimum = 21;
return age >= minimum;
};
```

## 追求“纯”的理由

1. 可缓存性
```js
var squareNumber = memoize(function(x){ return x*x; });
squareNumber(4);//=> 16
squareNumber(4);//=> 16 // 从缓存中读取输入值为 4 的结果
//简单实现
var memoize = function(f) {
var cache = {};
return function() {
var arg_str = JSON.stringify(arguments);
cache[arg_str] = cache[arg_str] || f.apply(f, arguments);
return cache[arg_str];
};
};
```

2. 通过延迟执行把不纯的函数转换为纯函数
```js
var pureHttpCall = memoize(function(url, params){
return function() { return $.getJSON(url, params); }
});
```

3. 纯函数是完全自给自足的，它需要的所有东西都能轻易获得，纯函数对于其依赖必须要诚实。
```js
// 不纯的
var signUp = function(attrs) {
var user = saveUser(attrs);
welcomeUser(user);
};
var saveUser = function(attrs) {
var user = Db.save(attrs);
//...
};
var welcomeUser = function(user) {
Email(user, ...);
//...
};
// 纯的
var signUp = function(Db, Email, attrs) {
return function() {
var user = saveUser(Db, attrs);
welcomeUser(Email, user);
};
};
var saveUser = function(Db, attrs) {
//...
};
var welcomeUser = function(Email, user) {
//...
};
```
并行运行任意纯函数,纯函数不需要访问共享的内存
**合理性:**等式推导带来的分析代码的能力对重构和理解代码非常重要

# curry 
只传递给函数一部分参数来调用它，让它返回一个函数去处理剩下的参数
```js
var add = function(x) {
return function(y) {return x + y;};
};
add(1)(2);// 3
```

# 代码组合
```js
var compose = function(f,g) {
return function(x) {
return f(g(x));
};
};
var toUpperCase = function(x) { return x.toUpperCase(); };
var exclaim = function(x) { return x + '!'; };
var shout = compose(exclaim, toUpperCase);
shout("send in the clowns");
```

# pointfree  
pointfree 模式指的是，永远不必说出你的数据,减少不必要的命名，让代码保持简洁和通用
```js
// 非 pointfree，因为提到了数据：word
var snakeCase = function (word) {
return word.toLowerCase().replace(/\s+/ig, '_');
};
// pointfree
var snakeCase = compose(replace(/\s+/ig, '_'), toLowerCase);
//trace  函数允许我们在某个特定的点观察数据
var dasherize = compose(join('-'), toLower, trace("after split"), split(' '), replace(/\s{2,}/ig, ' '));
// after split [ 'The', 'world', 'is', 'a', 'vampire' ]
```

# 范畴学
```js
var g = function(x){ return x.length; };
var f = function(x){ return x === 4; };
var isFourLetterWord = compose(f, g);
```

# 声明式代码
指明的是做什么，不是怎么做.不指定执行顺序
```js
// 命令式
var makes = [];
for (i = 0; i < cars.length; i++) {
makes.push(cars[i].make);
}
// 声明式
var makes = cars.map(function(car){ return car.make; });
// 命令式
var authenticate = function(form) {
var user = toUser(form);
return logIn(user);
};
// 声明式
var authenticate = compose(logIn, toUser);
```

# 容器
控制流（controlflow）、异常处理（error handling）、异步操作（asynchronous actions）和状态（state）、作用（effects）

## 简单示例
```js
var Container = function(x) {
this.__value = x;
}
//构造器
Container.of = function(x) { return new Container(x); };
//functor
Container.prototype.map = function(f){
//在不离开  Container  的情况下操作容器里面的值
//对于函数运用的抽象。当map一个函数的时候，我们请求容器来运行这个函数
return Container.of(f(this.__value))
}
//一直调用map,就是个组合（composition）
Container.of(2).map(function(two){ return two + 2 })//=> Container(4)
```
 
## 薛定谔的 Maybe
最常用在那些可能会无法成功返回结果的函数中
```js
Container.prototype.isNothing = function() {
return (this.__value === null || this.__value === undefined);
}
Container.prototype.map2 = function(f) {
return this.isNothing() ? Container.of(null) : Container.of(f(this.__v
alue));}
```

## 释放容器里的值
```js
// maybe :: b -> (a -> b) -> Maybe a -> b
var maybe = curry(function(x, f, m) {
return m.isNothing() ? x : f(m.__value);
});
// getTwenty :: Account -> String
var getTwenty = compose(maybe("You're broke!", finishTransaction), withdraw(20));
```

## 异步
```js
var getJSON = curry(function(url, params) {
return new Task(function(reject, result) {
$.getJSON(url, params, result).fail(reject);
});
});
getJSON('/video', {id: 10}).map(_.prop('title'));
```


