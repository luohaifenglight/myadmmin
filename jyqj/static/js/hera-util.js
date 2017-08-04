/**
 * Created by Thierry on 5/20/15.
 */
var util = {

    /**
     * @description 警告操作后的提示层，定时消失,见@_showTips
     */
    showWarning: function (opt) {
        opt.type = 'warning';
        this._showTips(opt);
    },

    /**
     * @description 提示操作后的提示层，定时消失,见@_showTips
     */
    showInfo: function (opt) {
        opt.type = 'info';
        this._showTips(opt);
    },

    /**
     * @description 成功操作后的提示层，定时消失,见@_showTips
     */
    showSuccess: function (opt) {
        opt.type = 'success';
        this._showTips(opt);
    },

    /**
     * @description 错误操作后的提示层，定时消失,见@_showTips
     */
    showError: function (opt) {
        opt.type = 'danger';
        this._showTips(opt);
    },

    showMessage: function(opt) {
        opt.type = "success";
        opt.delay = 10;
        this._showTips(opt);
    },

    /**
     * @description 异步操作后的提示层，定时消失
     * @param {JSON} opt 包含以下内容:
     *     @param {String} type success、error、warning，info,默认 success
     *     @param {String} text
     *     @param {Number} delay 显示时间（秒），默认 3 秒
     */
    _showTips: function (opt) {
        var _this = this;
        var classname = 'alert hera-tips alert-' + opt.type;
        var layerid = 'tip_' + (+new Date());
        var tmpl = '<div class="' + classname + '" id="' + layerid + '">' + opt.msg + '</div>';

        $('#wrapper').prepend(tmpl);
        $('#' + layerid).slideDown();
        var t = setTimeout(function () {
            $('#' + layerid).remove();
        }, opt.delay * 1000 || 3000);
    },
    /**
     * @description 重置 DataTable 宽度
     * @param {Object} $dataTable dataTable jQuery 对象
     */
    resizeDataTable: function ($dataTable) {
        if(!$dataTable.length) return;
        var $tableContainer = $dataTable.parents('.dataTables_scroll');
        var $TH = $tableContainer.find('th'); // DataTable 生成的 th
        var $originTH = $dataTable.find('th'); // 表格原始的 th
        var dw = ($tableContainer.width() - $dataTable.width()) / $TH.length >> 0;
        var $container = $([$dataTable, $tableContainer.find('table'), $tableContainer.find('.dataTables_scrollHeadInner')]);

        $container.each(function () {
            $(this).css('width', '100%');
        });

        $originTH.each(function () {
            var $this = $(this);
            $this.css('width', $this.width() + dw);
        });

        $TH.each(function (index) {
            $(this).css({'width': $($originTH[index]).css('width'), 'vertical-align': 'top'});
        });
    },
    // 当 Select2 有选中项时，禁止按 Backspace 删除，只能用 X 按钮删除
    disableSelect2Backspace: function () {
        $('.select2-search__field').on('keydown', function (e) {
            if(e.keyCode == 8 && !$(this).val().length) {
                e.preventDefault();
                return false;
            }
        });
    }
};


 /**
     * 侦查附件上传情况
     */
function uploadProgress(evt) {
        var loaded = evt.loaded, // 已经上传大小情况
            total = evt.total, // 附件总大小
            percent = Math.floor(100 * loaded / total); // 已经上传的百分比
        if(percent == 100){
            percent = 99.99;
        }
        $.bootstrapLoading.uploading( percent + "%");
        console.log(percent);
    }
  // 显示上传进度
xhr_process = function () {
        var xhr = $.ajaxSettings.xhr();
        if (uploadProgress && xhr.upload) {
            xhr.upload.addEventListener("progress", uploadProgress, false);
        }
        return xhr;
    };





