$(function () {
    $("#search").click(function () {
        $("#ip_table").DataTable().draw(true);
    });
    $("#create_task").click(function () {
        $('#newTask').modal('toggle');
    });
    $("#start_task").click(function () {
        const target = $('#text_target').val();
        var port = $('#input_port').val();
        var rate = $('#input_rate').val();
        if (!target) {
            swal('Warning', '请至少输入一个Target', 'error');
            return;
        }
        if (!port) port = "--top-ports 1000";
        if (!rate) rate = 5000;
        $.post("/task-start-portscan",
            {
                "target": target,
                "port": port,
                'rate': rate,
                'nmap_tech': $('#select_tech').val(),
                'org_id': $('#select_org').val(),
                'iplocation': $('#checkbox_iplocation').is(":checked"),
                'webtitle': $('#checkbox_webtitle').is(":checked"),
                'ping': $('#checkbox_ping').is(":checked"),
                'fofasearch': $('#checkbox_fofasearch').is(":checked")
            }, function (data, e) {
                if (e === "success" && data['status'] == 'success') {
                    swal({
                        title: "新建任务成功！",
                        text: "TaskId:" + data['result']['task-id'],
                        type: "success",
                        confirmButtonText: "确定",
                        confirmButtonColor: "#41b883",
                        closeOnConfirm: true,
                    },
                        function () {
                            $('#newTask').modal('hide');
                        });
                } else {
                    swal('Warning', "添加任务失败!", 'error');
                }
            });

    });



    $('#ip_table').DataTable(
        {
            "paging": true,
            "searching": false,
            "processing": true,
            "serverSide": true,
            "autowidth": true,
            "sort": false,
            "pagingType": "full_numbers",//分页样式
            'iDisplayLength': 20,
            "dom": '<t><"bottom"ip>',
            "ajax": {
                "url": "/ip-list",
                "type": "post",
                "data": function (d) {
                    return $.extend({}, d, {
                        "org_name": $('#org_name').val(),
                        "ip_address": $('#ip_address').val(),
                        "port": $('#port').val()
                    });
                }
            },
            columns: [
                {
                    data: "id",
                    width: "5%",
                    title: '<input title="checkbox_all" type="checkbox" id="all_select" value="1" />',
                    "sClass": "center",
                    "salign": "center",
                    "render": function (data, type, full) { return '<input title="checkbox_all" type="checkbox" id="all_select" value="1"/>'; }
                },
                { data: "index", title: "序号", width: "5%" },
                {
                    data: "ip",
                    title: "IP地址",
                    width: "12%",
                    render: function (data, type, row, meta) {
                        return '<a href="/ip-info?ip=' + data + '">' + data + '</a>';
                    }
                },
                { data: "port", title: "开放端口", width: "40%" },
                { data: "org_name", title: "所属组织机构", width: "15%" },
                { data: "update_time", title: "更新时间", width: "15%" },
                {
                    title: "操作",
                    "render": function (data, type, row, meta) {
                        var strDelete = "<a href=javascript:delete_ip(" + row.id + ")><i class='fa fa-pencil'></i><span>删除</span></a>";
                        return strDelete;
                    }
                }
            ],
            infoCallback: function (settings, start, end, max, total, pre) {
                var api = this.api();
                var pageInfo = api.page.info();
                return "共<b>" + pageInfo.pages + "</b>页,当前显示" + start + "到" + end + "条记录" + ",共有<b>" + total + "</b>条记录";
            },
        }
    );//end datatable
});

function delete_ip(id) {
    swal({
        title: "确定要删除?",
        text: "该操作会删除这个IP的所有信息！",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确认删除",
        cancelButtonText: "取消",
        closeOnConfirm: true
    },
        function () {
            $.ajax({
                type: 'post',
                url: '/ip-delete/' + id,
                success: function (data) {
                    $("#ip_table").DataTable().draw(false);
                },
                error: function (xhr, type) {
                }
            });
        });
}

