/**
 * Created by yuan on 2017/3/24.
 */
$(function () {
   $('#flush-captcha').click(function (event) {
       event.preventDefault();
       var img = $(this).children('img');
       var href = xtparam.setParam(img.attr('src'),'xx',Math.random());
       img.attr('src',href);
   });
});
