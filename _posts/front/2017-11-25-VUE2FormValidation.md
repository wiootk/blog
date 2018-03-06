---
layout: post
title:  "VUE2表单验证"
date:   2017-11-25
desc: "VUE2表单验证"
keywords: "前端,VUE2,FormValidation,表单验证"
categories: [Front]
tags: [前端,VUE2,FormValidation,表单验证]
icon: icon-vue
---
# 目标
  封装基于vue2的表单验证  
  1. 指定的输入框验证并提示信息
  2. 当表单（所有输入）验证通过后可提交表单
  
# 编写指令
1. 验证指令的正则表达式库：patterns.js
   ```js
    const patterns = {
        'abc': {
            'reg': '^\\d{2}$',//正则表达式
            'msg': '请输入两个数字'//验证失败的提示文字
        },
    }
    export { patterns as default };
   ```
2. 封装指令：directive.js
   ```js
    import $ from 'jquery'
    import Vue from 'vue'
    import patterns from './patterns.js'
    
    Vue.directive('valid', function(el, binding) {
            // 获取指令库中指定的key
        let key = Object.keys(binding.modifiers).sort((a, b) => a - b)[0],
            //输入值（自定义验证函数）
            custom = binding.value,
            patt = patterns[key];
        if (patt) {
            // 为元素添加 pattern 属性
            $(el).attr('pattern', patt.reg);
        }
        // 监听事件
        el.addEventListener('blur', function(e) {
            //移除信息提示
            var alerts = $(el).parent()[0].childNodes;
            if (alerts) {
                for (let i = 0; i < alerts.length; i++) {
                    if ($(alerts[i]).attr('class') == 'am-alert am-alert-danger') {
                        $(alerts[i]).remove();
                    }
                };
            }
            var msg = "",
                // input 验证结果
                valid = $(el)[0].validity;
            if (custom && custom.fun) {
                //自定义验证函数
                if (custom.fun()) {
                    msg = custom.msg;
                }
            } else if ($(el).attr('pattern') && valid.patternMismatch) {
                // 正则验证
                msg = patt.msg;
            } else if ($(el).attr('required') && valid.valueMissing) {
                // 必填验证
                msg += '请输入内容 ';
            } else if ($(el).attr('max') && (parseInt($(el).val()) > parseInt($(el).attr('max')))) {
                // 最大值验证
                let maxMsg = `输入最大值为：${$(el).attr('max')} `;
                msg += maxMsg;
            } else if ($(el).attr('min') && (parseInt($(el).val()) < parseInt($(el).attr('min')))) {
                //最小值验证
                let maxMsg = `输入最小值为：${$(el).attr('min')} `;
                msg += maxMsg;
            };
            if (msg) {
                // 验证不通过的提示信息
                $(el)[0].setCustomValidity(msg);
                $(el).after(`<div class="am-alert am-alert-danger">${msg}</div>`);
            } else {
                 // 验证通过清空提示信息
                $(el)[0].setCustomValidity("");
            }
            // console.log($(el)[0].validationMessage); 
            var form = $(el).closest("form")[0];
            // 根据表单验证结果是否可提交
            for (var ii = 0; ii < form.length; ii++) {
                if (typeof($(form[ii]).attr("sublimt")) !== "undefined") {
                    $(form[ii]).attr('disabled', !$(el).closest("form")[0].checkValidity());
                }
            }
        }, false);
        // $(el).trigger("input");
        // el.dispatchEvent(new Event('change', { target: el.target })) ;
        // el.dispatchEvent(new Event('input', { target: el.target }));
    })

   ```
在main.js引入 directive.js

#  使用 
   ```html
   <template>
    <form >
        <div class="am-form-group">
            <label>data1：</label>
            <input type="text" v-valid.abc required v-model='data1' />
            <!-- v-valid.abc required  max="6" min="4" -->
        </div>                                
        <div class="am-form-group">
            <label>data2：</label>
            <input type="text" v-valid="{fun:test,msg:'test信息'}" required v-model='data2' />
        </div>
        <div class="am-form-group">
            <div class="am-u-sm-9 am-u-sm-push-3">
                <button sublimt type="button" class="am-btn am-btn-primary tpl-btn-bg-color-success am-btn-secondary" @click='save()'>
                <span class="am-icon-save"></span>&#12288;提交
                </button>
            </div>
        </div>
    </form>
    </template>
    <script>
        import $ from 'jquery';
        export default {
            name: 'validForm',
            data() {
                return {
                    'data1': 0,
                    'data2': 1
                       }
            },
            methods: {
                save: function() {       },
                test: function() {
                    return this.data1 > this.data2;
                }
            },
            mounted: function() {    },
            watch: {
                '$route' (to, from) {        }
            }
        }
    </script>
   ```
