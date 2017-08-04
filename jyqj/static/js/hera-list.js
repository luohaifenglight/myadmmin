function filter_datetime_range(dt, name){
    var datetime_min = $("input[name="+ name +"_min]").val();
    var datetime_max = $("input[name="+ name +"_max]").val();
    var datetime = datetime_min + ',' + datetime_max;
    dt.column(name+":name").search(datetime, false).draw();
}
function filter_multivalues(dt, name){
    var values_joinby_comma = $("input[name="+ name +"]:checked").map(
            function(){return this.value;}).get().join(",");
    dt.column(name+":name").search(values_joinby_comma, false).draw();
}
function filter_singlevalue(dt, name){
    var val = $("input[name="+ name +"]:checked").val();
    dt.column(name+":name").search(val, false).draw();
}
function filter_selected(dt, name){
    var val = $("select[name="+ name +"]").val();
    if(val == null){
        dt.column(name+":name").search("").draw();
    }else{
        dt.column(name+":name").search(val, false).draw();
    }
}

//===== datatable render function =====
function render_editlink_factory(url){
    var url = url;
    return function(data, type, row, meta){
        var id = row.DT_RowData.pk;
        //var uri = meta.settings.editlink_pre;
        var edit_link = '<a href="'+url+id+'/" target="_blank">'+data+'</a>';
        return edit_link;
    }
}
function render_boolvalue(data, type, row, meta){
    if(data){
        return '是'
    }else{
        return '否'
    }
}

function render_checkbox(data, type, row, meta){
    var edit_link = '<input type="checkbox" value="'+row.DT_RowData.pk+'"></input>'
    if(data){
        var edit_link = '<input type="checkbox" checked="checked" value="'+row.DT_RowData.pk+'"></input>';
    }
    return edit_link;
}

function render_text(data, type, row, meta){
    var edit_link = '<input type="text" class="form-control" style="width:100px" value="'+data+'"></input>'
    return edit_link;
}

function render_datetime(data, type, row, meta){
    if(data){
        return data.split('.')[0]
    }
    return data
}

function render_dict(dict){
    var dict = dict;
    return function(data, type, row, meta){
        return dict[data];
    }
}

function render_date(data, type, row, meta){
    if(data){
        return data.split(' ')[0]
    }
    return data
}

function render_editlink(url) {
    var url = url;
    return function (data, type, row, meta) {
        console.log(data);
        if(!data){
            return data
        }
        var id = data.id;
        var edit_link = '<a href="' + url + id + '/" target="_blank">' + data.text + '</a>';
        return edit_link;
    }
}
//=========== end ==========


// ========= 搜索开始==========
Array.prototype.contains = function (obj) {
    for(var i=0;i<this.length;i++)
    if (this[i] === obj) {
        return true;
    }
    return false;
};

function search_base(option){
    var v = $("input[name='srch_value']").val();
    var k = $("input[type='radio'][name='srch_field']:checked").val();
    var dt = $('#dataTables').DataTable();

    // query item
    $("input[type='radio'][name='srch_field']").each(function(){
        var name = $(this).val();
        if(name) {
            dt.column(name+':name').search('', false);
        }
    });
    if(k){
        dt = dt.search('').column(k+":name").search(v, true);
    }else{
        dt = dt.search(v, true);
    }

    var filterBody = $('.gm-search-body');
    // 单选按钮组
    filterBody.find('input[type=radio]:checked').each(function(){
        var name = $(this).attr("name");
        var val =$(this).val();
        dt.column(name+":name").search(val, false);
    });
    // 多选按钮组
    var checkboxDict = {};
    filterBody.find('input[type=checkbox].instant-filter').each(function(){
        var name = $(this).attr("name");
        var val =$(this).val();
        if(!checkboxDict.hasOwnProperty(name)){
            if(val !=null && val.length>0 && ($('input[name='+ name +']:checked').length==0)){
               checkboxDict[name]= val.split(',');
            }else{
            checkboxDict[name]=[];
            }
        }
        if($(this).prop("checked")){

            checkboxDict[name].push(val);
        }
    });
    for(var key in checkboxDict) {
        if(checkboxDict[key].contains('all')){
            // 用 all 标识全部， 只要全部被勾选就搜索全部类型
            dt.column(key + ":name").search('', false);
        }else {
            var values_joinby_comma = checkboxDict[key].join(',');
            dt.column(key + ":name").search(values_joinby_comma, false);
        }
    }
    // select
    console.log('st');
    filterBody.find('select').each(function(){
        var name = $(this).attr("name");
        var val = $(this).val();
        if(val == null){
            dt.column(name+":name").search('');
            console.log('12314');
        }else{
            dt.column(name+":name").search(val, false);
            console.log(val);
        }
    });
    // date time range
    datetimeElems = filterBody.find('input.datetime-range');
    for(var i=0;i<datetimeElems.length;i++){
        var elem = $(datetimeElems[i]);
        var name = elem.attr('range_name');
        if((i+1)%2==0){
            var min_val = $(datetimeElems[i-1]).val();
            var max_val = $(datetimeElems[i]).val();
            if(min_val=='' && max_val==''){
                dt.column(name+":name").search('', false)
            }else{
                var datetime = min_val + ',' + max_val;
                dt.column(name+":name").search(datetime, false)
            }
        }
    }
    if(option == 0){
       dt.draw();
    }else{
        var page = dt.page();
        dt.page(page).draw(false);
    }


}

function search(){
    search_base(1);

}

function search_click(){
    search_base(0);
}
// ========== end 搜索 ============
