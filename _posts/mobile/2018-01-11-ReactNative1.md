---
layout: post
title:  "ReactNative搭建开发环境"
date:   2018-01-11
desc: "ReactNative搭建开发环境"
keywords: "Mobile,ReactNative"
categories: [Mobile]
tags: [Mobile,ReactNative]
icon: icon-html
---

# Sublime text 插件
1. React ES6 Snippets
2. jsx语法代码格式化 sublime-jsfmt
    修改设置`Preferences -> Package Settings -> Sublime JSFMT->default setting`
3. 设置代码快捷键：
`Preferences -> Key Bindings ->User->{"keys":["ctrl+q"],"command":"format_javascript"}`

# 必需的软件

**主要安装：`Python、Node、react-native-cli、ANDROID_HOME环境变量、git、安卓模拟器、Android Studio`**

1. Chocolatey(Windows的包管理器)(未使用)
```shell
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
```

2. Python 2  
`choco install python2`  

3. Node  
`choco install nodejs.install`  

4. 设置npm镜像  
`npm config set registry https://registry.npm.taobao.org --global`  
`npm config set disturl https://npm.taobao.org/dist --global`  

5. 命令行工具（react-native-cli）  
`npm install -g yarn react-native-cli`  

6. 设置镜像源(未使用)：  
`yarn config set registry https://registry.npm.taobao.org --global`  
`yarn config set disturl https://npm.taobao.org/dist --global`  
*用`yarn add 某第三方库名`代替`npm install --save 某第三方库名`*  

7. Android Studio  
安装完成后，在Android Studio的欢迎界面中选择`Configure | SDK Manager`  
在`SDK Platforms->Show Package Details->Android 6.0 (Marshmallow)`:勾选  
```
Google APIs、Android SDK Platform 23（必须）、Intel x86 Atom System Image、Intel x86 Atom_64 System Image以及Google APIs Intel x86 Atom_64 System Image
```
`SDK Tools->Show Package Details->Android SDK Build Tools`:勾选  
`Android SDK Build-Tools 23.0.1,Android Support Repository`

8. ANDROID_HOME环境变量  
新建 `ANDROID_HOME=d：\soft\android\sdk`  
把`Android SDK的tools和platform-tools`目录添加到`PATH变量`  

9. 推荐  
**Gradle Daemon提升java代码的增量编译速度**  
```cmd
(if not exist "%USERPROFILE%/.gradle" mkdir "%USERPROFILE%/.gradle") && (echo org.gradle.daemon=true >> "%USERPROFILE%/.gradle/gradle.properties")
```

10. Git  
`choco install git`  

11. Genymotion模拟器  
        1. 下载和安装Genymotion（genymotion需要依赖VirtualBox虚拟机，下载选项中提供了包含VirtualBox和不包含的选项，请按需选择）  
        2. 打开Genymotion。如果你还没有安装VirtualBox，则此时会提示你安装  
        3. 创建一个新模拟器并启动  
        4. 启动React Native应用后，可以按下F1来打开开发者菜单          

12. 个人使用的是夜神模拟器  

# 测试安装
## 初始化 

1. 初始化项目  
    `react-native init reactNativeDemo && cd reactNativeDemo` 
2. 打开 安卓模拟器
3. 命令行(在模拟器的bin目录新建nox_connect.bat并快捷方式到桌面)：
```shell
# 模拟器的bin目录
nox_adb.exe connect 127.0.0.1:62001
adb connect 127.0.0.1:62001
```

4. 问题：gradle 下载不下来
    1. 下载 gradle-2.14.1-all.zip 放到：`android/gradle/wrapper/`下
    2. 修改：`gradle-wrapper.properties`： `distributionUrl=gradle-2.14.1-all.zip`

5. 启动项目(创建启动文件start.bat)
```shell
# 项目目录
react-native run-android
```

6. 处理红屏  
`红屏->摇一摇->Dev Settings->debug server host&port for device:ipconfig中的ip:8081->重启项目`

# 修改项目

1. 编辑`App.js`~~(`index.android.js`)~~->`按两下R键`，或`Menu键`（通常是F2，在Genymotion模拟器中是⌘+M）打开`开发者菜单`->选择` Reload JS`

2. 查看日志：（终端或命令行）运行`adb logcat *:S ReactNative:V ReactNativeJS:V`

# 真机调试
## USB调试
1. 开启USB调试
    1. 设置->...->开发者模式->usb 调试  
    *小米6:`设置->我的设备->全部参数->连续点击MIUI版本->返回上一级->更多设置`*
2. 查看连接的设备：`adb devices`  
    *（关闭模拟器，保持只有一台设备连接）*
3. 启动程序
    1. 用IDE启用（保持ide 服务开启）:`react-native start --port 9999`
    2. `react-native run-android`
    3. `react-native run-android --variant=release`来安装release版的应用  
*注：白屏情况：开启悬浮窗权限（应用软件管理-软件-权限-浮窗权限）*

4. 卸载原App: `adb uninstall packageName`
5. 重新编译：`cd android && gradlew clean`  
删掉`\android\app\build\`下的所有文件夹，重新`React-native run-android`
6. 常见问题
    1. 主机中的软件终止了一个已经建立的连接：
    ```shell
    adb kill-server&&adb start-server
    DDMS - Devices - Reset adb
    ```
    2. 开着两个IDE导致端口占用
    ```shell
    #查看adb server的端口
    adb nodaemon server
    #占用端口5037的PID值
    netstat -a -n -o |findstr "5037"
    DDMS - Devices - Reset adb
    #查看进程名
    tasklist /v | findstr 5096
    #杀死占用5037端口
    taskkill /f -pid 5096   taskkill /im tadb.exe
    ```

## wifi 调试
1. 保持`adb devices`有一台设备连接着
2. 确保电脑和手机设备在同一个Wi-Fi环境下
3. 在设备上运行你的React Native应用
4. 摇晃设备，或者运行`adb shell input keyevent 82`-->开发者菜单：`Dev Settings->Debug server host for device`->电脑的(ipconfig)IP地址和端口号->开发者菜单->`Reload JS`

## 开启debug
修改(因为要导包建议使用IDE工具修改)  `src/main/Java/MainApplication`的 onCreate方法：
```java
@Override
public void onCreate() {
  super.onCreate();
  //SoLoader.init(this, /* native exopackage */ false);
  SharedPreferences mPreferences =    PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
  mPreferences.edit().putString("debug_http_host","localhost:8099").commit();
}
```