# coding:utf8

import string
import random

def get_captcha(num):
    #num 获取验证码的数量
    sources = list(string.letters)
    [sources.append(str(x)) for x in xrange(0,10)]
    return ''.join(random.sample(sources,num))