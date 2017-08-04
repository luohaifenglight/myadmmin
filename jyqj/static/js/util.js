/**
 * Created by ducs on 17/1/20.
 */


//覆盖验证框架
$(function () {　　//保存原始的bootstrapValidator
    var overwrite = $.fn.bootstrapValidator; 　　//重载bootstrapValidator
    $.fn.bootstrapValidator = function (options) {
        //恢复原来的bootstrapValidator，因为其加了很多数据是不能丢失的
        $.fn.bootstrapValidator = overwrite;
        var validtor = overwrite.apply(this, arguments);
        if ($.type(arguments[0]) == "object") {
            var vtor = this.data("bootstrapValidator"),　　　　　　//过滤出输入框表单项　　
                fileds = this.find("input[name][type='hidden'],input[name][type='password'],input[name][type=''],input[name][type='text'],textarea[name]").not(":disabled,[type='hidden']");
            fileds.each(function () {
                //本身没有正则验证才添加不能输入&的验证
                if (!vtor.getOptions($(this).attr('name'), 'regexp', 'regexp')) {
                    vtor.addField($(this).attr('name'),
                        {
                            validators: {
                                notEmpty: {
                                    message: '不能为空'
                                },
                                regexp: {
                                    regexp: /^[^&]*$/,
                                    message: "不能包含&字符"
                                }
                            }
                        })
                }
            })
        }
        console.log('done');
        return validtor;
    }
});

//获取指定form中的所有的<input>对象
function getElements(formId) {
    var form = document.getElementById(formId);
    var elements = new Array();
    var tagElements = form.getElementsByTagName('input');
    for (var j = 0; j < tagElements.length; j++) {
        elements.push(tagElements[j]);
    }
    return elements;
}

//获取单个input中的【name,value】数组
function inputSelector(element) {
    if (element.checked)
        return [element.name, element.value];
}

function input(element) {
    switch (element.type.toLowerCase()) {
        case 'submit':
        case 'hidden':
        case 'password':
        case 'text':
            return [element.name, element.value];
        case 'checkbox':
        case 'radio':
            return inputSelector(element);
    }
    return false;
}

//组合URL
function serializeElement(element) {
    var method = element.tagName.toLowerCase();
    var parameter = input(element);

    if (parameter) {
        var key = encodeURIComponent(parameter[0]);
        if (key.length == 0) return;

        if (parameter[1].constructor != Array)
            parameter[1] = [parameter[1]];

        var values = parameter[1];
        var results = [];
        for (var i = 0; i < values.length; i++) {
            results.push(key + '=' + encodeURIComponent(values[i]));
        }
        return results.join('&');
    }
}

//调用方法
function serializeForm(formId) {
    var elements = getElements(formId);
    var queryComponents = new Array();

    for (var i = 0; i < elements.length; i++) {
        var queryComponent = serializeElement(elements[i]);
        if (queryComponent)
            queryComponents.push(queryComponent);
    }
    return queryComponents.join('&');
}


//初始化fileinput控件（第一次初始化） 上传文件并填充名称到input中
function initFileInputFullfill(ctrlName, uploadUrl, fullfill_id) {
    console.log('initfileinput');
    var control = $('#' + ctrlName);
    control.fileinput({
        autoUpload: true,
        language: 'zh', //设置语言
        uploadUrl: '/upload/upload_file_ajax/', //上传的地址
        allowedFileExtensions: ['jpg', 'png', 'gif', 'mp3', 'midi'],//接收的文件后缀
        showCaption: false,//是否显示标题
        browseClass: "btn btn-primary", //按钮样式
        uploadAsync: true, //默认异步上传
        showUpload: false, //是否显示上传按钮
        showRemove: false, //显示移除按钮
        showPreview: true, //是否显示预览
        dropZoneEnabled: true,//是否显示拖拽区域
        previewFileIcon: "<i class='glyphicon glyphicon-king' style='width:50px;height: 50px;'></i>",


    }).on('fileselect', function (event, numFiles, label) {
        var target_id = $("#" + fullfill_id);
        target_id.val(label);
        console.log(label);
        console.log(event);
        console.log(numFiles);
    });
}

//初始化fileinput控件（第一次初始化）
function initFileInput(ctrlName, uploadUrl) {
    console.log('initfileinput');
    var control = $('#' + ctrlName);
    control.fileinput({
        autoUpload: true,
        language: 'zh', //设置语言
        uploadUrl: '/upload/upload_file_ajax/', //上传的地址
        allowedFileExtensions: ['jpg', 'png', 'gif', 'mp3', 'midi'],//接收的文件后缀
        showCaption: false,//是否显示标题
        browseClass: "btn btn-primary", //按钮样式
        uploadAsync: true, //默认异步上传
        showUpload: false, //是否显示上传按钮
        showRemove: false, //显示移除按钮
        showPreview: true, //是否显示预览
        dropZoneEnabled: true,//是否显示拖拽区域
        previewFileIcon: "<i class='glyphicon glyphicon-king' style='width:50px;height: 50px;'></i>",
    });
}

function trans_input(name, value) {
    var str = '';
    str += '<input class="form-control" type="text" name=' + name + '  value=' + value + '  placeholder=' + value + '>';
    return str;

}

//自动填充table 第一个单元格序号
function auto_add_table_id(name) {
    //$('table tr:not(:first)').remove();
    var len = $('table tr').length;
    for (var i = 1; i < len; i++) {
        if (name != '') {
            $('table tr:eq(' + i + ') td:first').text(i);
            // $('table tr:eq(' + i + ') td:first').innerText(trans_input(name, i));
        }
        else {
            $('table tr:eq(' + i + ') td:first').text(i);
        }
    }
}


