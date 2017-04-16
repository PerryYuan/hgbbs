# coding:utf8
import top.api

import constants


def send_sms(captcha,telephone):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest(constants.ALIDAYU_URL, 80)
    req.set_app_info(top.appinfo(constants.ALIDAYU_APP_KEY, constants.ALIDAYU_APP_SECRET))
    req.extend = "123456"
    req.sms_type = "normal"
    req.sms_free_sign_name = constants.ALIDAYU_SIGN_NAME
    telephone = "{}".format(telephone)
    req.sms_param = "{\"code\":\"%s\",\"username\":\"%s\"}" % (captcha, telephone)
    req.rec_num = telephone
    req.sms_template_code = constants.ALIDAYU_TEMPLATE_CODE
    return req