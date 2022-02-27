from django.http import HttpResponse
from django.shortcuts import render
import xlrd
import random
import string
import re
import datetime
import math
import requests
import time
import os
import math
import platform
# Create your views here.


def login(request):
  # 高级设置
  year = '2022' # 年份
  xueqi = '2021-2022-2' # 学期数
  begin_week = 9 # 开学的当周，苹果日历中查看，打开设置中的周数
  year_week = 52 # 今年总周数
  Combine_Trigger = True # 连着几节的课程是否合并
  BUPT_ID = request.GET.get('id', '')
  BUPT_PASS = request.GET.get('pw', '')
  keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' # DO NOT CHANGE!!!
  def encodeInp(input):
    output = ''
    chr1, chr2, chr3 = '', '', ''
    enc1, enc2, enc3 = '', '', ''
    i = 0
    while True:
      chr1 = ord(input[i])
      i += 1
      chr2 = ord(input[i]) if i < len(input) else 0
      i += 1
      chr3 = ord(input[i]) if i < len(input) else 0
      i += 1
      enc1 = chr1 >> 2
      enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
      enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
      enc4 = chr3 & 63
      # print(chr1, chr2, chr3)
      if chr2 == 0:
        enc3 = enc4 = 64
      elif chr3 == 0:
        enc4 = 64
      output = output + keyStr[enc1] + keyStr[enc2] + keyStr[enc3] + keyStr[enc4]
      chr1 = chr2 = chr3 = ''
      enc1 = enc2 = enc3 = enc4 = ''
      if i >= len(input):
        break
    return output


  encoded = encodeInp(BUPT_ID) + '%%%' + encodeInp(BUPT_PASS)

  session = requests.session()

  l1 = session.get('https://jwgl.bupt.edu.cn/jsxsd/')
  cookies1 = l1.cookies.items()
  cookie = ''
  for name, value in cookies1:
    cookie += '{0}={1}; '.format(name, value)

  # 第二次请求，发送cookie和密码
  # print(cookie)
  headers = {
      'Host': 'jwgl.bupt.edu.cn',
      'Referer': 'https://jwgl.bupt.edu.cn/jsxsd/xk/LoginToXk?method=exit&tktime=1631723647000',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
      "cookie": cookie
  }
  payload = {'userAccount': BUPT_ID, 'userPassWord': '', 'encoded': encoded}
  l5 = session.post('https://jwgl.bupt.edu.cn/jsxsd/xk/LoginToXk',
                    data=payload, headers=headers)

  # 第三次请求带上cookie
  cookies1 = l1.cookies.items()
  cookie = ''
  for name, value in cookies1:
    cookie += '{0}={1}; '.format(name, value)
  headers = {
      "cookie": cookie
  }
  data = {'xnxq01id': xueqi, 'zc': '',
          'kbjcmsid': '9475847A3F3033D1E05377B5030AA94D'}
  url = 'https://jwgl.bupt.edu.cn/jsxsd/xskb/xskb_print.do?xnxq01id={}&zc=&kbjcmsid=9475847A3F3033D1E05377B5030AA94D'.format(
      xueqi)
  p = requests.post(url, data=data, headers=headers)
  if 'html' in p.text:
    print('\n------------------密码错误------------------')
    quit()
  f = open('a.xls', 'wb')
  f.write(p.content)
  return HttpResponse('hello')
