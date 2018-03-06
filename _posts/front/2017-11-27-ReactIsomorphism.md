---
layout: post
title:  "koa2+react 同构实践"
date:   2017-11-27
desc: "koa2+react 同构实践"
keywords: "前端,Koa2,React,同构"
categories: [Front]
tags: [前端,Koa2,React,同构]
icon: icon-html
---
本demo旨在一步步搭建 koa2+react 同构实践 ，koa2与react 仅是简短的涉及使用  
**同构的优势**  
首屏性能  
SEO / 搜索引擎爬虫支持  
无缝的用户体验  
**参考文章**   
 [React koa2 同构应用实践](https://www.tuicool.com/articles/B7Zzemn)  
 [React服务器端渲染](http://testudy.cc/tech/2017/09/22/react-server-render.html)  

# 1. 项目结构
```
├── src
│   ├── common
│   │    ├── actions
│   │    ├── components
│   │    ├── reducers
│   │    ├── config
│   │    ├── store
│   │    │      └── configureStore.js
│   │    ├── webpack.base.js
│   │    └── router.js 
│   ├── browser
│   │    ├── config
│   │    ├── app.js
│   │    └── webpack.config.js 
│   └── server
│        ├── middleware
│        ├── models
│        ├── controllers
│        ├── services
│        ├── templates
│        │      ├── 404.ejs
│        │      ├── 500.ejs
│        │      └── index.ejs
│        ├── app.js
│        ├── config.js
│        └── webpack.config.js
├── static
│   ├── img
│   ├── style
│   ├── js
│   └── favicon.ico
│── package.json
└── webpack.config.js
```

```sh
mkdir koa2React &&cd koa2React && npm init -y
mkdir src static && touch webpack.config.js
cd src&& mkdir common browser server browser/config&&touch browser/app.js browser/webpack.config.js&& cd ../common && mkdir actions components reducers routes store config&&touch webpack.base.js router.js&& cd ../server &&mkdir controllers middleware models services templates&&touch app.js config.js webpack.config.js &&cd templates&&touch 404.ejs 500.ejs index.ejs&& cd ../../..
cd static&& mkdir img style js &&touch favicon.ico&&cd ..
```

# 2. koa2
1. `npm i --save koa koa-bodyparser koa-mysql-session koa-router koa-session-minimal koa-static koa-views md5 moment mysql ejs`
2. touch src/server/config.js
```js
const config = {
  // 启动端口
  port: 5555, 
  showSql:true,
  // 数据库配置
  database: {
    DATABASE: 'demo2',
    USERNAME: 'root',
    PASSWORD: 'root',
    PORT: '3306',
    HOST: 'localhost'
  }
} 
module.exports = config
```
3. touch src/server/app.js  
```js
var Koa=require('koa');
var path=require('path')
var bodyParser = require('koa-bodyparser');
var ejs=require('ejs');
var session = require('koa-session-minimal');
var MysqlStore = require('koa-mysql-session');
var config = require('./config.js');
// var router=require('koa-router')
var views = require('koa-views')
var koaStatic = require('koa-static')
var app=new Koa() 
// session存储配置
const sessionMysqlConfig= {
  user: config.database.USERNAME,
  password: config.database.PASSWORD,
  database: config.database.DATABASE,
  host: config.database.HOST,
}
// 配置session中间件
app.use(session({
  key: 'USER_SID',
  store: new MysqlStore(sessionMysqlConfig)
})) 
// 配置静态资源加载中间件
app.use(koaStatic(
  path.join(__dirname , '../../static')
)) 
// 配置服务端模板渲染引擎中间件
app.use(views(path.join(__dirname, './templates'), {
  extension: 'ejs'
})) 
// 使用表单解析中间件
app.use(bodyParser()) 
// 使用新建的路由文件
// app.use(require('https://segmentfault.com/routers.js').routes())
const router = require('./controllers/routeUtil')
app.use(router.routes())
  .use(router.allowedMethods())
console.log(`server  listening on port ${config.port}`)
// 监听在3000端口
app.listen(config.port)
```
4. touch src/server/controllers/routeUtil.js  
```js
const Router = require('koa-router')
const router = new Router()
const fs = require('fs');
let addControllers = (router, dir) => {
    dir = dir || '';
    fs.readdirSync(__dirname + '/' + dir).filter((f) => {
        return f.endsWith('.js');
    }).forEach((f) => {
        const model = require(__dirname + '/' + dir + '/' + f);
        if (model.constructor == Router) {
          // constructor 更加精确地指向对象所属的类，而对 instanceof 而言，即使是父类也会返回true
            const modelStr = f.replace(/.js/, '');
            router.use(`/${modelStr}`, model.routes(), model.allowedMethods());
        }
    })
}
addControllers(router);
module.exports = router
```
5. touch src/server/controllers/user.js
```js
var router = require('koa-router')();
const userService = require('./../services/user.js');
router.get('/:id', async function(ctx, next) {
    let userInfo =await userService.getUserById(ctx.params.id);
    await ctx.render('user', { 'user': userInfo })     
})
router.post('/save', async function(ctx, next) { 
let userInfo = await userService.insertUser(ctx.request.body);
    let userList =await userService.findAllUser();
    //console.log(userList);
    let html = '<html><body>' +
        '<div> userList:&nbsp;<br/>' + userList + '</div>' +
        '</body></html>';
    ctx.response.type = 'text/html';
    ctx.response.body = html;
})
module.exports = router;
```
6. touch src/server/services/user.js
```js
const userDao = require('./../models/user.js');
var getUserById = async (userId) => {
    var users =await userDao.getUserById(userId);
    return users;
}
var findAllUser = async (userId) => {
    var users =await userDao.findAllUser(userId);
    var responseContent = '';
    for(let user of users) {
        responseContent += '姓名：' + user.name + '&nbsp;&nbsp;|&nbsp;&nbsp;';
        responseContent += 'id：' + user.id + '<br />';
    }
    return responseContent;
}
var insertUser = async (user) => {
    return userDao.insertUser(user);   
}
module.exports = {
    getUserById : getUserById,
    findAllUser : findAllUser,
    insertUser : insertUser
};
```
7. touch src/server/models/mysqlUtil.js
```js
var mysql = require('mysql');
var config = require('../config.js')
var pool = mysql.createPool({
    host: config.database.HOST,
    user: config.database.USERNAME,
    password: config.database.PASSWORD,
    database: config.database.DATABASE
});
let query = function(sql, values) {
    if (config.showSql) {
        console.log(sql, values)
    }
    return new Promise((resolve, reject) => {
        pool.getConnection(function(err, connection) {
            if (err) {
                resolve(err)
            } else {
                connection.query(sql, values, (err, rows) => {
                    if (err) {
                        reject(err)
                    } else {
                        resolve(JSON.parse(JSON.stringify(rows)))
                    }
                    connection.release()
                })
            }
        })
    })
}
let createTable = function(sql) {
    return query(sql, [])
}
module.exports = {
    query,
    createTable
}
```
8. touch src/server/models/user.js
```js
var util = require('./mysqlUtil.js')
let user=`create table if not exists user(
  id int(11) NOT NULL,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
);` 
// 建表
let createUserTable=util.createTable(user)
// 添加用户
let insertUser = function( value ) {
  let _sql = "insert into user(name,id) values(?,?);"
  return util.query( _sql, [value.name,value.id] )
}
// 查找用户
let getUserById = async  function (  id ) {
  let _sql = `SELECT * from user where id="${id}"`
  var aaa=await util.query( _sql);
  return await aaa[0];
}
// 查找用户列表
let findAllUser = function ( ) {
  let _sql = `SELECT * from user`
  return util.query( _sql)
} 
module.exports={
  createUserTable,
  insertUser,
  getUserById,
  findAllUser
}
```
9.  模板  
touch src/server/templates/header.ejs  
```
    <meta charset="UTF-8">
    <title>Document</title>
    <link rel="stylesheet" href="/index.css">
    <script src="http://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
```
touch src/server/templates/footer.ejs  
```
    foot
```
touch src/server/templates/user.ejs  
```
    <% include header %>
        <div class="container">
           <div>
                <label>用户名：</label> 
                <span><%= user.name %></span>
           </div>
           <div>
                <label>ID：</label> 
                <span><%= user.id %></span>
           </div>
        </div>
    <% include footer %>
```
10. nodemon自动重启node服务  
依赖 `npm install nodemon -g`  
修改package.json  
```
"scripts": {
     "server": "nodemon src/server/app.js"
  } 
```
启动：npm run server –>访问 http://localhost:5555/user/1  
post  http://localhost:5555/user/save  {"name":"abcd","id":"7"}

# 3. react
  ```
  npm install --save react react-dom babel-polyfill react-router react-router-dom redux react-redux redux-logger bootstrap
  npm install --save-dev webpack webpack-dev-server babel-core babel-loader babel-runtime babel-plugin-transform-runtime babel-preset-es2015  babel-preset-react babel-preset-stage-2 copy-webpack-plugin
  ```

1. touch src/common/webpack.base.js
```js
const webpack = require('webpack');
const rootDir = process.cwd();
const copyPlugin = require('copy-webpack-plugin');
module.exports = {
 entry: __dirname + '/app.js',
 output: {
     path: rootDir+'/build/browser',
     filename: "bundle.js"
 },
 module: {
     rules: [{
         test: /\.js$/,
         exclude: /node_modules/,
         loader: 'babel-loader',
         query: {
             plugins: ['transform-runtime'],
             presets: ['es2015', 'react', 'stage-2']
         }
     }, {
         test: /\.css$/,
         loader: "style-loader!css-loader"
     }]
 },
 devServer: {
        historyApiFallback: true,
        noInfo: true,
        port: 3344,
        host:'172.168.1.70'
    },
    plugins: [
        new copyPlugin([{
    from: rootDir + '/index.html',
    to:rootDir+'/build/browser'
        }])
    ],
     devtool: '#eval-source-map'
};
```
2. touch src/browser/webpack.config.js
```js
const webpackBase = require('../common/webpack.base');
const rootDir = process.cwd();
const plugins =Object.assign({}, webpackBase.plugins) ;
module.exports =Object.assign({}, webpackBase,{ entry: __dirname + '/app.js',plugins:plugins})
```
3. package.json
```
 "scripts": {
    "server": "nodemon src/server/app.js",
    "client": "webpack-dev-server --hot --inline --colors --content-base  --open --config src/browser/webpack.config.js ",
    "build:client": "webpack --progress --colors  --hide-modules --config src/browser/webpack.config.js ./build/browser"
  }
```
4. touch index.html  
    ```html
     <!DOCTYPE html>
     <html lang="en">
     <head>
       <meta charset="UTF-8">
       <title>Document</title>
       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
     </head>
     <body>
       <div id="app"></div>
       <script src="bundle.js"></script>
     </body>
     </html>
    ```
5. touch src/browser/app.js
    ```js
    // // import {render} from 'react-dom';
    // import ReactDOM from 'react-dom';
    // import React from 'react'
    // const List = (props) => { 
    // const list = props.listItems.map((el,i)=>(
    //     /*<li key={i} onClick={props.onClick.bind(null, i)}><h2>{el}</h2></li>*/
    //     <li key={i} onClick={() => props.onClick(i)}><h2>{el}</h2></li>
    //   ));
    //    return (<div><ul> { list }</ul></div>)
    //  };
    // class App extends React.Component {
    //   componentWillMount(){
    //      this.setState({list: ['thing1', 'thing2', 'thing3']})
    //    };
    // addList = (i) => {
    //   // event.target.value
    //   this.setState((state)=>({list: [...state.list,'thing4' ]})) 
    // };
    // render(){ 
    //      return(
    //        <div className="row">
    //    <div className="col-md-10 col-md-offset-1">
    //        <div className="panel panel-default">
    //            <div className="panel-body">
    //             <h1  onClick={this.addList} >add list</h1>
    //            <hr/>
    //              <List listItems={this.state.list} onClick={this.addList} />
    //            </div>
    //        </div>
    //    </div>
    //    </div>
    //      );
    //    }
    //  }
    //  ReactDOM.render(<App/>, document.getElementById('app'));
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { Provider } from 'react-redux';
    import UserContainer from '../common/containers/userContainer';
    import configureStore from '../common/store/configureStore';
    import Route from '../common/router' //路由配置
    const store = configureStore();
    // <Provider store={store}>        
    //   <UserContainer />
    // </Provider>
    class App extends React.Component {
    render(){
        return(
        <Provider store={store}> 
        <Route/> 
        </Provider>
        );
    }
    }
    ReactDOM.render(<App/>, document.getElementById('app'));
    // 热替换HMR，需要加入这段代码才会进行生效
    if(module.hot)
        module.hot.accept();
    ```
5. touch src/common/actions/user.js
```js
export const ADD_USER = 'ADD_USER';
export const ALL_USER = 'ALL_USER';
export const GET_USER = 'GET_USER';
export function listUser(list){
  return {
    type: ALL_USER,
    list
  }
}
export function addUser(value) {
  return {
    type: ADD_USER,
    value
  }
}
export function getUser(id) {
  return {
    type: GET_USER,
    id
  }
}
```
6. touch src/common/reducers/user.js
```js
import {ADD_USER,ALL_USER,GET_USER} from '../actions/user'
const initialState = {
  list:  ['thing1', 'thing2', 'thing3'],
  newUser:"名字1"
};
export default function reducer(state = initialState, action){
  switch (action.type){
  case ADD_USER:
    return Object.assign({},state,
      {list: [...state.list, action.value]}
    );
  case ALL_USER:
   return Object.assign({},state,  {list: [...action.list]}   ); 
 case GET_USER:
    return Object.assign({},state,{list: [...state.list, action.value]}); 
  default:
    return state;
  }
}
```
7. touch src/common/store/configureStore.js
```js
import { createStore, applyMiddleware, combineReducers } from 'redux';
// createStore 初始化store的函数, applyMiddleware 添加中间件,combineReducers把多个reducers合并为单一实体
import { createLogger } from 'redux-logger';
import user from '../reducers/user';
const reducer = combineReducers({ user});
const loggerMiddleware = createLogger();
const createStoreWithMiddleware = applyMiddleware( loggerMiddleware)(createStore); 
const configureStore = (initialState) => createStoreWithMiddleware(reducer, initialState);
export default configureStore;
```
8. touch src/common/components/Input.js
    ```js
    import React from 'react';
    const Input = ({ onChange, onSubmit, value }) => (
    <form onSubmit={onSubmit}>
        <div className="form-group">     
        <input value={value} onChange={onChange} type="text" className="form-control"  placeholder="添加用户" />
        <button className="btn btn-primary"> Add </button>
        </div>
    </form>
    )
    export default Input;
    ```
9. touch src/common/components/List.js  
```js
import React from 'react';
import {BrowserRouter, Route, Link} from 'react-router-dom'
const List = (props) => {
        // 本例使用\{\{\}\}代表占位符，请去掉 \
const list = props.listItems.map((el,i)=>(
    <li key={i} ><h2>{el}<span className="badge"><Link to={`/info/${i}`} params=\{\{id: 12\}\}>info</Link></span></h2></li>
    // onClick={props.onClick.bind(null, i)}  onClick={() => props.onClick(i)} onClick={() => props.showInfo(i)
  ));
   return (<div><ul> { list }</ul></div>)
 };
 export default List;
```
10. touch src/common/components/userComponent.js
```js
import React from 'react';
import List from './List';
import Input from './Input';
class UserContainer extends React.Component {
  constructor(props){super(props);}
    // 'http://localhost:5555/api/list'
  componentDidMount = () => { 
    fetch(`http://localhost:5555/api/list`)
      .then(res => res.json())
      .then(json=>{
         let array=[''];
         for(let i in json){
            array.push(json[i].name);
            }
          this.props.listUser(array);
      });
  }
  inputChange = (event) => {
    this.props.addUser(event.target.value)
  }
  listUser = () => {
    // event.preventDefault();
    this.props.listUser();
  };
  addUser = (event) => {
    // event.target.value
    this.props.addUser("555")
  };
  getUser = (i) => {
    this.props.getUser(i)
  };
  render(){
    return (
      <div className="row">
         <div className="col-md-10 col-md-offset-1">
            <div className="panel panel-default">
              <div className="panel-body">
                <h1  onClick={this.addUser} >add list</h1>
                <hr/>
                <List listItems={this.props.user.list} onClick={this.addUser} showInfo={this.getUser} />
                <Input value={this.props.user.newUser}  onChange={this.inputChange} onSubmit={this.addUser} />
              </div>
            </div>
          </div>
      </div>
    );
  }
}
export default UserContainer;
```
11.  touch src/common/components/InfoComponent.js
```js
import React from 'react';
import List from './List';
import Input from './Input';
class Info extends React.Component {
  constructor(props){
        super(props);
        this.state = {user:{id:'55',name:'initName'}};
            }
    // 'http://localhost:5555/api/list'
componentDidMount = () => {
  let id = this.props.match.params.id
    fetch(`http://localhost:5555/api/${id}`)
      .then(res => res.json())
      .then(json=>{this.setState({user:json   });
      });
  }
  render(){
    return (
      <div className="row">
        {console.log(this.props.match.params.id)}
         <div className="col-md-10 col-md-offset-1">
            <div className="panel panel-default">
              <div className="panel-body">
                <h1 >info - {this.props.match.params.id}</h1>
                <hr/>
                <label>{this.state.user.id}</label> &#12288;<span>{this.state.user.name}</span><br/> 
              <label>lable</label ><span onChange={this.inputChange}>{this.props.user.newUser}</span>                
              </div>
            </div>
          </div>
      </div>
    );
  }
}
export default Info;
```
12. touch src/common/containers/InfoContainer.js
```js
import { connect } from 'react-redux';
import InfoComponent from '../components/InfoComponent.js'
import {listUser,addUser,getUser} from '../actions/user'
function mapStateToProps(state) {
  return {
    user: state.user
  }
}
//mapping actions to props
function mapDispatchToProps(dispatch) {
  return {  
    getUser: (i) => dispatch(getUser(i))
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(InfoComponent);
```
13. touch src/common/containers/userContainer.js
```js
import { connect } from 'react-redux';
import userComponent from '../components/userComponent.js'
import {listUser,addUser,getUser} from '../actions/user'
function mapStateToProps(state) {
  return {
    user: state.user
  }
}
//mapping actions to props
function mapDispatchToProps(dispatch) {
  return {
    listUser: (list) => dispatch(listUser(list)),
    addUser: (value) => dispatch(addUser(value)),   
    getUser: (i) => dispatch(getUser(i))
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(userComponent);
```
14. touch src/common/router.js
    ```js
    import React, {Component, PropTypes} from 'react';
    import {BrowserRouter, Route, Link} from 'react-router-dom'
    import UserContainer from './containers/userContainer';
    import InfoContainer from './containers/InfoContainer.js';
    // var history = process.env.NODE_ENV !== 'production' ? browserHistory : hashHistory;
    // 本例使用\{\{\}\}代表占位符，请去掉 \
    const Links = () => (
            <ul className="nav">
                <li style=\{\{'float':'left','listStyle':'none'\}\}><Link to="/">列表</Link></li>  
                <li style=\{\{'float':'left','listStyle':'none'\}\}><Link to=\{\{pathname: '/info'\}\}>详情</Link> </li> 
                <li style=\{\{'float':'left','listStyle':'none'\}\}> <Link replace to="/contact">Contact</Link> </li>          
                </ul>  
    )
    const route = () => (
    <BrowserRouter>
        <div className="contentBox"> 
        <Links />      
        <Route exact path="/" component={UserContainer} />
        <Route path="/info/:id?" component={InfoContainer} />
        <Route path="/contact" render={() => <h1>Contact</h1>} />      
        </div>
    </BrowserRouter>
    )
    export default route;
    ```
15.修改 koa2  
    15.1 app.js  
    npm install --save koa2-cors
    ```js
    var cors = require('koa2-cors');   
    app.use(cors());
    ```
    15.2 修改 services/user.js   
    ```js
    var findAllUser2 = async (userId) => {
    return await userDao.findAllUser(userId); 
    }
    ```
    15.2 touch src/server/controllers/api.js
    ```js
    var router = require('koa-router')();
    const userService = require('./../services/user.js');
    router.get('/list', async function(ctx, next) {
        ctx.response.body = await userService.findAllUser2();
    })
    router.get('/:id', async function(ctx, next) {
        ctx.response.body=  await userService.getUserById(ctx.params.id);
    })
    module.exports = router;
    ```
16. 启动 npm run server、npm run client  
    启动文件 start.bat  
    ```shell
    @echo off  
    start cmd /k "npm run  server" 
    start cmd /k "npm run  client" 
    ```

## redux 与 koa2 异步数据
`npm install redux-thunk --save`

1.  common/store/configureStore.js  
```js
import { createStore, applyMiddleware, combineReducers } from 'redux';
// createStore 初始化store的函数, applyMiddleware 添加中间件,combineReducers把多个reducers合并为单一实体
import { createLogger } from 'redux-logger';
import user from '../reducers/user';
import thunk from 'redux-thunk';
const reducer = combineReducers({ user});
const loggerMiddleware = createLogger();
//const createStoreWithMiddleware = applyMiddleware( loggerMiddleware)(createStore); 
const createStoreWithMiddleware = applyMiddleware( loggerMiddleware,thunk)(createStore); 
const configureStore = (initialState) => createStoreWithMiddleware(reducer, initialState);
export default configureStore;
```
2. common/actions/user.js
```js
export function getUserAsync(id){
    return function(dispatch) {
      fetch(`http://localhost:5555/userData/${id}`)
      .then(res => res.json())
      .then(json=> dispatch({type: 'GET_USER', newUser: json}))
      .catch(err => console.log(err));
    }
}
```
3. common/containers/InfoContainer.js
```js
import { connect } from 'react-redux';
import InfoComponent from '../components/InfoComponent.js'
// import {listUser,addUser,getUser} from '../actions/user'
import {listUser,addUser,getUser,getUserAsync} from '../actions/user'
function mapStateToProps(state) {
  return {
    user: state.user
  }
}
//mapping actions to props
function mapDispatchToProps(dispatch) {
  return {  
    getUser: (i) => dispatch(getUser(i)),
    getUserAsync:(i)=>dispatch(getUserAsync(i))
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(InfoComponent);
```
4. common/reducers/user.js
```js
import {ADD_USER,ALL_USER,GET_USER} from '../actions/user'
const initialState = {
  list:  ['thing1', 'thing2', 'thing3'],
  newUser:"名字1"
};
export default function reducer(state = initialState, action){
  switch (action.type){
  case ADD_USER:
    return Object.assign({},state,
      {list: [...state.list, action.value]}
    );
  case ALL_USER:
    return {list: [...action.list]} 
 case GET_USER:
    // return Object.assign(
    //   {},
    //   state,
    //  {list: [...state.list, action.value]}
    // ); 
    return Object.assign({}, state, {newUser: action.newUser}); 
  default:
    return state;
  }
}
```
5. common/components/InfoComponent.js
```js
import React from 'react';
import List from './List';
import Input from './Input';
class Info extends React.Component {
  constructor(props){
        super(props);
        this.state = {user:{id:'55',name:'initName'}};
            }
    // 'http://localhost:5555/api/list'
componentDidMount = () => {
  let id = this.props.match.params.id
    fetch(`http://localhost:5555/api/${id}`)
      .then(res => res.json())
      .then(json=>{this.setState({user:json   });
      });
  }
  render(){
    return (
      <div className="row">
        {console.log(this.props.match.params.id)}
         <div className="col-md-10 col-md-offset-1">
            <div className="panel panel-default">
              <div className="panel-body">
                <h1 >info - {this.props.match.params.id}</h1>
                <hr/>
              组件内：<label>{this.state.user.id}</label> &#12288;<span>{this.state.user.name}</span><br/>
              redux： <label>{this.props.user.newUser.id}</label> &#12288;<span onChange={this.inputChange}>{this.props.user.newUser.name}</span>                                  
              </div>
            </div>
          </div>
      </div>
    );
  }
}
export default Info;
```

# 3. 同构
## 1. 关键要素
   ```
   1. DOM 的一致性:在前后端渲染相同的 Compponent，将输出一致的 Dom 结构。
   2. 不同的生命周期:在服务端上Component生命周期只会到componentWillMount，客户端则是完整的
   3.客户端 render 时机:同构时，服务端结合数据将 Component 渲染成完整的 HTML字符串并将数据状态返回给客户端，客户端会判断是否可以直接使用或需要重新挂载
   React的状态和渲染
   1. 在组件的componentWillMount方法中执行容器组件中的异步获取数据方法；
   2. 随后执行render方法，此时虽然尚未获得数据，当渲染出第一版页面；
   3. 数据从服务器端返回，组件props更新；
   4. 重新调用render方法，呈现最终页面；
   5. 随着用户的交互（比如输入新的条件，重新执行步骤1、3、4；跳转新的URL地址，重新执行步骤1、2、3、4）。这个步骤在浏览器端独立发起，和步骤4中的最终页面是两个阶段的状态。
   ``` 
## 2. 在nodejs端使用es6  
`npm install --save-dev babel-register`  
1. server根目录新建: touch .babelrc
    ``` 
    {  
    "presets":["es2015","react","stage-2"],  
    "plugins":["transform-runtime"],
    "ignore": ["/(.css|.less)$/"],
    "only": "/src/"
    }
    ```
2. 编辑 server/app.js(入口文件不能写es6和jsx!!!)
    ```js
    require('babel-polyfill')
    var fs = require('fs');  
    var babelConfig = JSON.parse(fs.readFileSync('./.babelrc')); 
    require('babel-register')(babelConfig);
    //require('ignore-styles');
    //服务器端支持fetch
    global.fetch = require('node-fetch');
    global.window=global;
    global.window.isServer=true;
    ```

## 3. 浏览器端改造
1. 改造路由  
common/router.js
    ```js
    import React, {Component, PropTypes} from 'react';
    import {BrowserRouter, Route, Link, Redirect,StaticRouter} from 'react-router-dom'
    import UserContainer from './containers/userContainer';
    import InfoContainer from './containers/InfoContainer.js';
    import { Provider, connect } from 'react-redux';
    import configureStore from './store/configureStore';
    const store = configureStore(window.__INITIAL_STATE__);
    export const config = [
        { exact: true, path: '/', component: UserContainer },
        { exact: true, path: '/info/:id', component: InfoContainer },
        { exact: true, path: '/contact',  render: () => <h1>Contact</h1> } ];
        // 本例使用\{\{\}\}代表占位符，请去掉 \
    const Links = () => (
            <ul className="nav">
                <li style=\{\{'float':'left','listStyle':'none'\}\}><Link to="/">列表</Link></li>  
                <li style=\{\{'float':'left','listStyle':'none'\}\}><Link to=\{\{pathname: '/info'\}\}>详情</Link> </li> 
                <li style=\{\{'float':'left','listStyle':'none'\}\}> <Link replace to="/contact">Contact</Link> </li>          
                </ul>  
            )
    export const Routes = (props) =>{
    const Router =window.isServer ? StaticRouter: BrowserRouter;
    return (
    <Provider store={props.store}> 
    <Router location={props.location} context={props.context}>
        <div className="contentBox"> 
        <Links />      
        {  config.map((item, index) => (<Route key={index} {...item} />)) }   
            
        </div>
    </Router>
    </Provider>
        )
    }
    ```
browser/app.js  
    ```js
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { Provider } from 'react-redux';
    import UserContainer from '../common/containers/userContainer';
    import configureStore from '../common/store/configureStore';
    import {Routes} from '../common/router' //路由配置
    const store = configureStore(window.__INITIAL_STATE__);
    if (window.isServer) {
        ReactDOM.hydrate(<Routes store={store} />, document.getElementById('app'));
    } else {
        ReactDOM.render(<Routes store={store} />, document.getElementById('app'));
    }
    // 热替换HMR，需要加入这段代码才会进行生效
    if(module.hot)
        module.hot.accept();
    ```
2. 改造组件（初始化数据）  
common/containers/infoContainer.js
    ```js
    import { connect } from 'react-redux';
    import { withRouter } from 'react-router-dom';
    import InfoComponent from '../components/InfoComponent.js'
    import {getUser,getUserAsync,fetchGetUser} from '../actions/user'
    
    function getInitData(dispatch, params) {
        const id = params.id;
        return () => dispatch(fetchGetUser(id));
    }
    
    function mapStateToProps(state,ownProps) {
    return {
        user: state.user
    }
    }
    //mapping actions to props
    function mapDispatchToProps(dispatch, ownProps) {
    return {  
        getUser: (i) => dispatch(getUser(i)),
        getUserAsync:(i)=>dispatch(getUserAsync(i)),
        fetchGetUser: getInitData(dispatch, ownProps.match.params),
    };
    }
    const InfoContainer = withRouter(connect(mapStateToProps, mapDispatchToProps)(InfoComponent));
    InfoContainer.getInitData = getInitData;
    export default InfoContainer;
    ```    
common/containers/userContainer.js
    ```js
    import { connect } from 'react-redux';
    import { withRouter } from 'react-router-dom';
    import userComponent from '../components/userComponent.js'
    import {listUser,addUser,getUser,fetchListUser} from '../actions/user'
    
    function getInitData(dispatch, params) {
        return () => dispatch(fetchListUser());
    }
    function mapStateToProps(state,ownProps) {
    return {
        user: state.user
    }
    }
    //mapping actions to props
    function mapDispatchToProps(dispatch,ownProps) {
    return {
        listUser: (list) => dispatch(listUser(list)),
        addUser: (value) => dispatch(addUser(value)),   
        getUser: (i) => dispatch(getUser(i)),
        fetchListUser: getInitData(dispatch, ownProps.match.params),
    };
    }
    
    const UserContainer = withRouter(connect(mapStateToProps, mapDispatchToProps)(userComponent));
    UserContainer.getInitData = getInitData;
    export default UserContainer;
    ```
common/actions/user.js
    ```js
    export function fetchGetUser(id) {
        return (dispatch) => {
            return fetch(`http://localhost:5555/api/${id}`)
            .then(res => res.json())
            .then(json => dispatch(getUser(json)))
            .catch(err => console.log(err));
        };
    };
    export function fetchListUser() {
        return (dispatch) => {
            return fetch(`http://localhost:5555/api/list`)
            .then(res => res.json())
            .then(json => dispatch(listUser(json)))
            .catch(err => console.log(err));
        };
    };
    ```
common/components/InfoComponent.js
    ```js
    import React from 'react';
    import List from './List';
    import Input from './Input';
    class Info extends React.Component {
    constructor(props){
            super(props);
            this.state = {user:{id:'55',name:'initName'}};       
                }
        // 'http://localhost:5555/api/list'
    // componentDidMount = () => {
    //   let id = this.props.match.params.id
    //     fetch(`http://localhost:5555/api/${id}`)
    //       .then(res => res.json())
    //       .then(json=>{this.setState({user:json   });
    //       });
    //   }
    
    componentDidMount() {
            // if (!this.props.user) {
                this.props.fetchGetUser();
    
            // }
        }
    
    render(){
        return (
        <div className="row">
            {console.log(this.props.match.params.id)}
            <div className="col-md-10 col-md-offset-1">
                <div className="panel panel-default">
                <div className="panel-body">
                    <h1 >info - {this.props.match.params.id}</h1>
                    <hr/>
                    组件内：<label>{this.props.user.id}</label> &#12288;<span>{this.props.user.name}</span><br/>
                </div>
                </div>
            </div>
        </div>
        );
    }
    }
    export default Info;
    ```
common/components/userComponent.js
    ```js
    import React from 'react';
    import List from './List';
    import Input from './Input';
    class UserContainer extends React.Component {
    constructor(props){super(props);}
        // 'http://localhost:5555/api/list'
    // componentDidMount = () => { 
    //     fetch(`http://localhost:5555/api/list`)
    //       .then(res => res.json())
    //       .then(json=>{
    //          let array=[''];
    //          for(let i in json){
    //             array.push(json[i].name);
    //             }
    //           this.props.listUser(array);
    //       });
    //   }
    
    componentDidMount() {
            // if (!this.props.fetchListUser) {//服务端
                this.props.fetchListUser();
            // }
        }
    
    inputChange = (event) => {
        this.props.addUser(event.target.value)
    }
    listUser = () => {
        // event.preventDefault();
        this.props.listUser();
    };
    addUser = (event) => {
        // event.target.value
        this.props.addUser("555")
    };
    getUser = (i) => {
        this.props.getUserAsync(i)
    };
    render(){
        return (
        <div className="row">
            <div className="col-md-10 col-md-offset-1">
                <div className="panel panel-default">
                <div className="panel-body">
                    <h1  onClick={this.addUser} >add list</h1>
                    <hr/>
                    <List listItems={this.props.user.list} onClick={this.addUser} showInfo={this.getUser} />
                    <Input value={this.props.user.newUser}  onChange={this.inputChange} onSubmit={this.addUser} />
                </div>
                </div>
            </div>
        </div>
        );
    }
    }
    export default UserContainer
    ```
common/reducers/user.js
    ```js
    import {ADD_USER,ALL_USER,GET_USER} from '../actions/user'
    const initialState = {
    list:  ['thing1', 'thing2', 'thing3'],
    newUser:"名字1"
    };
    export default function reducer(state = initialState, action){
    switch (action.type){
    case ADD_USER:
        return Object.assign({},state,
        {list: [...state.list, action.value]}
        );
    case ALL_USER:
            let array=[''];
            for(let i in action.list){
                array.push(action.list[i].name);
                }
        return  Object.assign({},state,  {list: array}   );  
    case GET_USER:
        return Object.assign({}, state,  action.value);
        // return Object.assign({}, state, {newUser: action.newUser}); 
    default:
        return state;
    }
    }
    ```

##  4. 服务端
1. 渲染模板   
touch server/templates/index.ejs
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>React App</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    </head>
    <body>
    <div id="app"><%- html %></div>
        <script type="text/javascript" charset="utf-8">
        //window.__REDUX_STATE__ = <%- JSON.stringify(reduxState) %>;
        window.__REDUX_STATE__ = JSON.parse('<%- JSON.stringify(reduxState)%>');
        </script>
    <script src="/bundle.js"></script>
    </body>
    </html>
    ```
2. 服务器端路由
 *路由：api/XXX  获取数据（koa-router处理）,render/XXX 渲染模板（react-router处理）*
touch src/server/controllers/router.js
    ```js
    import render from './render'
    function router(options) {
        return async (ctx, next) => {
    if (ctx.path.match(/^\/api/)) {
        return await require('./routeUtil.js').routes()(ctx, next)
    }
        // await require('./render.js')(ctx, next)  
        await render(ctx, next) 
        }
    }
    module.exports = router;
    ```
修改 app.js
    ```js
    const router = require('./controllers/router.js');
    app.use(router());
    ```
touch src/server/controllers/render.js
    ```js
    import {renderToString } from 'react-dom/server'
    import configureStore from '../../common/store/configureStore'
    import React from 'react';
    import {config,App,Routes } from '../../common/router.js'
    const matchPath = require('react-router-dom').matchPath;
    export default async (ctx, next, renderProps) => {
        // 简单解决node-fetch host问题
        // app.locals.host = req.headers.host;
        // store必须是fresh的，以避免前后请求间的干扰
        const store = configureStore();
        const context = {};
        // 包含一个请求
        const promises = []
        //some() 方法用于检测数组中的元素是否满足指定条件
        //为`<Switch>`选择第一个匹配行为
        config.some(route => {       
            const match = matchPath(ctx.request.url, route);
            // console.log('match', match);
            if (match) {
                // 初始化数据，改变路由
                promises.push(route.component.getInitData(store.dispatch, match.params)());
            }
            return match;
        });
        await  Promise.all(promises).then(data => {
            const html = renderToString(React.createElement(Routes, {
                store:store,
                location:ctx.request.url,
                context:context,
            }));
            return html;        
        }).then(html => {
            //console.log(html);
            const reduxState = store.getState();
            return  ctx.render('index', { html: html, reduxState: JSON.stringify(reduxState) });
        });  
    }
    ```
5. 服务端wepback打包：
touch src/server/webpack.config.js
    ```js
    const webpack = require("webpack");
    const webpackBase = require('../common/webpack.base');
    const rootDir = process.cwd();
    const plugins =webpackBase.plugins;
    plugins.push(new webpack.HotModuleReplacementPlugin());
    const serverConfig={
    entry: {
    app:["webpack-hot-middleware/client?noInfo=true&reload=true",rootDir + '/src/browser/app.js']
    },
    plugins:plugins
    }
    module.exports =Object.assign({}, webpackBase,serverConfig)
    ```
mkdir src/server/middleware  
`npm install --save-dev webpack-dev-middleware webpack-hot-middleware`
touch src/server/middleware/devMiddleware.js
    ```js
    // npm install --save-dev webpack-dev-middleware webpack-hot-middleware
    const webpackDev  = require('webpack-dev-middleware')
    const devMiddleware = (compiler, opts) => {
        const middleware = webpackDev(compiler, opts)
        return async (ctx, next) => {
            await middleware(ctx.req, {
                end: (content) => {
                    ctx.body = content
                },
                setHeader: (name, value) => {
                    ctx.set(name, value)
                }
            }, next)
        }
    }
    module.exports=devMiddleware;
    ```
touch src/server/middleware/hotMiddleware.js    
    ```js
    const webpackHot = require('webpack-hot-middleware')
    const PassThrough = require('stream').PassThrough;
    const hotMiddleware = (compiler, opts) => {
        const middleware = webpackHot(compiler, opts);
        return async (ctx, next) => {
            let stream = new PassThrough()
            ctx.body = stream
            await middleware(ctx.req, {
                write: stream.write.bind(stream),
                writeHead: (status, headers) => {
                    ctx.status = status
                    ctx.set(headers)
                }
            }, next)
        }    
    }
    module.exports = hotMiddleware;
    ```
touch src/server/app.js
    ```js
    const webpack = require("webpack");
    const webpackConfig = require("./webpack.config");
    const devMiddleware = require("./middleware/devMiddleware");
    const hotMiddleware = require('./middleware/hotMiddleware');
    const compiler = webpack(webpackConfig);
    ```
6. 服务器端支持fetch
npm i --save node-fetch
app.js
    ```js
    global.fetch = require('node-fetch');
    ```
7. 忽略组件中的CSS和图片等非JS资源
npm i --save ignore-styles
    ```js
    require('ignore-styles');
    ```
浏览器： http://172.168.1.70:5555
