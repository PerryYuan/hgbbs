/**
 * Created by yuan on 2017/3/21.
 */

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var checkboxInput = $(':checkbox:checked');
        role_id_list = [];
        var user_id = $(this).attr('data-user-id');
        checkboxInput.each(function (index,element) {
            role_id_list.push($(this).val());
        });
        phajax.post({
            'url':'/cms/edit_cmsuser/',
            'data':{
                'user_id':user_id,
                'role_id_list':role_id_list
            },
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('用户信息修改成功');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

$(function () {
    $('#black').click(function (event) {
        event.preventDefault();
        var user_id = $('#submit').attr('data-user-id');
        phajax.post({
            'url':'/cms/remove_black/',
            'data':{'user_id':user_id},
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('修改成功');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});