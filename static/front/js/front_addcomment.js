/**
 * Created by yuan on 2017/4/2.
 */

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var comment_id = $(this).attr('data-comment-id');
        var content = window.editor.$txt.html();
        phajax.post({
            'url': '/add_comment/',
            'data':{
                'post_id': post_id,
                'content': content,
                'comment_id': comment_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜，评论发表成功。');
                    setTimeout(function () {
                        window.location = 'http://ph.com:5000/post_detail/'+post_id+'/';
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});
