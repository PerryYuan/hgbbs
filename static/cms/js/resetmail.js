/**
 * Created by yuan on 2017/3/16.
 */

$(function () {
    $('#get_captcha').click(function (event) {
        event.preventDefault();
        var mail = $('input[name=mail]').val();
        phajax.get({
            'url':'/captcha/',
            'data':{
                'mail':mail
            },
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('验证码发送成功。');
                }else{
                    xtalert.alertErrorToast(data['message'])
                }
            },
            'fail':function (errors) {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $('#resetmail').click(function (event) {
        event.preventDefault();
        var mailInput = $('input[name=mail]');
        var captchaInput = $('input[name=captcha]');

        var mail = mailInput.val();
        var captcha = captchaInput.val();

        phajax.post({
            'url':'/resetmail/',
            'data': {
                'mail': mail,
                'captcha': captcha
            },
            'success':function (data) {
                mailInput.val('');
                captchaInput.val('');
                if(data['code'] == 200){
                    xtalert.alertSuccess('邮箱修改成功。');
                }else{
                    xtalert.alertError(data['message']);
                }
            },
        });
    });
});
