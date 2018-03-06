---
layout: post
title:  "VUE2常用指令"
date:   2017-11-25
desc: "VUE2常用指令"
keywords: "前端,VUE2,directive,指令"
categories: [Front]
tags: [前端,VUE2,directive,指令]
icon: icon-vue
---
# 内置指令
1、响应并更新DOM特性；`v-bind:class="[isActive ? 'active' : '']"`  
2、监听DOM事件；`v-on:click  v-on:keyup  @click`  
3、数据双向绑定；`<input v-model="message">`  
4、条件渲染指令(display): `v-show`  
5、条件渲染指令: 

   ```html
    <div v-if="status === 'loading'">
        <div class="alert alert-info">loading</div>
    </div>
    <div v-else-if="status === 'ready'">
        <div class="alert alert-success">ready</div>
    </div>
    <div v-else>
        <div class="alert alert-danger">fail</div>
    </div>
   ```
6、循环指令:`<li v-for="(item,index) in todos"></li>`  
7、更新元素的textContent；`<span v-text="msg"></span>  <span>{{msg}}</span>`  
8、更新元素的innerHTML；`<h1 v-html="'<small>使用v-html渲染</small>'"></h1>`  
9、跳过元素以及子元素的编译过程，加快项目编译速度：`<span v-pre>\{\{ compiled \}\}</span>`；  
10、v-cloak：不需要表达式，这个指令保持在元素上直到关联实例结束编译；  
11、只渲染元素或组件一次: `<div v-once>{{ once }}</div>`


# 自定义指令
1. 定义
```js
Vue.directive('demo', {
     // deep: true, //相关属性也是一个对象
     twoWay: true, //双向绑定
     acceptStatement: true, //让指令像 v-on 一样接受内联语句
     // isLiteral: true, //值被看成字符串,不会建立数据监视 
     //<div v-my-directive="a++"></div>     
      bind: function (el, binding, vnode, oldVnode) {
            console.log('初始化');
            var s = JSON.stringify
            el.innerHTML =
             'name: '       + s(binding.name) + '<br>' +
             'value: '      + s(binding.value) + '<br>' +
             'expression: ' + s(binding.expression) + '<br>' +
             'argument: '   + s(binding.arg) + '<br>' +
             'modifiers: '  + s(binding.modifiers) + '<br>' +
             'vnode keys: ' + Object.keys(vnode).join(', ')
            this.handler = function() {
                 this.set(this.el.value) //赋值
             }.bind(this);
                this.el.addEventListener('input', this.handler)
        },
        inserted: function (el){
            console.log('元素插入父节点时调用');
        },
        update: function (el, binding, vnode, oldVnode){
            console.log('模板更新时调用');
            // this.vm.$emit('crop', event)       
        },
        componentUpdated: function (el){
            console.log('模板完成一次更新周期');
        },
        unbind: function (el){
            console.log('指令与元素解绑');
                    // this.vm.$off('rotate')
        this.el.removeEventListener('input', this.handler)
        }
});
```
简写：
```js
Vue.directive('demo', function (el, binding) {
  el.style.backgroundColor = binding.value
})
```
2. 使用  
```html
    <div id="app" v-demo:foo.a.b="message"></div>
```








