---
layout: post
title:  "Vue2+express 前后端同构"
date:   2017-11-27
desc: "Vue2+express 前后端同构"
keywords: "前端,VUE2,Vuex2,Webpack2,同构"
categories: [Front]
tags: [前端,VUE2,Vuex2,Webpack2,同构]
icon: icon-html
---
原文：[无痛学会各种 2 的 Vue2+Vuex2+Webpack2 前后端同构渲染](https://segmentfault.com/a/1190000007244289)
## 初始化项目
```shell
mkdir vue2Isom&&cd vue2Isom 
npm init -y
# 依赖包
npm install --save express serialize-javascript vue vue-server-renderer vuex
npm install --save-dev autoprefixer babel-core babel-loader babel-preset-es2015 babel-preset-stage-2 cross-env css-loader extract-text-webpack-plugin file-loader url-loader vue-loader webpack webpack-dev-middleware webpack-hot-middleware vue-template-compiler
# 项目结构
mkdir build dist files src src\components src\store&&touch build\setup-dev-server.js build\vue-loader.config.js build\webpack.base.config.js build\webpack.client.config.js build\webpack.server.consig.js files\gener.html src\components\list.vue src\store\index.js src\app.js src\App.vue src\client-entry.js src\index.html src\server-entry.js .babelrc .gitignore server.js
```
## 编写文件
### 1. app.js:逻辑入口
```js
import Vue from 'vue'
import App from './App.vue'
import store from './store'
const app = new Vue({
    store,
    ...App
})
export { app, store }
```
### 2. App.vue

```html
    <template>
        <div id="app">
            <div class="c">
                App Component
                <div @click='testClick' class="a"> click me!</div>
                <div class="b">{{a}}</div>
                <List></List>
            </div>
        </div>
    </template>
    <script>
    import List from './components/List.vue'
    export default {
        data() {
            return {
                a: 11
            }
        },
        methods: {
            testClick() {
                this.a = Math.random();
            }
        },
        components: {
            List
        }
    }
    </script>
    <style lang="css" scoped>
    .a {
        background: blue;
        margin-bottom: 10px;
        color: white;
        cursor: pointer;
    }
    .b {
        background: red;
        margin-bottom: 10px;
    }
    .c {
        background: lightblue;
    }
    </style>
```
### 3. list.vue

```html
    <template>
        <div class="d">
            <div>list component</div>
            <div class="e">{{list.length}} </div>
            <div>
                <div class="btn" @click='replaceList'>replace list</div>
                <div class="btn"  @click='addItem'>add</div>
            </div>
            <ul>
                <li v-for='item in list'>{{item}}</li>
            </ul>
        </div>
    </template>
    <script type="text/javascript">
        import {mapState,mapMutations,mapAction} from 'vuex'
        export default {
            computed: mapState(['count','list'])
            methods:{
                ...mapMutations(['addItem']),
                ...mapActions(['replaceList'])
            }
        }
    </script>
    <style type="text/css" scoped="">
        .btn {
            display: inline-block;
            cursor: pointer;
            padding: 10px;
            background: rosybrown;
            margin: 10px;
        }
        .e{
            background: lightsalmon;
            margin: 10px;
        }
        .d{
            margin: 10px;
            background: lightcoral;
        }
    </style>
```
### 4. store/index.js

```js
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex);
const store = new Vuex.Store({
    //全局的状态存储
    state: {
        list: [1, 2, 3],
        count: 1
    },
    //不直接修改state，通过commit调用mutations修改数据,可以异步
    actions: {
        replaceList: context => {
            var t = [];
            let i = 0;
            while (i < 7) {
                t.push(Math.random());
                i++;
            }
            setTimeout(() => {
                context.commit('replaceList', 1)
            }, 1000)
        }
    },
    //唯一可以修改数据的地方,通过commit发射事件调用,不可以异步
    mutations: {
        replaceList: (state, payload) => {
            console.log(state, payload);
            var t = [];
            t.push(payload);
            state.list = t;
        },
        addItem: state => {
            console.log(state);
            state.list.push(Math.random());
        }
    },
    //对获取的数据进行加工
    getters: {
        cc: state => {
            return state.count + "  hello!";
        }
    }
})
export default store;
```
### 5. client-entry.js:前端代码入口

```js
import { app, store } from './app'
//将服务端渲染的时候的状态写入vuex
if (window._INIT_STATE_) {
    store.replaceState(window._INIT_STATE_);
}
//挂载到dom元素
app.$mount('#app');
```
### 6. server-entry.js:后端代码入口

```js
import { app, store } from './app'
export default context => {
    //保存现有的store 状态
    context.initialState = store.state;
    return app;
}
```
### 7. index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>vue2 + webpack2 + ssr</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
   {{ STYLE }}
  </head>
  <body>
    {{ APP }}
    <script src="/dist/client-vendor-bundle.js"></script>
    <script src="/dist/client-bundle.js"></script>
  </body>
</html>
```
### 8. server.js：express 应用
```js
process.env.VUE_ENV = 'server';
const isProd = process.env.NODE_ENV === 'production';
const fs = require('fs');
const path = require('path');
const resolve = file => path.resolve(__dirname, file);
const express = require('express');
const serialize = require('serialize-javascript');
const createBundleRenderer = require('vue-server-renderer').createBundleRenderer;
const app = express();
//将html文件切割为头尾两部分,生成文件的时进行拼接
const html = (() => {
    const template = fs.readFileSync(resolve('./src/index.html'), 'utf-8')
    const i = template.indexOf('{{ APP }}')
    //如果是开发调试状态,css会直接插入页面中,而不是应用文件
    const style = isProd ? '<link rel="stylesheet" href="/dist/styles.css">' : ''
    return {
        head: template.slice(0, i).replace('{{ STYLE }}', style),
        tail: template.slice(i + '{{ APP }}'.length)
    }
})();

let renderer;
if (isProd) {
    //如果是生产环境,bundle是构建完成的正式文件
    const bundlePath = resolve('./dist/server-bundle.js')
    renderer = createRenderer(fs.readFileSync(bundlePath, 'utf-8'))
} else {

    //如果是开发环境,bundle会在改变之后重新回调生成
    require('./build/setup-dev-server')(app, bundle => {
        renderer = createRenderer(bundle)
    })
}

function createRenderer(bundle) {
    return createBundleRenderer(bundle);
}
app.use('/dist', express.static(resolve('./dist')))
app.get("/file", (req, res) => {
    //这个接口用于在真是环境中生成静态页面
    if (!isProd) {
        res.end("please run this api on the product environment");
        return;
    }
    if (!renderer) {
        return res.end("waiting for compilation... refresh in a moment.");
    }
    const context = {};
    //调用renderToString 一次性生成文件
    renderer.renderToString(context, (error, htmltext) => {

        var s = html.head + htmltext + html.tail;

        fs.writeFile(resolve("./files/gener.html"), s, () => {
            res.end("OK");
        })
    });
});
app.get('/', (req, res) => {
    if (!renderer) {
        return res.end('waiting for compilation... refresh in a moment.')
    }
    const context = {}
    //调用 renderToSStream 流式渲染
    const renderStream = renderer.renderToStream(context)
    let firstChunk = true
    res.write(html.head)
    renderStream.on('data', chunk => {
        if (firstChunk) {
            // embed initial store state
            if (context.initialState) {
                res.write(
                    `<script>window._INIT_STATE_=${
                        serialize(context.initialState, {isJSON: true})
                        }</script>`
                )
            }
            firstChunk = false
        }
        res.write(chunk)
    })
    renderStream.on('end', () => {
        res.end(html.tail)
    })
})
const port = process.env.PORT || 9090
app.listen(port, () => {
    console.log(`server started at localhost:${port}`)
})
```
### 9. files/gener.html
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>vue2 + webpack2 + ssr</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
    <link rel="stylesheet" href="/dist/styles.css">
</head>

<body>
    <div id="app" server-rendered="true">
        <div class="c">
            this is the App.vue Component
            <div class="a"> Click me! Change the &#x27;a&#x27; Value</div>
            <div class="b"> the &#x27;a&#x27; value is 11</div>
            <div class="d" data-v-e6efd4e8>
                <div data-v-e6efd4e8>this is the List.vue component</div>
                <div class="e" data-v-e6efd4e8>the list length is : 9</div>
                <div data-v-e6efd4e8>
                    <div class="btn" data-v-e6efd4e8>click to replace list after 1s </div>
                    <div class="btn" data-v-e6efd4e8>click to add item</div>
                </div>
                <ul data-v-e6efd4e8>
                    <li data-v-e6efd4e8>1</li>
                    <li data-v-e6efd4e8>23</li>
                    <li data-v-e6efd4e8>4</li>
                    <li data-v-e6efd4e8>5</li>
                    <li data-v-e6efd4e8>6</li>
                    <li data-v-e6efd4e8>7</li>
                    <li data-v-e6efd4e8>7</li>
                    <li data-v-e6efd4e8>8</li>
                    <li data-v-e6efd4e8>8</li>
                </ul>
            </div>
        </div>
    </div>
    <script src="/dist/client-vendor-bundle.js"></script>
    <script src="/dist/client-bundle.js"></script>
</body>
</html>
```

## 编译及打包
###  1. .babelrc：es6 编译
```
{
  "presets": [
    ["es2015", { "modules": false }],
    "stage-2"
  ]
}
```
### 2. vue-loader.config.js
```js
module.exports = {
  postcss: [
    require('autoprefixer')({
      browsers: ['last 3 versions']
    })
  ],
}
```
### 3. setup-dev-server.js:webpack开发服务器
```js
const path = require('path');
const webpack = require('webpack');
const MFS = require('memory-fs');
const clientConfig = require('./webpack.client.config');
const serverConfig = require('./webpack.server.config');

// 开发调试的server-bundle
module.exports = function setupDevServer(app, onUpdate) {
    clientConfig.entry.app = ['webpack-hot-middleware/client', clientConfig.entry.app]
    clientConfig.plugins.push(
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin()
    )

    const clientCompiler = webpack(clientConfig)
    app.use(require('webpack-dev-middleware')(clientCompiler, {
        publicPath: clientConfig.output.publicPath,
        stats: {
            colors: true,
            chunks: false
        }
    }))
    app.use(require('webpack-hot-middleware')(clientCompiler))

    const serverCompiler = webpack(serverConfig)
    const mfs = new MFS()
    const outputPath = path.join(serverConfig.output.path, serverConfig.output.filename)
    serverCompiler.outputFileSystem = mfs
    serverCompiler.watch({}, (err, stats) => {
        if (err) throw err
        stats = stats.toJson()
        stats.errors.forEach(err => console.error(err))
        stats.warnings.forEach(err => console.warn(err))
        onUpdate(mfs.readFileSync(outputPath, 'utf-8'))
    })
}
```
### 4. webpack.base.config.js
```js
const path = require('path');
const vueConfig = require('./vue-loader.config');
module.exports = {
    devtool: '#source-map',
    entry: {
        app: './src/client-entry.js',
        vendor: ['vue', 'vuex']
    },
    output: {
        path: path.resolve(__dirname, '../dist'),
        publicPath: '/dist/',
        filename: 'client-bundle.js'
    },
    module: {
        rules: [{
                test: /\.vue$/,
                loader: 'vue-loader',
                options: vueConfig
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'url',
                options: {
                    limit: 10000,
                    name: '[name].[ext]?[hash]'
                }
            }
        ]
    }
}
```
### 5. webpack.client.config.js
```js
const webpack = require('webpack');
const base = require('./webpack.base.config');
const vueConfig = require('./vue-loader.config');
//生成 前端文件的webpack 配置
const config = Object.assign({}, base, {
    plugins: (base.plugins || []).concat([
        // strip comments in Vue code
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
        }),

        //将类库文件进行分开打包,便于缓存
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'client-vendor-bundle.js'
        })
    ])
})
if (process.env.NODE_ENV === 'production') {
    const ExtractTextPlugin = require('extract-text-webpack-plugin')
    vueConfig.loaders = {
        css: ExtractTextPlugin.extract({
            loader: "css-loader!stylus-loader",
            fallbackLoader: "vue-style-loader" // <- this is a dep of vue-loader
        })
    }
    config.plugins.push(
        new ExtractTextPlugin('styles.css'),
        //minifying CSS
        new webpack.LoaderOptionsPlugin({
            minimize: true
        }),
        // minify JS
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        })
    )
}
module.exports = config
```
### 6. webpack.server.config.js
```js
const webpack = require('webpack');
const base = require('./webpack.base.config');
module.exports = Object.assign({}, base, {
    target: 'node',
    devtool: false,
    entry: './src/server-entry.js',
    output: Object.assign({}, base.output, {
        filename: 'server-bundle.js',
        libraryTarget: 'commonjs2'
    }),
    externals: Object.keys(require('../package.json').dependencies),
    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
            'process.env.VUE_ENV': '"server"'
        })
    ]
})
```
### 7. package.json
```json
"scripts": {
    "dev": "node server",
    "start": "cross-env NODE_ENV=production node server",
    "build": "npm run build:client && npm run build:server",
    "build:client": "cross-env NODE_ENV=production webpack --config build/webpack.client.config.js --progress --hide-modules",
    "build:server": "cross-env NODE_ENV=production webpack --config build/webpack.server.config.js --progress --hide-modules"
  }
```





