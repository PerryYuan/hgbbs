/**
 * Created by Administrator on 2017/3/20.
 */

$(function () {
   $('#send-captcha-btn').click(function (event) {
       event.preventDefault();
       // 获取手机号码
       var self = $(this);
       var telephone = $('input[name=telephone]').val();
       if(!telephone){
           xtalert.alertInfoToast('请输入手机号码！');
           return;
       }
       phajax.get({
           'url': '/alidayu_captcha/',
           'data':{'telephone':telephone},
           'success':function (data) {
               if(data['code'] == 200){
                   self.attr('disabled','disabled');
                   self.css('cursor','default');
                   var m_time = 60;
                   var timer = setInterval(function () {
                       self.text(m_time--);
                       if(m_time <= 0){
                           self.text('发送验证码');
                           self.removeAttr('disabled');
                           clearInterval(timer);
                       }
                   },1000);
                   xtalert.alertSuccessToast('手机验证码发送成功');
               }else{
                   xtalert.alertInfoToast(data['message']);
               }
           }
       })
   })
});
