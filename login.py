# -*- coding:utf-8 -*-
import urllib.parse as parse
import urllib.request as req
# import urllib2 as req
# from urlparse import urlparse as parse, urlunparse as unparse
from oa.ntlm import HTTPNtlmAuthHandler
import oa.common as common
import ssl
import os
import oa.parseCode as pc

import requests
from requests_ntlm import HttpNtlmAuth

context = ssl._create_unverified_context()


def requests_auth():
    session = requests.Session()
    session.auth = HttpNtlmAuth(common.INDEX_URL + '\\' + common.USER_NAME, common.USER_PASS)
    # session.get(common.AUTH_URL)
    # pCookie = res.headers.get('Set-Cookie')
    # pCookie = pCookie[:pCookie.find(';')]
    # common.HEADER['Cookie'] = pCookie
    data = {'username': common.USER_NAME, 'password': common.USER_PASS, 'captcha': 123}
    reqDic = requests.Request('post', common.AUTH_URL, common.HEADER, None, data)
    prepare_request = session.prepare_request(reqDic)
    res = session.send(prepare_request, verify=False)
    print(res.content.decode('utf8'))


def urllib_auth():
    p = req.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, uri=common.INDEX_URL, user=(common.INDEX_URL + '\\' + common.USER_NAME),
                   passwd=common.USER_PASS)
    handler = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(p)
    opener = req.build_opener(handler)
    req.install_opener(opener)

    reqData = req.Request(common.INDEX_URL, None, common.HEADER)
    x = req.urlopen(reqData, context=context)
    # # print(x.read().decode('utf8'))
    # # print(x.info())
    pCookie = x.info().get('Set-Cookie')
    apCookie = pCookie[:pCookie.find(';')]

    # task url
    common.HEADER['Cookie'] = apCookie
    reqData = req.Request(common.TASK_URL, headers=common.HEADER)
    res = req.urlopen(reqData)
    pCookie = res.info().get('Set-Cookie')
    common.HEADER['Cookie'] = pCookie[:pCookie.find(';')]

    reqData = req.Request(common.AUTH_URL, headers=common.HEADER)
    res = req.urlopen(reqData)
    print(res.read().decode('utf8'))

    #
    # reqData = req.Request(common.CAPTCHA_URL, headers=common.HEADER)
    # res = req.urlopen(reqData, context=context)
    # filePath = os.path.join('../codeAuto/test', '1234.jpg')
    # with open(filePath, 'wb') as fp:
    #     fp.write(res.read())
    #
    # captchaData = ''.join(pc.captcha_data())
    # common.HEADER['Content-Type'] = 'application/x-www-form-urlencoded'
    # loginData = urllib.urlencode({'username': common.USER_NAME, 'password': common.USER_PASS, 'captcha': captchaData})
    # loginData = loginData.encode('utf8')
    # reqData = req.Request(common.AUTH_URL, loginData, common.HEADER)
    # res = req.urlopen(reqData, context=context)
    # print(res.read().decode('utf8'))


if __name__ == '__main__':
    urllib_auth()
