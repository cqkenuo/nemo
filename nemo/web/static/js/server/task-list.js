$(function () {
    $('#tasks-table').DataTable(
        {
            "rowID": 'uuid',
            "paging": true,
            "searching": false,
            "processing": true,
            "serverSide": true,
            "autowidth": true,
            "sort": false,
            "dom": '<t><"bottom"ip>',
            "ajax": {
                "url": "/task-list",
                "type": "post",
                "data": function (d) {
                    return $.extend({}, d, {
                        "task_status": $('#task_status').val()
                    });
                }
            },
            columns: [
                { data: 'uuid', title: 'task-id', width: '15%' },
                { data: 'name', title: '名称', width: '10%' },
                { data: 'state', title: '状态', width: '5%' },
                { data: 'kwargs', title: '参数', width: '25%' },
                { data: 'result', title: '结果', width: '10%' },
                { data: 'received', title: '接收时间', width: '8%' },
                { data: 'started', title: '启动时间', width: '8%' },
                { data: 'runtime', title: '执行时长', width: '8%' }
            ]
        }
    );//end datatable

    $("#task_status").change(function () {
        $('table').DataTable().draw(false);
    });

    $("#refresh").click(function () {
        $('table').DataTable().draw(false);
    });

    //全选 
    $('table th input:checkbox').on(
        'click',
        function () {
            var that = this;
            $(this).closest('table').find(
                'tr > td:first-child input:checkbox').each(
                    function () {
                        this.checked = that.checked;
                        $(this).closest('tr').toggleClass('selected');
                    });

        });

});