var select2_remote_options = {
    minimumInputLength: 0,
    ajax: {
        url: $(this).attr("data-ajax--url"),
        dataType: "json",
        data: function (params) {
            return {
                q: params.term,
                page: params.page
            };
        },
        processResults: function (data, params) {
            var num = data.num;
            params.page = params.page || 1;
            var more = data.results.length == num;
            //var more = (data.page * num) < data.total_count;
            data.pagination = {more: more};
            return data;
        },
        cache: true
    },
}
var select2_remote_multiple_options = {
    multiple: true,
    closeOnSelect: false,
};
$.extend(true, select2_remote_multiple_options, select2_remote_options);
$(".select2-remote").select2(select2_remote_options)
    .on('select2:open select2:close', function () {
        util.disableSelect2Backspace();
    });
$(".select2-remote-multiple").select2(select2_remote_multiple_options)
    .on('select2:open select2:close', function () {
        util.disableSelect2Backspace();
    });

function select2_init() {
    $.extend(true, select2_remote_multiple_options, select2_remote_options);
    $(".select2-remote").select2(select2_remote_options)
        .on('select2:open select2:close', function () {
            util.disableSelect2Backspace();
        });
    $(".select2-remote-multiple").select2(select2_remote_multiple_options)
        .on('select2:open select2:close', function () {
            util.disableSelect2Backspace();
        });
}

