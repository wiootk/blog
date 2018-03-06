---
layout: post
title:  "AngularJs指令封装"
date:   2018-01-24
desc: "AngularJs指令封装"
keywords: "前端,AngularJs,指令封装"
categories: [Front]
tags: [前端,AngularJs,指令封装]
icon: icon-html
---

# 表格内动态插入tr

1. 指令封装
```js
app.directive('photoRecordsTr', ['concrete', '$rootScope', '$timeout', 'showEloamGpy', '$compile', function(concrete, root, $timeout, showEloamGpy, compile) {
        return {
            restrict: 'AE',
            scope: {
                objid: '=',
                bizid: '='
            },
            tranclude: true,
            template: '<span style="cursor:pointer" ng-bind="{true:\'隐藏\',false:\'显示\'}[showStatus]"></span>',
            link: function(scope, element, attr, ctrl) {
                var first = false;
                scope.showStatus = false;
                // dom元素绑定click 事件
                element.bind('click', function(event) {
                    scope.showStatus = !scope.showStatus;
                    if (!first) {
                        var tr = $(element).parent('td').parent('tr');
                        // 获取td个数
                        var tdSize = tr.find("td").length;
                        // var newTr = tb.insertRow(trIndex);
                        //添加新行，trIndex就是要添加的位置 
                        tr.after('<tr ng-show="showStatus&&photoRecords[0]"><td colspan="' + tdSize + '"><div  photos="photoRecords"></div></td></tr>');
                        // 编译html进入angular管理
                        compile(element.parent('td').parent('tr').next())(scope);                        
                    }
                    first = true;
                     // 每次进入指令，触发脏检查，更新model
                    scope.$apply();                   
                    if (!scope.photoRecords) {
                        var url = 'Photos.get';
                        if (scope.bizid) {
                            url = 'Photos.getBizRecord';
                        }
                        concrete(url, function(PhotoInfos) {
                            scope.photoRecords = PhotoInfos;
                        }, { 'objectId': scope.objid, 'bizId': scope.bizid, 'type': scope.type });
                    }
                });
            }
        }
    }]);
```

2. 使用
   ```html
   <td><span photo-records-tr objid='item.objId' bizid='item.bizId'><span></td>
   ```

