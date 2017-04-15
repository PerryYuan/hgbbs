/**
 * Created by yuan on 2017/3/16.
 */

$(function () {
    $('#btn_save').click(function (event) {
        event.preventDefault();
        oldpwdInput = $('input[name=oldpwd]');
        newpwdInput = $('input[name=newpwd]');
        newpwd_repeatInput = $('input[name=newpwd_repeat]');

        oldpwd = oldpwdInput.val();
        newpwd = newpwdInput.val();
        newpwd_repeat = newpwd_repeatInput.val();

        phajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd_repeat':newpwd_repeat
            },
            'success':function (data) {
                oldpwdInput.val('');
                newpwdInput.val('');
                newpwd_repeatInput.val('');
                if(data['code'] == 200){
                    xtalert.alertSuccess('密码修改成功');
                }else{
                    xtalert.alertError(data['message'])
                }
            },
        });
    });
});
