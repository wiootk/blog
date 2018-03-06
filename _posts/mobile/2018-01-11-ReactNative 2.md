---
layout: post
title:  "ReactNative脚手架搭建"
date:   2018-01-22
desc: "ReactNative脚手架搭建"
keywords: "Mobile,ReactNative"
categories: [Mobile]
tags: [Mobile,ReactNative]
icon: icon-html
---

#  开发环境搭建[参见前文](/blog/mobile/2018/01/11/ReactNative1.html){:target="_blank"} 

# 脚手架搭建

## 页面导航
文件结构
```
src/
    |- app.js
    |- components/
    |- pages/
    |- images/
    |- config/
    |- utils/
```

创建目录结构： `mkdir src&cd src & mkdir component page images  config  utils & touch app.js`

### react-navigation
安装依赖：  `npm install --save react-navigation`  
创建文件：  `touch page/index.js page/list.js page/detail.js`  

1. page/index.js 
```html
import React, { Component } from 'react';
import { AppRegistry, Text, View, Button } from 'react-native';
class index extends React.Component {
    static navigationOptions = {
        title: 'index页'
    };
    render() {
        const {navigate} = this.props.navigation;
        return (
            <View>
            <Text>欢迎：index 页</Text>
            <Button onPress={() => navigate('index')}   title="主页"  />
            <Button onPress={() => navigate('list')}   title="列表页"  />
            <Button onPress={() => navigate('detail', {
                page: '主页'
            })} title="详情页"  /> 
            </View>
        );
    }
}
export default index;
```

2. page/list.js 
```html
import React, { Component } from 'react';
import { Text, View, Button } from 'react-native';
class list extends React.Component {
    static navigationOptions = {
        title: '列表页'
    };
    render() {
        const {navigate} = this.props.navigation;
        return (
            <View>
                <Text>欢迎：list 页</Text>
                <Button onPress={() => navigate('index')}   title="主页"  />
                <Button onPress={() => navigate('list')}   title="列表页"  />
                <Button onPress={() => navigate('detail', {
                page: '列表页'
            })} title="详情页"  />             
            </View>
        );
    }
}
export default list;
```

3. page/detail.js
```html
import React, { Component } from 'react';
import { Text, View, Button } from 'react-native';
class detail extends React.Component {
    static navigationOptions = ({navigation}) => ({
        title: `详情页__来自 ${navigation.state.params.page}`,
    });
    render() {
        // const { params } = this.props.navigation.state;
        const {navigate, state, goBack} = this.props.navigation;
        return (
            <View>
        <Text>欢迎：detail 页   来自 {state.params.page}</Text>
        <Button onPress={() => navigate('index')}   title="主页"  />
        <Button  title="Go back"  onPress={() => goBack()}    />
      </View>
        );
    }
}
export default detail;
```

4. app.js
```js
import index from './page/index';
import list from './page/list';
import detail from './page/detail';
//StackNavigator顶部导航，跳转页面和传递参数。
//TabNavigator底部标签栏，区分模块。
//DrawerNavigator左侧滑出页面
import { StackNavigator } from 'react-navigation';
const app = StackNavigator({
    index: {
        screen: index
    },
    list: {
        screen: list,
         navigationOptions:{
            // header：null//隐藏顶部导航条
            headerBackTitle:'返回' , //返回箭头后面的文字
            // headerTruncatedBackTitle：上个页面 //返回箭头后的文字不符合，默认改成"返回"
            // headerRight：设置导航条右侧
            // headerLeft：设置导航条左侧。按钮或者其他
            // headerStyle：导航条的样式。去掉安卓导航条底部阴影elevation: 0,iOS用shadowOpacity: 0
            // headerTitleStyle：导航条文字样式。文字居中alignSelf:'center'
            // mode：card|modal|headerMode 定义跳转风格
            // headerTintColor：设置导航栏文字颜色
            // headerBackTitleStyle：设置导航条返回文字样式
            // onTransitionStart：当转换动画即将开始时被调用的功能。
            // onTransitionEnd：当转换动画完成，将被调用的功能。
            headerTitle:'详情',
            headerBackTitle:null,
        }
    },
    detail: {
        screen: detail
    }
});
export default app;
```

5. App.js~~(index.android.js)~~
```js
import React from 'react';
import { AppRegistry, Text, View, Button } from 'react-native';
import Main from './src/app';
export default Main;//重要
AppRegistry.registerComponent('reactNativeDemo', () => Main);
```

