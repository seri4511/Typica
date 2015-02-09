var editor; // use a global for the submit and return data rendering in the examples

$(document).ready(function() {

    var $result = $('#eventsResult');
    var target_id = '';

    $('#server-list-table').on('check.bs.table', function (e, row) {
//        $result.text(row['email']);
        target_id = {id : row['id']};
        $('#targetid').text(row['id']);
    })

    $('#btn_delete_user').click(function () {
        $.ajax({
            url:'deleteuser',
            type:'post',
            data:target_email,
            success:function(data){
                alert("삭제되었습니다");
                $('#server-list-table').bootstrapTable("refresh", {silent: true});

                $('#delete-form').modal('hide');
            }
        })
    });

} );