// 帖子文件上传
(function () {
    'use strict';
    var fileManager = $('.js_file_manager');
    var raw_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-w";
            }
            return url;
        }else{
            return "";
        }
    };
    var thumb_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-thumb";
            }
            return url;
        }else{
            return "";
        }
    };

    if(fileManager.length) {
        fileManager.on('click', function (e) {
            var $target = $(e.target);
            var $this = $(this);
            var $a = $this.find('.js_file_raw');
            var $thumb = $this.find('.js_file_thumb');
            var $url = $this.find('.js_file_url');
            if($target.hasClass('js_file_del')) {
                var conf = confirm('确定要删除吗？');
                if(conf) {
                    $url.val('');
                    console.log('delete00');
                    var $file_a = $this.find('.js_file_a');
                    $file_a.val('');
                    //$this.hide();
                }
            } else if($target.hasClass('js_file_update')) {
                var val = $url.val();
                if(/^http/.test(val)) {
                    $a.attr('href', raw_url(val));
                    $thumb.attr('src', thumb_url(val));
                } else {
                    alert('请输入正确的图片地址');
                }
            } else if($target.hasClass('js_file_upload')) {
                var $upload = $('.js_file_upload');
                if(!$._data($upload[0], 'events')) {
                    $upload.on('change', function (e) {
                        var $this = $(this).closest('table');
                        var $a = $this.find('.js_file_raw');
                        var $thumb = $this.find('.js_file_thumb');
                        var $url = $this.find('.js_file_url');
                        var $file_a = $this.find('.js_file_a');
                        var $save_thumb = $this.find('.js_save_thumb')
                        var $save_size = $this.find('.js_save_size')
                        var $save_time_l = $this.find('.js_save_time_l')
                        var $js_td_show_thumb = $this.find('.js_td_show_thumb')
                        var $js_td_show_input = $this.find('.js_td_show_input')
                        var file = this.files[0];
                        var $file_type = $this.find('.file_type').val();
                        console.log(file.name);
                        console.log($file_type);
                        if($file_type != "all"){
                            if(file.name.indexOf($file_type)==-1){
                            var parent_dom = $this.parent();
                            parent_dom.addClass("has-error");
                            var error_html = '<p class="error-status help-block has-error">请选择正确的'+$file_type+'文件</p>';
                            parent_dom.append(error_html);
                            // alert("请选择正确的"+$file_type +"文件");
                            return;
                        }
                        else{
                                 var parent_dom = $this.parent();
                                 parent_dom.removeClass("has-error");
                                 parent_dom.find('.error-status').remove();
                            }
                        }

                        var form = new FormData();
                        form.append($(this).attr('name'), file);
                        form.append('img_type', '99'); // 不带水印
                        $.bootstrapLoading.start({ loadingTips: "正在上传，请稍候..." });
                        $.ajax({
                            url: '/upload/image_with_type/',
                            type: 'POST',
                            cache: false,
                            contentType: false,
                            processData: false,
                            xhr: xhr_process,
                            data: form,
                            success: function(data, status){
                                $.bootstrapLoading.end();
                                var img_url = data.file;
                                if (data.thumb_url != '' && data.thumb_url){
                                    $a.attr('href', data.thumb_url);
                                    $thumb.attr('src', data.thumb_url);
                                    $a.show();
                                    $thumb.show();
                                    $js_td_show_thumb.show();
                                    $js_td_show_input.hide();
                                    console.log(data.thmub_url);
                                }
                                else
                                {
                                    console.log('14');
                                    $thumb.hide();
                                    console.log('1');
                                    $js_td_show_thumb.hide();
                                    $js_td_show_input.show();
                                    console.log('12');
                                }
                                if ($save_thumb){
                                    $save_thumb.val(data.thumb_url)
                                }
                                if ($save_time_l){
                                    $save_time_l.val(data.time_l)
                                }
                                if ($save_size){
                                    $save_size.val(data.size)
                                }
                                $url.val(img_url);
                                var path_name = data.address;
                                //$a.attr('href', raw_url(img_url));
                                //$thumb.attr('src', thumb_url(img_url));
                                $url.val(path_name);
                                $file_a.val(img_url);
                                 $('form').data('bootstrapValidator').resetForm();
                                $('form').data('bootstrapValidator').validate();
                                //$file_a.attr('href', path_name);
                            }
                        });
                    });
                }
            }
        });
    }
})();



