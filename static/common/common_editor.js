/**
 * Created by yuan on 2017/4/2.
 */

$(function () {
    var progress_box = $('#progress-box');
    console.log('fdsafdas'+progress_box);
    var progress_bar = progress_box.children(0);
    xtqiniu.setUp({
        'browse_btn': 'pictureandvedio',
        'success': function (up,file,info) {
            var file_path = file.name;
            var data = {
                'file_path' :file_path
            };
            if(file.type.indexOf('image') >= 0){
                var img = template('img',data);
                window.editor.$txt.append(img);
            }else{
                var video = template('video',data);
                window.editor.$txt.append(video);
            }
        },
        'fileadded': function (up,files) {
            progress_box.show();
            $('#pictureandvedio').button('loading');
        },
        'progress': function (up,file) {
            var percent = file.percent;
            progress_bar.attr('aria-valuenow',percent);
            progress_bar.css('width',percent+'%');
            progress_bar.text(percent+'%');
        },
        'complete': function () {
            progress_box.hide();
            progress_bar.attr('aria-valuenow',0);
            progress_bar.css('width','0%');
            progress_bar.text('0%');
            $('#pictureandvedio').button('reset');
        }
    });
});


$(function () {
    var editor = new wangEditor('editor');
    editor.create();
    window.editor = editor;
});