### 导航嵌套
在images文件夹下添加photo.jpg

1. touch src/router.js 路由页面作为入口（包含两个主页面）
```js
import {StackNavigator} from "react-navigation";
import MainPage from './page/mainPage';
import detail from './page/detail';
import MyDraw from './page/DrawPage';
const routers = StackNavigator({
    Main: {     screen: MainPage   },
    detail: {     screen: detail },
    MyDraw: {     screen: MyDraw },
});
module.exports = routers;
```

2. touch src/page/mainPage.js 主页页面（包含两个分页面）
```js
import React, {Component} from 'react';
import {    StyleSheet,    Image,    Style} from 'react-native';
import {TabNavigator} from "react-navigation";
import index from './index';
import list from './list';
const mainPage = TabNavigator({
    index: {
        screen: index,
        navigationOptions: {   }
    },
    list: {
        screen: list,
        //以下参数也可放置在list.js页面
        navigationOptions: {
            title: '列表',
            tabBarLabel: '列表',
            tabBarIcon: ({ tintColor }) => (
                <Image   source={  require('../images/photo.jpg')   }
                    style={[styles.icon,{tintColor: tintColor}]}// {tintColor: tintColor} 选中的图片和文字颜色
                />
            ),
            headerTitleStyle: {
                alignSelf:'center'
            }
        }
    }   
}, {
    animationEnabled: true, // 切换页面时不显示动画
    tabBarPosition: 'bottom', // 显示在底端，android 默认是显示在页面顶端的
    swipeEnabled: false, // 是否左右滑动,如果有DrawerNavigator,最好设置为false避免手势冲突
    backBehavior: 'none', // 按 back 键是否跳转到第一个 Tab， none 为不跳转
    tabBarOptions: {
        activeTintColor: '#0F9C00', // 文字和图片选中颜色
        inactiveTintColor: '#999', // 文字和图片默认颜色
        showIcon: true, // android 默认不显示 icon, 需要设置为 true 才会显示
        indicatorStyle: {height: 0}, // android 中TabBar下面会显示一条线，高度设为 0         style: {
            backgroundColor: '#444', // TabBar 背景色
            height:50
        },
        labelStyle: {
            fontSize: 12, // 文字大小,
            marginTop: 0,
        },
    },
});
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    icon:{
        width:20,
        height:20
    }
});
module.exports = mainPage;
```

3. src/page/index.js 分页面1
```html
import React, {Component} from 'react';
import {AppRegistry,StyleSheet,Text,View,Image,Button,TouchableOpacity} from 'react-native';
import DrawPage from './DrawPage'
export default class index extends Component {
    static navigationOptions = {
        title: 'index页',
        tabBarLabel: '首页',
        tabBarIcon: ({ tintColor }) => (
            <Image   source={require('../images/photo.jpg')}
                style={[styles.icon,{tintColor: tintColor}]}// {tintColor: tintColor} 选中的图片和文字颜色
            />
        ),
        headerTitleStyle: {
         alignSelf:'center'
        },
    };
    render() {
        const {navigate} = this.props.navigation;
        return (
         <View>
         <DrawPage/>
         <Text>欢迎：index 页</Text>
         <Button onPress={() => navigate('index')}   title="主页"  />
         <Button onPress={() => navigate('list')}   title="列表页"  />
         <Button onPress={() => navigate('detail', {
                page: '主页'
            })} title="详情页"  /> 
        <Button onPress={() => navigate('MyDraw')}   title="MyDraw"  /> 
         </View>
        )
    }
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    icon:{
        width:20,
        height:20
    }
});
```

4. src/page/list.js 分页面2
```html
import React, {Component} from 'react';
import {AppRegistry,StyleSheet,Text,View,Image,Button} from 'react-native';
import { NavigationActions } from 'react-navigation'
export default class list extends Component {
    static navigationOptions = {
        title: 'list页',
        tabBarLabel: '列表页',
        tabBarIcon: ({ tintColor }) => (
            <Image source={require('../images/photo.jpg')}
                style={[styles.icon,{tintColor: tintColor} ]}/>
        ),
    };
    goToDetail() {
        const {dispatch} = this.props.navigation;
        const resetAction = NavigationActions.reset({
            index: 0,//指定显示数组内的路由
            actions: [
                NavigationActions.navigate({ routeName: 'detail',params:{page: '列表页'}}),
            ]
        });
        dispatch(resetAction);
    }
    render() {
         const {navigate} = this.props.navigation;
        return (
            <View style={styles.container}>
            <Text>欢迎：list 页</Text>
             <Button onPress={() => navigate('index')}   title="主页"  />
             <Button onPress={() => navigate('list')}   title="列表页"  />
             <Button onPress={() => navigate('detail', {
                page: '列表页'
            })} title="详情页"  />              
                <Button onPress={() => this.goToDetail()} title="跳转详情页+传参+清空路由" />
            </View>
        );
    }
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    icon:{
        width:20,
        height:20
    }
});
```

