/**
 * Created by yuan on 2017/3/26.
 */


$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name=title]');
        var captchaInput = $('input[name=graph_captcha]');
        var board_id = $('.select-board').val();
        var content = window.editor.$txt.html();
        var title = titleInput.val();
        var captcha = captchaInput.val();

        phajax.post({
            'url': '/add_post/',
            'data':{
                'title': title,
                'content': content,
                'graph_captcha': captcha,
                'board_id': board_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertConfirm({
                        'msg': '恭喜，文章发表成功。',
                        'confirmText': '再发一篇',
                        'cancelText': '返回首页',
                        'confirmCallback': function () {
                            titleInput.val('');
                            captchaInput.val('');
                            window.editor.clear();
                            $('#flush-captcha').click();
                        },
                        'cancelCallback': function () {
                            window.location = '/';
                        }
                    });
                }else{
                    xtalert.alertInfoToast(data['message']);
                    $('#flush-captcha').click();
                }
            }
        });

    });
});

