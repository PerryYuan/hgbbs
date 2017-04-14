/**
 * Created by yuan on 2017/3/5.
 */

$(function () {
    phajax = {
         'ajax':function (args) {
             if(!args['error']){
                 args['error'] = function (error) {
                    xtalert.alertNetworkError();
                 }
             }
            this.ajaxSetup();
            $.ajax(args);
        },
        'get':function (args) {
            args['type'] = 'get';
            this.ajax(args);
        },
        'post':function (args) {
            args['type'] = 'post';
            this.ajax(args);
        },
        'ajaxSetup':function () {
            $.ajaxSetup({
                'beforeSend':function(xhr,settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        var csrftoken = $('meta[name=csrf-token]').attr('content');
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                    }
                }
            });
        }
    }
});