upload_image_version2=function () {
    'use strict';
    var fileManager = $('.js_file_manager');
    var raw_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-w";
            }
            return url;
        }else{
            return "";
        }
    };
    var thumb_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-thumb";
            }
            return url;
        }else{
            return "";
        }
    };

    if(fileManager.length) {
        fileManager.each(function(){
           var $that=$(this);
        $that.on('click', function (e) {
            var $this = $target.closest('.js_file_manager');
            var $a = $this.find('.js_file_raw');
            var $thumb = $this.find('.js_file_thumb');
            var $url = $this.find('.js_file_url');
            if($target.hasClass('js_file_del')) {
                var conf = confirm('确定要删除吗？');
                if(conf) {
                    $url.val('');
                    console.log('delete00');
                    var $file_a = $this.find('.js_file_a');
                    $file_a.val('');
                    //$this.hide();
                }
            } else if($target.hasClass('js_file_update')) {
                var val = $url.val();
                if(/^http/.test(val)) {
                    $a.attr('href', raw_url(val));
                    $thumb.attr('src', thumb_url(val));
                } else {
                    alert('请输入正确的图片地址');
                }
            } else if($target.hasClass('js_file_upload')) {

                if(!$._data($target, 'events')) {
                    $target.off('change');
                    $target.on('change', function (e) {
                        var $this = $(this).closest('table');
                        var $a = $this.find('.js_file_raw');
                        var $thumb = $this.find('.js_file_thumb');
                        var $url = $this.find('.js_file_url');
                        var $file_a = $this.find('.js_file_a');
                        var $save_thumb = $this.find('.js_save_thumb')
                        var $save_size = $this.find('.js_save_size')
                        var $save_time_l = $this.find('.js_save_time_l')
                        var $js_td_show_thumb = $this.find('.js_td_show_thumb')
                        var $js_td_show_input = $this.find('.js_td_show_input')
                        var file = this.files[0];
                        var form = new FormData();
                        console.log(file.name);
                        if(file.name.indexOf('.py')>0){
                            return;
                        }
                        form.append($(this).attr('name'), file);
                        form.append('img_type', '99'); // 不带水印
                        $.ajax({
                            url: '/upload/image_with_type/',
                            type: 'POST',
                            cache: false,
                            contentType: false,
                            processData: false,
                            data: form,
                            success: function(data, status){
                                var img_url = data.file;
                                if (data.thumb_url != '' && data.thumb_url){
                                    $a.attr('href', data.thumb_url);
                                    $thumb.attr('src', data.thumb_url);
                                    $a.show();
                                    $thumb.show();
                                    $js_td_show_thumb.show();
                                    $js_td_show_input.hide();
                                    console.log(data.thumb_url);
                                }
                                else
                                {
                                    console.log('14');
                                    $thumb.hide();
                                    console.log('1');
                                    $js_td_show_thumb.hide();
                                    $js_td_show_input.show();
                                    console.log('12');
                                }
                                if ($save_thumb){
                                    $save_thumb.val(data.thumb_url)
                                }
                                if ($save_time_l){
                                    $save_time_l.val(data.time_l)
                                }
                                if ($save_size){
                                    $save_size.val(data.size)
                                }
                                $url.val(img_url);
                                var path_name = data.address;
                                //$a.attr('href', raw_url(img_url));
                                //$thumb.attr('src', thumb_url(img_url));
                                $url.val(path_name);
                                $file_a.val(img_url);
                                $('form').data('bootstrapValidator').resetForm();
                                $('form').data('bootstrapValidator').validate();
                                //$file_a.attr('href', path_name);
                            }
                        });
                    });
                }
            }
        });

        })
    }
};

upload_image_with_type_version2=function () {
    'use strict';
    var fileManager = $('.js_file_manager');

    var _fn = function (e) {
            var $target = $(e.target);
            var $this = $target.closest('.js_file_manager');
            var $a = $this.find('.js_file_raw');
            var $thumb = $this.find('.js_file_thumb');
            var $url = $this.find('.js_file_url');
            if($target.hasClass('js_file_del')) {
                var conf = confirm('确定要删除吗？');
                if(conf) {
                    $url.val('');
                    console.log('delete00');
                    var $file_a = $this.find('.js_file_a');
                    $file_a.val('');
                    //$this.hide();
                }
            } else if($target.hasClass('js_file_update')) {
                var val = $url.val();
                if(/^http/.test(val)) {
                    $a.attr('href', val);
                    $thumb.attr('src', val);
                } else {
                    alert('请输入正确的图片地址');
                }
            } else if($target.hasClass('js_file_upload')) {

                if(!$._data($target, 'events')) {
                    $target.off('change');
                    $target.on('change', function (e) {
                         var $this = $(this).closest('table');
                        var $a = $this.find('.js_file_raw');
                        var $thumb = $this.find('.js_file_thumb');
                        var $url = $this.find('.js_file_url');
                        var $file_a = $this.find('.js_file_a');
                        var $save_thumb = $this.find('.js_save_thumb')
                        var $save_size = $this.find('.js_save_size')
                        var $save_time_l = $this.find('.js_save_time_l')
                        var $js_td_show_thumb = $this.find('.js_td_show_thumb')
                        var $js_td_show_input = $this.find('.js_td_show_input')
                        var file = this.files[0];
                        var form = new FormData();
                        form.append($(this).attr('name'), file);
                        form.append('img_type', '99'); // 不带水印
                        $.ajax({
                            url: '/upload/image_with_type/',
                            type: 'POST',
                            cache: false,
                            contentType: false,
                            processData: false,
                            data: form,
                            success: function(data, status){
                                var img_url = data.file;
                                if (data.thumb_url != '' && data.thumb_url){
                                    $a.attr('href', data.thumb_url);
                                    $thumb.attr('src', data.thumb_url);
                                    $a.show();
                                    $thumb.show();
                                    $js_td_show_thumb.show();
                                    $js_td_show_input.hide();
                                    console.log(data.thmub_url);
                                }
                                else
                                {
                                    console.log('14');
                                    $thumb.hide();
                                    console.log('1');
                                    $js_td_show_thumb.hide();
                                    $js_td_show_input.show();
                                    console.log('12');
                                }
                                if ($save_thumb){
                                    $save_thumb.val(data.thumb_url)
                                }
                                if ($save_time_l){
                                    $save_time_l.val(data.time_l)
                                }
                                if ($save_size){
                                    $save_size.val(data.size)
                                }
                                $url.val(img_url);
                                var path_name = data.address;
                                //$a.attr('href', raw_url(img_url));
                                //$thumb.attr('src', thumb_url(img_url));
                                $url.val(path_name);
                                $file_a.val(img_url);
                                 $('form').data('bootstrapValidator').resetForm();
                                $('form').data('bootstrapValidator').validate();
                                //$file_a.attr('href', path_name);
                            }
                        });
                    });
                }
            }
        }

    if(fileManager.length) {
        fileManager.each(function(){
            var $that=$(this);
            $that.on('click', _fn);
        })
    }
};