$(function () {　　//保存原始的bootstrapValidator
    var overwrite = $.fn.bootstrapValidator; 　　//重载bootstrapValidator
    $.fn.bootstrapValidator = function (options) {
        //恢复原来的bootstrapValidator，因为其加了很多数据是不能丢失的
        $.fn.bootstrapValidator = overwrite;
        var validtor = overwrite.apply(this, arguments);
        if ($.type(arguments[0]) == "object") {
            var vtor = this.data("bootstrapValidator"),　　　　　　//过滤出输入框表单项　　
                fileds = this.find("input[name][type='hidden'],input[name][type='password'],input[name][type=''],input[name][type='text'],textarea[name]").not(":disabled,[type='hidden']");
            fileds.each(function () {
                //本身没有正则验证才添加不能输入&的验证
                if (!vtor.getOptions($(this).attr('name'), 'regexp', 'regexp')) {
                    vtor.addField($(this).attr('name'),
                        {
                            validators: {
                                notEmpty: {
                                    message: '不能为空'
                                },
                                regexp: {
                                    regexp: /^[^&]*$/,
                                    message: "不能包含&字符"
                                }
                            }
                        })
                }
            })
        }
        return validtor;
    }
});


function append_valid_digital(id, st) {
    console.log('append' + st);
    $('#' + id).bootstrapValidator('addField', st, {
        message: 'The filed is not valid',
        validators: {
            notEmpty: {
                message: '不能为空'
            },
            regexp: {           //正则校验 
                regexp: /^(\+|-)?[1-9][0-9]*$/,
                // regexp: /^(\+|-)?([1-9][0-9]*(\.\d+)?|(0\.(?!0+$)\d+))$/,
                message: '请输入非零整数'
            }
        }
    });
}


function append_valid(id, st) {
    console.log('append' + st);
    $('#' + id).bootstrapValidator('addField', st, {
        message: 'The filed is not valid',
        validators: {
            notEmpty: {
                message: '不能为空'
            }
        }
    });
}

function append_valid_enable(id, st) {
    $('#' + id).bootstrapValidator('addField', st, {
        message: 'The filed is not valid',
        validators: {
            notEmpty: {
                message: '不能为空'
            }
        }
    });
}


function remove_valid(id, st) {
    console.log('remove field' + st);
    $('#' + id).bootstrapValidator('removeField', st);
}

function active_valid() {

    $('form').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            /*input状态样式图片*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and can\'t be empty'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The username must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'The username can only consist of alphabetical, number, dot and underscore'
                    }
                }
            },
            time: {
                message: 'time invalid!',
                validators: {
                    notEmpty: {
                        message: '不能为空'
                    }
                }
            }
        }
    })
}
function init_valid(form_id) {
    console.log('init valid' + form_id);

    $('#' + form_id).bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            /*input状态样式图片*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {}
    })
}

function clear_modal_data(modal_id) {
    //清除弹窗原数据
    $("#" + modal_id).on("hidden.bs.modal", function () {
        console.log('clear data');
        $(this).removeData("bs.modal");
    });
}


function is_valid(form_id) {
    var bootstrapValidator = $("#" + form_id).data('bootstrapValidator');
    bootstrapValidator.validate();
    if (bootstrapValidator.isValid()) {
        console.log('success');
        $("#id_modal_submit").attr("disabled", "false");

        $('#myModal').modal('hide');
        // $("#" + form_id).submit();
        // return true;
        return true;
    }
    else {
        $("#id_modal_submit").attr("disabled", "true");
        console.log('failed');
        // return false;
        return false;
    }


}


function global_form_valid() {
    //保存原始的bootstrapValidator
    var overwrite = $.fn.bootstrapValidator; 　　//重载bootstrapValidator
    $.fn.bootstrapValidator = function (options) {
        //恢复原来的bootstrapValidator，因为其加了很多数据是不能丢失的
        $.fn.bootstrapValidator = overwrite;
        //这里有两种做法，第一种是直接修改arguments内容，使其包含不能输入&的验证，然后调用即可；　　　
        // 　//第二种是先使用arguments来初始化，然后使用调用bootstrapValidator的函数来给非正则表达式验证的项添加不能输入&的验证　　　　//这里我们使用了第二中。　　
        var validtor = overwrite.apply(this, arguments);
        if ($.type(arguments[0]) == "object") {
            var vtor = this.data("bootstrapValidator"),　　　　　　//过滤出输入框表单项　　
                fileds = this.find("input[name][type='hidden'],input[name][type='password'],input[name][type='text'],textarea[name]").not(":disabled,[type='hidden']");
            fileds.each(function () {
                //本身没有正则验证才添加不能输入&的验证
                if (!vtor.getOptions($(this).attr('name'), 'regexp', 'regexp')) {
                    vtor.addField($(this).attr('name'),
                        {
                            validators: {
                                notEmpty: {
                                    message: '不能为空'
                                },
                            }
                        })
                }
            })
        }
        return validtor;
    }
}

function auto_form_input_valid() {
    var input_name_arr;
    input_name_list = new Array();

    $('input:visible').each(function () {
        console.log(this);
        var name = $(this).attr('name');
        console.log(name);
        if (name) {
            input_name_list.push(name);
        }
    });
    console.log(input_name_list);
    return input_name_list
}

function add_table_tr(table_id, innerhtml) {
    $('#' + table_id).append(innerhtml);
}