5. src/page/detail.js 主页页面
```html
import React, {Component} from 'react';
import {AppRegistry,StyleSheet,Text,View,Image,Button} from 'react-native';
import { StackNavigator} from 'react-navigation';
export default class detail  extends Component {
       static navigationOptions = ({navigation}) => ({
        title: `详情页__来自 ${navigation.state.params.page}`,
    });
    render() {
        // const { params } = this.props.navigation.state;
        const {navigate, state, goBack} = this.props.navigation;
        return (
            <View style={styles.container}>
                <Text>欢迎：detail 页   来自 {state.params.page}</Text>
                <Button onPress={() => navigate('index')}   title="主页"  />
                <Button  title="Go back"  onPress={() => goBack()}    />
            </View>
        );
    }
}
const styles = StyleSheet.create({
    container: {
        flex: 6,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F5FCFF',
    }
});
```

6. touch src/page/DrawPage.js 主页页面（包含两个分页面）
```html
import React, {Component} from 'react';
import {AppRegistry,StyleSheet,Text,View,Image,Button,ScrollView} from 'react-native';
import {DrawerNavigator, DrawerItems} from 'react-navigation';
class MyHomeScreen extends Component {
    render() {
        return (
            <View style={styles.container}>
                <Button onPress={() => this.props.navigation.navigate('Notifications')} title="notifications" />
                <Button onPress={() => this.props.navigation.navigate('DrawerOpen')} title="左侧菜单开" />
                <Button onPress={() => this.props.navigation.navigate('DrawerClose')} title="左侧菜单关" />
            </View>
        );
    }
}
class MyNotificationsScreen extends Component { 
    render() {
        return (
            <View style={styles.container}>
                <Button onPress={() => this.props.navigation.navigate('Home')} title="Go back home" />
            </View>
        );
    }
}
const CustomDrawerContentComponent = (props) => (
    <ScrollView>
        {/*<DrawerItems {...props} />*/}
        <View>
            <Text>左侧菜单</Text>
            <Text>你好美女</Text>
        </View>
    </ScrollView>
);
const MyDraw = DrawerNavigator({
        Home: {  screen: MyHomeScreen },
        Notifications: {  screen: MyNotificationsScreen    },
    }, {
        //drawerWidth: 200, // 抽屉宽
        drawerPosition: 'left', // 抽屉在左边还是右边
        contentComponent: CustomDrawerContentComponent,  // 自定义抽屉组件
        // contentOptions: {
        //     initialRouteName: MyHomeScreen, // 默认页面组件
        //     activeTintColor: 'white',  // 选中文字颜色
        //     activeBackgroundColor: '#ff8500', // 选中背景颜色
        //     inactiveTintColor: '#666',  // 未选中文字颜色
        //     inactiveBackgroundColor: '#fff', // 未选中背景颜色
        //     style: {  // 样式
        //
        //     }
        // }
    });
const styles = StyleSheet.create({
    icon: {
        width: 24,
        height: 24,
    },
    container:{justifyContent: 'center', alignItems: 'center', flex: 1}
});
export default  MyDraw;
```

7. 修改 App.js
```js
// import Main from './src/app';
import Main from './src/router';
```

## 集成redux
1. 安装依赖 : `npm install  redux react-redux redux-thunk react-native-vector-icons  redux-promise redux-actions --save`  
新建文件夹 redux  
拷贝样式表 styles  

