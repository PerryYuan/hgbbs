/**
 * Created by yuan on 2017/3/25.
 */

$(function () {
    $('#add-board').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'text':'请输入板块名称',
            'confirmCallback':function (inputValue) {
                phajax.post({
                    'url':'/addboard/',
                    'data':{
                        'board_name':inputValue
                    },
                    'success':function (data) {
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('板块添加成功');
                            setInterval(function () {
                                window.location.reload();
                            },500);
                        }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
        }});

    });
});

$(function () {
   $('.edit-board').click(function (event) {
       event.preventDefault();
       var board_id = $(this).attr('data-board-id');
       xtalert.alertOneInput({
               'text':'请输入板块名称',
               'confirmCallback':function (inputValue) {
                    phajax.post({
                        'url':'/editboard/',
                        'data':{
                            'board_name':inputValue,
                            'board_id':board_id
                        },
                        'success':function (data) {
                            if(data['code'] == 200){
                                xtalert.alertSuccessToast('板块修改成功');
                                setInterval(function () {
                                    window.location.reload();
                                },500);
                            }else{
                                xtalert.alertInfoToast(data['message']);
                            }
                        }
                    });
        }});

   });
});

$(function () {
   $('.delete-board').click(function (event) {
       event.preventDefault();
       var board_id = $(this).attr('data-board-id');
       xtalert.alertConfirm({
               'msg':'你确认删除该板块吗？',
               'confirmCallback':function () {
                    phajax.post({
                        'url':'/deleteboard/',
                        'data':{
                            'board_id':board_id
                        },
                        'success':function (data) {
                            if(data['code'] == 200){
                                xtalert.alertSuccessToast('板块删除成功');
                                setInterval(function () {
                                    window.location.reload();
                                },500);
                            }else{
                                setTimeout(function(){
                                    xtalert.alertInfoToast(data['message']);
                                },500);
                            }
                        }
                    });
        }});

   });
});

