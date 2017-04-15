/**
 * Created by yuan on 2017/3/19.
 */

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var emailInput = $('input[name=email]');
        var usernameInput = $('input[name=username]');
        var passwordInput = $('input[name=password]');
        var rolesCheckbox = $(':checkbox:checked');

        var email = emailInput.val();
        var password = passwordInput.val();
        var username = usernameInput.val();
        var roles = [];
        rolesCheckbox.each(function (index,element) {
            roles.push($(this).val());
        });
        
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
        }
        if(!password){
            xtalert.alertInfoToast('请输入密码');
        }
        if(!username){
            xtalert.alertInfoToast('请输入用户名');
        }
        if(roles.length <= 0){
            xtalert.alertInfoToast('请选择至少一个分组');
        }

        phajax.post({
            'url':'/cms/addcmsuser/',
            'data':{
                'email':email,
                'password':password,
                'username':username,
                'roles':roles
            },
            'success':function (data) {
                if(data['code'] == 200){
                    emailInput.val('');
                    passwordInput.val('');
                    usernameInput.val('');
                    rolesCheckbox.each(function (index,element) {
                        $(this).prop('checked',false);
                    });
                    xtalert.alertSuccessToast('cms用户添加成功');
                }else{
                    xtalert.alertErrorToast(data['message']);
                }
            }
        });
        
    });
});