(function () {
    'use strict';
    var fileManager = $('.js_file_manager_with_type');
    var raw_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-w";
            }
            return url;
        }else{
            return "";
        }
    };
    var thumb_url = function(url){
        if(typeof(url) == "string"){
            if(url.indexOf('-') == -1){
                return url + "-thumb";
            }
            return url;
        }else{
            return "";
        }
    };

    if(fileManager.length) {
        fileManager.on('click', function (e) {
            var $target = $(e.target);
            var $this = $(this);
            var $a = $this.find('.js_file_raw');
            var $thumb = $this.find('.js_file_thumb');
            var $url = $this.find('.js_file_url');
            if($target.hasClass('js_file_del')) {
                var conf = confirm('确定要删除吗？');
                if(conf) {
                    $url.val('');
                    console.log('delete00');
                    var $file_a = $this.find('.js_file_a');
                    $file_a.val('');
                    //$this.hide();
                }
            } else if($target.hasClass('js_file_update')) {
                var val = $url.val();
                if(/^http/.test(val)) {
                    $a.attr('href', raw_url(val));
                    $thumb.attr('src', thumb_url(val));
                } else {
                    alert('请输入正确的图片地址');
                }
            } else if($target.hasClass('js_file_upload')) {
                var $upload = $('.js_file_upload');
                if(!$._data($upload[0], 'events')) {
                    $upload.on('change', function (e) {
                        var $this = $(this).closest('table');
                        var $a = $this.find('.js_file_raw');
                        var $thumb = $this.find('.js_file_thumb');
                        var $url = $this.find('.js_file_url');
                        var $file_a = $this.find('.js_file_a');
                        var file = this.files[0];
                        var form = new FormData();
                        form.append($(this).attr('name'), file);
                        form.append('img_type', $(this).attr('img_type'));
                        $.ajax({
                            url: '/upload/image_with_type/',
                            type: 'POST',
                            cache: false,
                            contentType: false,
                            processData: false,
                            data: form,
                            success: function(data, status){
                                var img_url = data.file;
                                var path_name = data.address;
                                //$a.attr('href', raw_url(img_url));
                                //$thumb.attr('src', thumb_url(img_url));
                                $url.val(path_name);
                                $file_a.text(img_url);
                                $file_a.attr('href', 'http:127.0.0.1:8080/uploadfiles/'+path_name);
                            }
                        });
                    });
                }
            }
        });
    }
})();

MultiSelect=function(dom) {
        var searchDom = dom;
        searchDom.multiSelect({
            selectableOptgroup: true,
            selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='请输入城市'>",
            selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='请输入城市'>",
            afterInit: function (ms) {
                var that = this,
                        $selectableSearch = that.$selectableUl.prev(),
                        $selectionSearch = that.$selectionUl.prev(),
                        selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
                        selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

                that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                        .on('keydown', function (e) {
                            if (e.which === 40) {
                                that.$selectableUl.focus();
                                return false;
                            }
                        });

                that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                        .on('keydown', function (e) {
                            if (e.which == 40) {
                                that.$selectionUl.focus();
                                return false;
                            }
                        });
            },
            afterSelect: function () {
                this.qs1.cache();
                this.qs2.cache();
            },
            afterDeselect: function () {
                this.qs1.cache();
                this.qs2.cache();
            }
        });
    };

