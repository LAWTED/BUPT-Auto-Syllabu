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
  f=open('a.xls','wb')
  f.write(p.content)
  class lesson:
    name = ''
    week = ''
    place = ''
    section = ''
    time = ''

  wb = xlrd.open_workbook("./a.xls")
  os.remove("./a.xls")
  ws = wb.sheet_by_index(0)
  nrows = ws.nrows
  ncols = ws.ncols


  col_values = ws.col_values(colx=0)
  realtime_list = col_values[3:17]
  realtime_list = [time.split('\n')[1] for time in realtime_list]
  all_lesson = []
  # list(realtime_list)
  # print(realtime_list)
  for col in range(1,6):
    for row in range(3,17):
      cell_info = ws.cell_value(rowx=row, colx=col)
      if cell_info != ' ' and 0<row<17:
        cells_list = []
        cells = cell_info.splitlines()[1:]
        # 体育课有六项
        if len(cells) == 6:
          cells = cells[1:]
          # 去掉括号
          cells[0] = cells[0][1:-1]
        # 两种课程写一起了
        if len(cells) > 5:
          cells1 = cells[5:]
          cells2 = cells[:5]
          cells_list.append(cells1)
          cells_list.append(cells2)
        else:
          cells_list.append(cells)
        for c in cells_list:
          lec1 =lesson()
          lec1.name = c[0]
          lec1.week = c[-3]
          lec1.place = c[-2]
          lec1.section = c[-1]
          lec1.time = realtime_list[row-3] + '+' +str(col)
          all_lesson.append(lec1.__dict__)
          # print(lec1.__dict__)
      if Combine_Trigger and cell_info != ' ' and 3 < row and cell_info == ws.cell_value(rowx=row-1, colx=col):
        all_lesson.pop()
        tmplesson = all_lesson.pop()
        tmplesson['time'] = tmplesson['time'].split('-')[0] + '-' +realtime_list[row-3].split('-')[1] + '+' + str(col)
        all_lesson.append(tmplesson)
  # print(all_lesson)
  # 写入头文件
  f=open('apple_calendar.ics','w',encoding='utf-8')
  head=['BEGIN:VCALENDAR',
  'VERSION:2.0',
  ]
  for i in head:
    f.write(i)
    f.write('\n')
  def randomUID():
    return ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 15))

  res_txt = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\n'

  def write_file(res_txt, name, place, date, time_start, time_end):
    res_txt += 'BEGIN:VEVENT'
    res_txt += '\r\n'
    res_txt += 'DTSTAMP:20201012T104622Z'
    res_txt += '\r\n'
    res_txt += 'UID:' + randomUID()
    res_txt += '\r\n'
    res_txt += 'SUMMARY:{} {}'.format(name,place)
    res_txt += '\r\n'
    res_txt += 'DTSTART;TZID=Asia/Shanghai:{}T{}'.format(date, time_start)
    res_txt += '\r\n'
    res_txt += 'DTEND;TZID=Asia/Shanghai:{}T{}'.format(date, time_end)
    res_txt += '\r\n'
    res_txt += 'BEGIN:VALARM'
    res_txt += '\r\n'
    res_txt += 'X-WR-ALARMUID:F03864BD-41F4-40EC-BF20-1E4E7930ED92'
    res_txt += '\r\n'
    res_txt += 'UID:' + randomUID()
    res_txt += '\r\n'
    res_txt += 'TRIGGER:-PT5M'
    res_txt += '\r\n'
    res_txt += 'ATTACH;VALUE=URI:Chord'
    res_txt += '\r\n'
    res_txt += 'ACTION:AUDIO'
    res_txt += '\r\n'
    res_txt += 'END:VALARM'
    res_txt += '\r\n'
    res_txt += 'END:VEVENT'
    res_txt += '\r\n'

  for l in all_lesson:
    # print(l['name'])
    name = l['name']
    week = l['week']
    week_all = week[:-3].split(',')
    place = l['place']
    time = l['time']
    time_all = time.split('+')[0]
    time_start = ''.join(time_all.split('-')[0].split(':')) + '00'
    time_end = ''.join(time_all.split('-')[1].split(':')) + '00'
    time_seven = time.split('+')[1]
    date = []
    # print(week_all)
    for week_item in week_all:
      # if len(week_item) == 1:
      #   print(week_item)
      #   week_item_begin = week_item
      #   week_item_end = week_item
      if not '-' in week_item:
        d = year + '-W' + str(int(week_item)+begin_week-1) + '-' + str(time_seven)
        r = datetime.datetime.strptime(d, "%Y-W%W-%w")
        date = r.strftime('%Y%m%d')
        # print(name, place, date, time_start, time_end)
        write_file(res_txt, name, place, date, time_start, time_end)
      else:
        week_item_begin = week_item.split('-')[0]
        week_item_end = week_item.split('-')[1]
        # print(week_item_begin, week_item_end)
        for week_iter in range(int(week_item_begin)+begin_week-1, int(week_item_end)+begin_week-1):
          d = year + '-W' + str(week_iter) + '-' + str(time_seven)
          r = datetime.datetime.strptime(d, "%Y-W%W-%w")
          date = r.strftime('%Y%m%d')
          # print(name, place, date, time_start, time_end)
          write_file(res_txt, name, place, date, time_start, time_end)
        # date.append(a)
        # print(name,place,date,time_start,time_end)

    res_txt += 'END:VCALENDAR'

    import urllib.parse


    res_txt = urllib.parse.quote(res_txt, safe='~@#$&()*!+=:;,.?/\'')
    #使用二进制格式保存转码后的文本
    res_txt = 'data:text/calendar,' + res_txt
  return HttpResponse(res_txt)