2. 集成react-native-vector-icons  
   1. android/app/build.gradle
   ```
   # 添加
   project.ext.vectoricons = [
       iconFontNames: [ 'MaterialIcons.ttf', 'EvilIcons.ttf','FontAwesome.ttf','Ionicons.ttf' ]
   ]
   apply from: "../../node_modules/react-native-vector-icons/fonts.gradle"
   ```
   将Fonts 文件夹拷贝到`android/app/src/main/assets/fonts`
   
   2. android/settings.gradle
   ```
   # 添加
   include ':react-native-vector-icons'
   project(':react-native-vector-icons').projectDir = new File(rootProject.projectDir, '../node_modules/react-native-vector-icons/android')
   ```
   
   3. android/app/build.gradle
   ```
   dependencies {
   //...
      compile project(':react-native-vector-icons')
   }
   ```
   
   4. 未测试： *rm ./node_modules/react-native/local-cli/core/__fixtures__/files/package.json*

2. touch src/redux/actionTypes.js
```js
export const TEST_TYPE = '测试1';
```
3. touch src/redux/actions.js
```js
import {   TEST_TYPE } from './actionTypes';
import { createAction } from 'redux-actions';
const thumbnail = 'https://facebook.github.io/react/img/logo_og.png';
// 获取news 列表数据
export var fetchList = createAction(TEST_TYPE, () => {
    return [1,2,3,4,5].map(item => {
        return {
            id: item,
            title: `[${item}]夏季又要到`,
            thumbnail: thumbnail
        }
    });
});
```

4. touch src/redux/reducer.js
```js
import { combineReducers } from 'redux';
import news from './minePage';
export default function getReducers(navReducer) {
    //一个根reducer,把N个reducer组合起来
    return combineReducers({
        news,
        nav: navReducer
    });
}
```

5. touch src/redux/store.js
```js
import { createStore, applyMiddleware } from 'redux';
import promiseMiddleware from 'redux-promise';
import getReducers from './reducer';
//promiseMiddleware 是异步action的一个中间件
export default function getStore(reducer) {
    return createStore(
        getReducers(reducer),
        undefined,
        applyMiddleware(promiseMiddleware)
    );
}
```

