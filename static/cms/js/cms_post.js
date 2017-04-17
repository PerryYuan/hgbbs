/**
 * Created by yuan on 2017/4/1.
 */

$(function () {
    $('.is-highlight').click(function (event) {
        event.preventDefault();
        var is_highlight = parseInt($(this).attr('data-is-highlight'));
        var post_id = $(this).attr('data-post-id');

        phajax.post({
            'url':'/cms/highlight/',
            'data':{
                'is_highlight': !is_highlight,
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_highlight){
                        msg = '取消加精成功';
                    }else{
                        msg = '加精成功'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message'])
                }
            }
        });
    });
});



$(function () {
    $('.remove-post').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        phajax.post({
            'url': '/cms/remove_post/',
            'data':{
                'post_id': post_id
            },
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('帖子移除成功');
                    setTimeout(function () {
                        window.location.reload();
                    },500)
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

$(function () {
    $('#post-sort').change(function (event) {
        event.preventDefault();
        var type = $(this).val();
        var new_href = xtparam.setParam(window.location.href,'sort',type);
        window.location = new_href;
    });
});

$(function () {
    $('#post-filter').change(function (event) {
        event.preventDefault();
        var type = $(this).val();
        var new_href = xtparam.setParam(window.location.href,'board',type);
        var new_href = xtparam.setParam(new_href,'page',1);
        window.location = new_href;
    });
});
