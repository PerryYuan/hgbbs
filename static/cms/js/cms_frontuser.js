/**
 * Created by yuan on 2017/3/25.
 */

$(function () {
   $('.sort-select').change(function (event) {
       event.preventDefault();
       var v = $(this).val();
       var href = xtparam.setParam(window.location.href,'sort',v);
       window.location = href;
   });
});
