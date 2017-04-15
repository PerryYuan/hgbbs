/**
 * Created by yuan on 2017/3/25.
 */

$(function () {
    $('.deal-active').click(function (event) {
        event.preventDefault();
        var user_id = $(this).attr('data-user-id');
        var active = $(this).attr('data-active');
        phajax.post({
           'url':'/cms/frontuserblack/',
            'data':{
                'user_id':user_id
            },
            'success':function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(active == '1'){
                        msg = '已拉入黑名单';
                    }else{
                        msg = '已移出黑名单';
                    }
                    xtalert.alertSuccessToast(msg);
                    setInterval(function () {
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});
