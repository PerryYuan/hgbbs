/**
 * Created by yuan on 2017/4/8.
 */

$(function () {
    $('#save-btn').click(function (event) {
        event.preventDefault();
        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var email = $('input[name=email]').val();
        var qq = $('input[name=qq]').val();
        var signature = $('#signature').val();
        var avatar = $('#avatar-img').attr('src');
        phajax.post({
            'url': '/user_setting/',
            'data': {
                'username':username,
                'realname':realname,
                'email':email,
                'qq':qq,
                'avatar':avatar,
                'signature':signature
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('修改成功。');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});
$(function () {
    xtqiniu.setUp({
    'browse_btn':'avatar-img',
    'success': function (up,file,info) {
        var avatar = file.name;
        $('#avatar-img').attr('src',avatar);
    }
    });
});
