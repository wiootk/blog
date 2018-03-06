---
layout: post
title:  "AngularJs文件上传指令封装"
date:   2018-01-24
desc: "AngularJs文件上传指令封装"
keywords: "前端,AngularJs,文件上传"
categories: [Front]
tags: [前端,AngularJs,文件上传]
icon: icon-html
---
# js封装指令
```js
// 上传
 app.directive('uploadFile', ['$timeout', function($timeout) {
        return {
            restrict: 'A',
            scope: {
                lable: '@',
                uploadFile: '='
            },
            tranclude: true,
            template: '<span><span class="btn btn-success" style="position: relative;display: inline-block;overflow: hidden;"><span ng-bind="lable"></span><input type="file" bind-file ng-model="uploadFile" style="width:100%;position:absolute;right: 0px;top: 0px;opacity: 0; -ms-filter: \'alpha(opacity=0)\';font-size: 200px;"></span>&nbsp;&nbsp;<a  href="javascript:void(0)"  show-file="uploadFile"><span ng-bind="fileName"></span></a></span>',
            link: function(scope, element, attr, ctrl) {
                scope.$watch('uploadFile', function(newValue, oldValue) {
                    if (newValue && newValue.name) {
                        var name = newValue.name
                        var ext = name.substring(name.lastIndexOf('_') + 1);
                        scope.fileName = name.substring(0, name.lastIndexOf('_')) + '.' + ext;
                    }
                });
            }
        }
    }])
    // 绑定 input[type=file] 文件变化时，进行上传
    app.directive('bindFile', ['concrete', '$rootScope', function(concrete, root) {
        return {
            require: "ngModel",
            restrict: 'A',
            link: function($scope, el, attrs, ngModel) {
                var url = root.uploaderInfo.fileServerLocation + "?a=" + 
                   root.uploaderInfo.appId + "&s=" + root.uploaderInfo.tokenId;
                var upload = function(_file) {
                    var formData = new FormData();
                    if (_file[0]) {
                        console.log(_file[0]);
                        formData.append(_file[0].name || "file", _file[0]);
                        $.ajax({
                            url: url,
                            type: 'post',
                            data: formData,
                            processData: false,
                            contentType: false,
                            enctype: 'multipart/form-data',
                            cache: false,
                            beforeSend: function() {
                                console.log("正在进行，请稍候");
                            },
                            success: function(data) {
                                ngModel.$setViewValue({
                                    // 'name': data.files[0].name,
                                    'name': _file[0].name,
                                    'resourceId': data.files[0].resourceId
                                })
                                $scope.$apply();
                            },
                            error: function(data) {
                                console.log("error");
                            }
                        });
                    }
                }
                el.bind('change', function(event) {
                    upload(event.target.files);
                });

                $scope.$watch(function() {
                    return ngModel.$viewValue;
                }, function(value) {
                    if (!value) {
                        el.val("");
                    }
                });
            }
        };
    }]);
// 下载
    app.directive('showFile', ['concrete', '$rootScope', function(concrete, root) {
        return {
            restrict: 'A',
            scope: {
                'showFile': '='
            },
            link: function(scope, el, attrs, ctrl) {
                var getUrl = function() {                    
                        return root.uploaderInfo.fileServerLocation + "/" +
                         root.uploaderInfo.appId + "/" + 
                         scope.showFile.resourceId + "?s=" + 
                         root.uploaderInfo.tokenId;
                }
                el.bind('click', function(event) {
                    concrete('charteredVehCert.initLoad', function(data) {
                        var name = scope.showFile.name
                        var ext = name.substring(name.lastIndexOf('_') + 1);
                        var fileName = name.substring(0, name.lastIndexOf('_'));
                        var aLink = document.createElement('a');
                        var evt = document.createEvent("HTMLEvents");
                        evt.initEvent("click", false, false);
                        // aLink.download = fileName;
                        aLink.style.display = 'none';
                        aLink.target = '_blank';
                        aLink.href = getUrl();
                        document.body.appendChild(aLink);
                        aLink.click();
                        document.body.removeChild(aLink);
                        // if (['BMP', 'GIF', 'JPEG', 'PNG', 'JPG'].indexOf(ext.toUpperCase())) {
                        //     window.open().document.write("<img style='width:100%' src=" + getUrl() + " />");
                        // } else {

                        //     window.open(getUrl());
                        // }
                    }, scope.showFile.resourceId);
                });
            }
        };
    }]);
```

# 使用
```html
<!-- 上传 -->
<span upload-file="Contract" lable="合同"></span>
<!-- 下载 -->
<span show-file='fileInfo'><a bo-text="fileInfo.name"></a></span>
```