6. touch src/redux/home.js（使用\{\{ 代替双大括号 ）
```html
import React, { Component } from 'react';
import Icon from 'react-native-vector-icons/Ionicons';
import { View,Text,Image,FlatList,StatusBar,TouchableHighlight} from 'react-native';
import { topicCard } from '../styles';
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import * as testActions from './actions';
class Home extends Component {
    //定义底部tabBar的icon和name
    static navigationOptions = {
        tabBarLabel: '首页',
        tabBarIcon: ({ tintColor }) => (
            <Icon name="md-home" size={24} color={tintColor} />
        )
    };
    componentDidMount() {
        this.props.fetchList();
    }
    _onPressItem = (id) => {
        this.props.navigation.navigate('detail', { id: id });
    };
    _keyExtractor = (item, index) => item.id;    
    _renderItem = ({item}) => (
        <View style=\{\{alignItems:'flex-start',flexWrap:'nowrap'\}\}>
            <Image style={topicCard.cover} source=\{\{uri: item.thumbnail, crop: {left: 10, top: 50, width: 20, height: 40}\}\} style=\{\{alignSelf:'center',width: 36, height: 36,flex: 6}}></Image>
            <TouchableHighlight style={topicCard.title} onPress={this._onPressItem.bind(this, item.id)} style=\{\{alignSelf:'center',flex: 6\}\}>
                <Text numberOfLines={1} style={topicCard.titleText}>{item.title}</Text>
            </TouchableHighlight>           
        </View>
    );
    render() {
        return (
            <View >
                <FlatList data={this.props.news.data} refreshing={false}
                    keyExtractor={this._keyExtractor} renderItem={this._renderItem}/>
            </View>
        );
    }
}
//让业务组件和redux建立关联
export default connect(
    state => ({  news: state.news }),
    dispatch => bindActionCreators(testActions, dispatch)
)(Home);
```

7. touch src/redux/detail.js
```js
import React, { Component } from 'react';
import { View, Text} from 'react-native';
export default class NewsDetail extends Component {
    static navigationOptions = {
        title: '详情页',
    }
    render() {
        return (
            <View><Text>小哥，精彩哦。。。</Text></View>
        );
    }
}
```

8. touch src/redux/minePage.js
```js
import { TEST_TYPE} from './actionTypes';
import { handleActions } from 'redux-actions';
export default handleActions({
    [TEST_TYPE]: {
        next(state, action) {
            return { ret: true, data: action.payload };
        },
        throw(state, action) {
            return { ret: false, statusText: action.payload, data: [] };
        }
    }
}, { ret: true, statusText: '', data: [] });
```

9. touch src/reduxIndex.js
```html
import React, { Component } from "react";
import { Provider, connect } from "react-redux";
import { addNavigationHelpers } from "react-navigation";
import getStore from "./redux/store";
import { AppNavigator } from './router';
const navReducer = (state, action) => {
    const newState = AppNavigator.router.getStateForAction(action, state);
    return newState || state;
};
const mapStateToProps = (state) => ({
    nav: state.nav
});
class App extends Component {
    render() {
        return (
            <AppNavigator  navigation={addNavigationHelpers({ dispatch: this.props.dispatch,state: this.props.nav })} />
        );
    }
}
const AppWithNavigationState = connect(mapStateToProps)(App);
const store = getStore(navReducer);
export default function Root() {
    return (
        <Provider store={store}>
            <AppWithNavigationState />
        </Provider>
    );
}
```

10. 编辑 router.js
```js
import {TabNavigator,StackNavigator,addNavigationHelpers}from "react-navigation";
import Home from './redux/home';
import detail from './redux/detail';
//底部的tabBar导航
const TabbarNavigator = TabNavigator({
    Home: { screen: Home }
}, {   initialRouteName: 'Home'});
//整个应用的路由栈
const AppNavigator = StackNavigator({
    TabBar: {
        screen: TabbarNavigator,
        navigationOptions: {      header: null    }
    },
    detail: {
        path: 'news/:id',
        screen: detail
    }
});
export { AppNavigator};
```

11. 编辑 index.Android.js
```js
import React, { Component } from 'react';
import { AppRegistry, Text, View, Button } from 'react-native';
// react-navigation
// import Main from './src/app';
// react-navigation 导航嵌套
//import Main from './src/router';
// react-navigation 与redux 整合
import Main from './src/reduxIndex';
export default Main;
AppRegistry.registerComponent('reactNativeDemo', () => Main);
```

## react-navigation与redux集成示例（未测试）
touch src/page/appNavigation
```js
import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { addNavigationHelpers, StackNavigator } from 'react-navigation';
import LoginScreen from '../components/LoginScreen';
import MainScreen from '../components/MainScreen';
import ProfileScreen from '../components/ProfileScreen';
export const AppNavigator = StackNavigator({
  Login: { screen: LoginScreen },
  Main: { screen: MainScreen },
  Profile: { screen: ProfileScreen },
});
const AppWithNavigationState = ({ dispatch, nav }) => (
  <AppNavigator navigation={addNavigationHelpers({ dispatch, state: nav })} />
);
AppWithNavigationState.propTypes = {
  dispatch: PropTypes.func.isRequired,
  nav: PropTypes.object.isRequired,
};

const mapStateToProps = state => ({
  nav: state.nav,
});

export default connect(mapStateToProps)(AppWithNavigationState);
```

## 数据请求（未测试）
1. touch utils/fetch.js
```js
import React, { Component } from 'react';
import { AppRegistry, StyleSheet, Text, View, ListView, Image, TouchableOpacity, Platform, AsyncStorage } from 'react-native';
class fetchUtil extends React.Component {
    static get(url, params, callback) {
        if (params) {
            let paramsArray = [];
            //拼接参数
            Object.keys(params).forEach(key => paramsArray.push(key + '=' + params[key]))
            if (url.search(/\?/) === -1) {
                url += '?' + paramsArray.join('&')
            } else {
                url += '&' + paramsArray.join('&')
            }
        }
        //fetch请求
        fetch(url, {
            method: 'GET',
        }).then((response) => {
            callback(response)
        }).done();
    }
    static post(url, params, token, callback) {
        //fetch请求
        fetch(url, {
                method: 'POST',
                headers: {
                    'token': token
                },
                body: JSON.stringify(params)
            }).then((response) => response.json())
            .then((responseJSON) => {
                callback(responseJSON)
            }).done();
    }
}
module.exports = fetchUtil;
```

2. 使用
```js
    let params = {'start':'0',limit:'20'};
    fetchUtil.post('http://www.pintasty.cn/',params,'tokenId',function (set) {
      console.log(set)
    })
    fetchUtil.get('https://www.baidu.com/','',function (set) {
        console.log(set)
    })
```

## 集成ui框架
参考:   
`https://github.com/react-native-training/react-native-elements`  
