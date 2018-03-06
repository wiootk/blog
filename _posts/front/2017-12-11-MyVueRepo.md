---
layout: post
title:  "vue组件库开发"
date:   2017-12-11
desc: "vue组件库开发"
keywords: "前端,自制,vue,组件库"
categories: [Front]
tags: [前端,自制,vue,组件库]
icon: icon-html
---
**问题描述：**  
在我们开发中，尽管有大厂开源的组件库支持，但是根据业务等还需要我们自己造轮子来适应项目，满足需求。一般公司都会使用同一套相同或类似的框架，当再次出现组件库不足时，就会重复造轮子（或拷贝）。基于这种情况，我们可以开发自己的组件库，作为大厂组件库的补充，发布到npm（或私服），使得公司所有项目都可以使用，不再重复造轮子。  
本文就是从零开始一步步搭建Vue 组件库的详细实践笔记  
**参考：**  
[从零开始搭建Vue组件库 VV-UI](https://www.cnblogs.com/tiedaweishao/p/7825997.html){:target="_blank"}  
[打包 Vue 组件库的正确姿势](http://cnodejs.org/topic/5833e104bde2b59e06141e16){:target="_blank"}

# 初始化项目
## 1. 脚手架
```shell
 npm install --global vue-cli
 vue init webpack my-repo
 cd my-repo
 # chromedriver 安装报错
 npm install chromedriver --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
 npm install
 # less 依赖
 npm install --save-dev  less less-loader
 npm run dev
```

## 2. 项目结构
```
├── examples      # 原src目录:示例展示
│   ├── component
│   │    └── demo-block.vue   
│   ├── docs
│   │    └──  test.md  
│   ├── router
│   ├── App.vue
│   └── main.js
├── packages        # 存放组件
│   ├── button
│   │   ├── src                # 组件文件夹
│   │   │    ├── button.vue
│   │   │    └── button.scss
│   │   └──index.js            # 组件的出口
│   ├── styles                 # 公用的 css 样式文件
│   ├── theme                 # 主题样式
│   │     ├── src
│   │     │    ├── button.css
│   │     │    ├── common.css
│   │     │    └── index.css
│   │     ├── gulpfile.js
│   │     ├── package.json
│   │     └── salad.config.json
│   └── index.js               # 插件的出口
```

1. 改造： `mv src examples && mkdir packages theme\src`  
         *`ren src examples` 也是重命名(cmd)*
2. 修改文件(`build/webpack.base.conf.js 、 bulid/vue-loader.conf.js`): 把指向src的目录改成examples
3. 编译目录 build/webpack.base.conf.js
```js
{
   test: /\.js$/,
   loader: 'babel-loader',
   include: [resolve('examples'), resolve('test'), resolve('packages')]
}
```

# 编写markdown文档
## 1. 解析工具  
1. 安装依赖 `npm install --save-dev vue-markdown-loader`  
2. build/webpack.base.conf.js  
```js
rules: [
   {
     test: /\.md$/,
     loader: 'vue-markdown-loader'
   }
 ]
```

## 2. 写文档  
1. 创建文件： `mkdir examples\docs&&touch examples\docs\test.md`  
```md
# test
> Hello World
```
2. 增加路由指向：`examples/router/index.js`  
```js
{
  path: '/test',
  name: 'test',
  component: r => require.ensure([], () => r(require('../docs/test.md')))
}
```
3. 启动：`npm start`  
4. 浏览器: `http://localhost:8080/#/test`  

    *eslint*

1.  关闭eslint  
在 `build/webpack.base.conf.js` 中注释掉`eslint-loader rules`  
2.  修改配置文件 .eslintrc.js  
```js
module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
     //设置"script"（默认）或"module"
    sourceType: 'module'
  },
  env: {
    browser: true,
  },
  extends: 'standard',
  // required to lint *.vue files
  plugins: [
    'html'
  ],
  'rules': {
    // allow paren-less arrow functions
    'arrow-parens': 0,
    // allow async-await
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    "no-unused-vars": [2, { 
      // 允许声明未使用变量
      "vars": "local",
      // 参数不检查
      "args": "none" 
    }],
    // 关闭语句强制分号结尾
    "semi": [0],
    //空行最多不能超过100行
    "no-multiple-empty-lines": [0, {"max": 100}],
    //关闭禁止混用tab和空格
    "no-mixed-spaces-and-tabs": [0],
  }
}
```

## 3. 识别代码块:做演示+显示演示代码  

1. 首先把内容里面vue片段编译成html，用于显示，另一方面用highlight来高亮代码块  
安装依赖: `npm install markdown-it-container --save-dev`  
build/webpack.base.conf.js  
```js
onst wrapCustomClass = function (render) {
  return function (...args) {
    return render(...args)
      .replace('<code class="', '<code class="hljs ')
      .replace('<code>', '<code class="hljs">')
  }
}
const convertHtml = function (str) {
  return str.replace(/(&#x)(\w{4});/gi, $0 => String.fromCharCode(parseInt(encodeURIComponent($0).replace(/(%26%23x)(\w{4})(%3B)/g, '$2'), 16)))
}
const cheerio = require('cheerio')
const striptags = (str, tags) => {
  const $ = cheerio.load(str, { decodeEntities: false })
  if (!tags || tags.length === 0) {
    return str
  }
  tags = !Array.isArray(tags) ? [tags] : tags
  let len = tags.length
  while (len--) {
    $(tags[len]).remove()
  }
  return $.html()
}
const MarkdownItContainer = require('markdown-it-container')
const vueMarkdown = {
  preprocess: (MarkdownIt, source) => {
    MarkdownIt.renderer.rules.table_open = function () {
      return '<table class="table">'
    }
    MarkdownIt.renderer.rules.fence = wrapCustomClass(MarkdownIt.renderer.rules.fence)
    return source
  },
  use: [
    [MarkdownItContainer, 'demo', {
      // 用于校验包含demo的代码块
      validate: params => params.trim().match(/^demo\s*(.*)$/),
      render: function(tokens, idx) {
        
        var m = tokens[idx].info.trim().match(/^demo\s*(.*)$/);

        if (tokens[idx].nesting === 1) {
          var desc = tokens[idx + 2].content;
          // 编译成html
          const html = convertHtml(striptags(tokens[idx + 1].content, 'script'))
          // 移除描述，防止被添加到代码块
          tokens[idx + 2].children = [];
          var returnStr= `<demo-block>
                        <div slot="desc">${html}</div>
                        <div slot="highlight">`
          console.log(tokens[idx + 1].content);
          return returnStr;
        }
        return '</div></demo-block>\n';
      }
    }]
  ]
}
// ...
{
    test: /\.md$/,
    loader: 'vue-markdown-loader',
    options: vueMarkdown
 }
```

2. touch examples/components/demo-block.vue
   ```html
   <template>
     <div class="docs-demo-wrapper">
       <div :style="{maxHeight: isExpand ? '700px' : '0'}" class="demo-container">
           <div span="14">
             <div class="docs-demo docs-demo--expand">
               <div class="highlight-wrapper">
                 <slot name="highlight"></slot>
               </div>
             </div>
           </div>
         </div>
       <span class="docs-trans docs-demo__triangle" @click="toggle">\{\{isExpand ? '隐藏代码' : '显示代码'\}\}</span>
     </div>
   </template>
   <script>
     /* eslint-disable */
     import Vue from 'vue'
     export default {
       data() {
         return {
           isExpand: false
         };
       },
       methods: {
         toggle() {
           this.isExpand = !this.isExpand;
         }
       }
     };
   </script>
   <style lang="less" type="text/less">
     .demo-container {
       transition: max-height .3s ease;
       overflow: hidden;
     }
     .docs-demo {
       width: 100%;
       min-height: 60px;
       box-sizing: border-box;
       font-size: 14px;
       background-color: #F7F7F7;
       border: 1px solid #e2ecf4;
       border-top: none;
       pre code {
         font-family: Consolas,Menlo,Courier,monospace;
         line-height: 22px;
         border: none;
       }
     }
     .docs-trans {
       width: 100%;
       text-align: center;
       display: inline-block;
       color: #C5D9E8;
       font-size: 12px;
       padding: 10px 0;
       background-color: #FAFBFC;
     }
     .docs-demo__code,
     .highlight-wrapper,
     .docs-demo__meta {
       padding: 0 20px;
     }
     .docs-demo__code {
       border-bottom: 1px solid #eee;
     }
     .docs-demo.docs-demo--expand .docs-demo__meta {
       border-bottom: 1px dashed #e9e9e9;
     }
     .docs-demo.docs-demo--expand .docs-demo__triangle {
       transform: rotate(180deg);
     }
     .highlight-wrapper {
       display: none;
       p,
       pre {
         margin: 0;
       }
       .hljs {
         padding: 0;
       }
     }
     .docs-demo.docs-demo--expand .highlight-wrapper {
       display: block;
     }
     .docs-demo__code__mobi {
       height: 620px;
       margin: 20px 0;
     }
     .docs-demo__code__mobi__header {
       border-radius: 4px 4px 0 0;
       background: -webkit-linear-gradient(rgba(55,55,55,.98),#545456);
       background: linear-gradient(rgba(55,55,55,.98),#545456);
       text-align: center;
       padding: 8px;
       img {
         width: 100%;
       }
       .url-box {
         height: 28px;
         line-height: 28px;
         color: #fff;
         padding: 0 3px;
         background-color: #a2a2a2;
         margin: 10px auto 0;
         border-radius: 4px;
         white-space: nowrap;
         overflow-x: auto;
       }
     }
     .docs-demo__code__mobi__content {
       iframe {
         width: 100%;
         border: 0;
         height: 548px;
       }
     }
   </style>
   ```

3. 编写组件  
**3.1** 编写：`mkdir packages\button\src&&touch packages\button\src\button.vue`
   ```html
   <template>
     <button @click="$emit('click')" class="m_button" :disabled="disabled"
       :class="['m_button--'+type,{'is-plain': plain, 'is-disabled': disabled, 'is-round': round},'m_button--size-'+size]">
       <i v-if="icon !== ''" :class="icon"></i>
       <slot></slot>
     </button>
   </template>
   <script>
     export default{
       name: 'MButton',
       props: {
         type: {
           type: String,
           default: 'default'
         },
         size: {
           type: String,
           default: 'default'
         },
         icon: {
           type: String,
           default: ''
         },
         plain: Boolean,
         disabled: Boolean,
         round: Boolean
       },
       data () {
         return {
           msg: 'button'
         }
       }
     }
   </script>
   ```
**3.2** 导出 ：`touch packages\button\index.js`  
   ```js
   import Button from './src/button.vue';
   Button.install = function (Vue) {
     Vue.component(Button.name, Button);
   };
   export default Button;
   ```
**3.3** 全局引入+按需加载:`touch packages\index.js`  
   ```js
   import Button from './button/index.js';
   const components = [Button];
   //全局引入
   const install = function(Vue) {
     if (install.installed) return;
     components.map(component => Vue.component(component.name,component));
   };
   if (typeof window !== 'undefined' && window.Vue) {
     install(window.Vue);
   }
   //导出 全局+按需加载
   export default {install,Button};
   ```
**3.4** 引入组件：examples\main.js  
   ```js
   import demoBlock from './components/demo-block.vue'
   import MUI from '../packages/index'
   // import '../packages/theme-default/lib/index.css'
   Vue.component('demo-block', demoBlock)
   Vue.use(MUI)
   ```
**3.5** 修改 examples\docs\test.md  
   ```md
   <m-button type='success'>默认</m-button>
   <m-button size='sm'>小型</w-button>
   ::: demo
    //```html    
       <m-button type='success'>默认</m-button>
       <m-button size='sm'>小型</m-button>    
    //```
    :::
   ```
**3.6** 运行： `npm start `  

# 样式冲突,采用BEM规范  
*使用gulp+postcss构建样式文件*

1. 安装 gulp
```shell
npm install --global gulp
cd packages/theme&&npm init
npm install --save-dev gulp gulp-cssmin gulp-postcss postcss-salad
```
2. 修改 package.json
```json
"main": "index.css",
  "scripts": {
    "dev": "gulp build && gulp watch",
    "build": "gulp build"
  }
```
3. postcss-salad配置文件：`touch salad.config.json`  
```json
{
  "browsers": ["ie > 8", "last 2 versions"],
  "features": {
    "bem": {
      "shortcuts": {
        "component": "b",
        "modifier": "m",
        "descendent": "e"
      },
      "separators": {
        "descendent": "_",
        "modifier": "--"
      }
    }
  }
}
```
4. `touch gulpfile.js`
```js
var gulp = require('gulp');
var postcss = require('gulp-postcss');
var cssmin = require('gulp-cssmin');
var salad = require('postcss-salad')(require('./salad.config.json'));
gulp.task('compile', function() {
  return gulp.src('./src/*.css')
    .pipe(postcss([salad]))
    .pipe(cssmin())
    .pipe(gulp.dest('./lib'));
});
gulp.task('copyfont', function() {
  return gulp.src('./src/fonts/**')
    .pipe(cssmin())
    .pipe(gulp.dest('./lib/fonts'));
});
gulp.task('build', ['compile', 'copyfont']);
gulp.task('watch', function () {
  gulp.watch('./src/*.css', ['compile']);
});
```
5. 编写样式文件  
touch src/index.css  
```css
@import "button.css";
```
touch src/common.css  
```css
:root {
  --color-primary: #3FAAF5;
  --border-radius-base: 4px; 
  --size-base: 14px;
  --button-font-size: 14px;
  --button-border-radius: var(--border-radius-base); 
  --color-success: #13ce66;
  --color-white: #fff;
  --button-default-fill: var(--color-white); 
  --border-width-base: 1px;
  --border-style-base: solid;
  --color-primary: #3FAAF5;
  --color-base-black: color(var(--color-primary) h(+6) s(33%) l(18%));
  --border-color-base: color(var(--color-base-black) s(26%) l(80%));
  --border-base: var(--border-width-base) var(--border-style-base) var(--border-color-base);
  --button-default-color: var(--color-base-black);
}
```
touch src/button.css  
```css
@import "common.css";
@b m {
  @e button {
    cursor: pointer;
    border-radius: var(--border-radius-base);
    padding: 12px 20px;
    font-size: 14px;
    @m size-sm {
      padding: 9px 15px;
      font-size: 12px;
      border-radius: 3px;
    }
    @m size-default {
      padding: 12px 20px;
      font-size: 14px;
    }
    @m default {
      background: var(--button-default-fill);
      border: var(--border-base);
      color: var(--button-default-color);
    }
    @m success {
      background: var(--color-success);
      &:hover,
      &:focus {
        opacity: 0.7;
      }
      &:disabled {
        opacity: 0.3;
      }
      @when plain {
        background: rgba(var(--color-success), 0.05);
        border-color: rgba(var(--color-success), 0.8);
        color: var(--color-success);
      }
    }
    &.is-round {
      border-radius: 20px;
    }
  }
}
```
6. 生成文件: `gulp build`
7. 使用文件：examples/main.js:`import '../packages/theme/lib/index.css'`

# 打包 Vue 组件库
~~修改build/webpack.base.config.js~~  
修改 build/webpack.pronf.conf.js  
1. 组件库输入/输出:
```js
 entry: {
    app: './packages/index.js'
  },
  output: {
    path: config.build.assetsRoot,
    filename: utils.assetsPath('js/myrepo.js'),
    chunkFilename: utils.assetsPath('js/[id].js'),   
    library: 'myrepo',       // 模块名称
    //CMD只能在 Node 环境执行，AMD 只能在浏览器端执行，UMD 同时支持两种执行环境
    // “var” “this” “commonjs” “commonjs2” “amd” “umd”
    libraryTarget: 'umd',   // 输出格式
    umdNamedDefine: true    // 是否将模块名称作为 AMD 输出的命名空间
  },
// 设置 打包时不分离文件:new webpack.optimize.CommonsChunkPlugin
```
2. 打包组件依赖：修改build/webpack.base.config.js  
```js
externals:{
    vue:{
        root: 'Vue',
        commonjs: 'vue',
        commonjs2: 'vue',
        amd: 'vue'
    }
}
```
3. package.jsom  
    指定入口主文件:`"module": "dist/static/js/myrepo.js",`  
    不打包vue-router:把依赖放到`devDependencies`  

# 使用
1. 上传到私服  
 touch packages/theme/.gitignore
 ```
 node_modules/
 ```
 上传参照[私服搭建](http://localhost:4000/blog/back/2017/12/09/nuxus.html#4npm私服){:target="_blank"}  
 删除 package.json的`"private": true,`  
 发布：`npm publish --registry http://localhost:8234/repository/npm-my`  
2. 下载使用  
 新建项目
```shell
 vue init webpack test
 cd test
 # chromedriver 安装报错
 npm install chromedriver --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
 npm install
 npm install --save my-repo
```
使用：main.js
```js
// import myrepo from '../node_modules/my-repo/dist/static/js/my-repo'
import MUI from 'my-repo'
import '../node_modules/my-repo/packages/theme/lib/index.css' // 引入样式库
Vue.use(MUI)
```
hello.vue
   ```html
   <m-button type='success'>默认</m-button>
   <m-button size='sm'>小型</w-button>
   ```







