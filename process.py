
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

# 高级设置
year = '2022' # 年份
xueqi = '2022-2023-1' # 学期数
begin_week = 35 # 开学的当周，苹果日历中查看，打开设置中的周数
year_week = 52 # 今年总周数
Combine_Trigger = True # 连着几节的课程是否合并
class ProcessBar(object):
  def __init__(self, total):  # 初始化传入总数
    self.shape = ['▏', '▎', '▍', '▋', '▊', '▉']
    self.shape_num = len(self.shape)
    self.row_num = 30
    self.now = 0
    self.total = total
  def print_next(self, now=-1):   # 默认+1
    if now == -1:
      self.now += 1
    else:
      self.now = now

    rate = math.ceil((self.now / self.total) * (self.row_num * self.shape_num))
    head = rate // self.shape_num
    tail = rate % self.shape_num
    info = self.shape[-1] * head
    if tail != 0:
      info += self.shape[tail-1]
    full_info = '[%s%s] [%.2f%%]' % (info, (self.row_num-len(info)) * ' ', 100 * self.now / self.total)
    print("\r", end='', flush=True)
    print(full_info, end='', flush=True)
    if self.now == self.total:
      print('')

if platform.system().lower() == 'windows':
  os.system("cls")
else:
  os.system("clear")


print('这是一个从BUPT教务爬取课程表并转为苹果日历的脚本 BY LAWTED')
time.sleep(1)

print('---------------GIVE ME A STAR IF U LIKE!--------------')
print('Github: www.github.com/LAWTED')
print('Github: www.github.com/Lawted')
time.sleep(1)
print("------------------NOW LET'S BEGIN!!!------------------")
time.sleep(1)
BUPT_ID = input('请输入你的学号: ')
BUPT_PASS = input('请输入你的新教务密码: ')




# 别动
keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' # DO NOT CHANGE!!!


pb = ProcessBar(10000)


if not begin_week:
  print('---请设置开学当周在今年的第多少周,苹果日历中查看---')
  quit()
if not year_week:
  print('---请设置今年总周数---')
  quit()
if not BUPT_ID:
  print('---请填入你的学号---')
  quit()
if not BUPT_PASS:
  print('---请填入你的密码，本项目在源码公开，不存在泄露密码操作---')
  quit()
if not keyStr:
  print('---叫你别改那个---')
  quit()


if platform.system().lower() == 'windows':
  os.system("cls")
else:
  os.system("clear")
for i in range(1000):
  pb.print_next()

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

for i in range(1000,2000):
  pb.print_next()

session = requests.session()

for i in range(2000,3500):
  pb.print_next()

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
l5 = session.post('https://jwgl.bupt.edu.cn/jsxsd/xk/LoginToXk', data=payload, headers=headers)
for i in range(3500,4600):
  pb.print_next()


for i in range(4600,5500):
  pb.print_next()

# 第三次请求带上cookie
cookies1 = l1.cookies.items()
cookie = ''
for name, value in cookies1:
  cookie += '{0}={1}; '.format(name, value)
time.sleep(3)
headers = {
  "cookie": cookie
}
data = {'xnxq01id': xueqi, 'zc': '', 'kbjcmsid': '9475847A3F3033D1E05377B5030AA94D'}
url = 'https://jwgl.bupt.edu.cn/jsxsd/xskb/xskb_print.do?xnxq01id={}&zc=&kbjcmsid=9475847A3F3033D1E05377B5030AA94D'.format(xueqi)
p = requests.post(url, data=data, headers=headers)
if 'html' in p.text:
  print('\n------------------密码错误------------------')
  quit()
f=open('a.xls','wb')
f.write(p.content)

class lesson:
  name = ''
  week = ''
  place = ''
  section = ''
  time = ''

wb = xlrd.open_workbook("./a.xls")
ws = wb.sheet_by_index(0)
nrows = ws.nrows
ncols = ws.ncols
for i in range(5500,7000):
  pb.print_next()

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
# print(len(all_lesson))
# print(all_lesson)

# 写入头文件
for i in range(7000,8000):
  pb.print_next()

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
for i in range(8000,9900):
  pb.print_next()

def write_file(f, name, place, date, time_start, time_end):
  global res_txt
  f.write('BEGIN:VEVENT')
  f.write('\n')
  res_txt += 'BEGIN:VEVENT'
  res_txt += '\r\n'
  f.write('DTSTAMP:20201012T104622Z')
  f.write('\n')
  res_txt += 'DTSTAMP:20201012T104622Z'
  res_txt += '\r\n'
  f.write('UID:' + randomUID())
  f.write('\n')
  res_txt += 'UID:' + randomUID()
  res_txt += '\r\n'
  f.write('SUMMARY:{} {}'.format(name,place))
  f.write('\n')
  res_txt += 'SUMMARY:{} {}'.format(name,place)
  res_txt += '\r\n'
  f.write('DTSTART;TZID=Asia/Shanghai:{}T{}'.format(date, time_start))
  f.write('\n')
  res_txt += 'DTSTART;TZID=Asia/Shanghai:{}T{}'.format(date, time_start)
  res_txt += '\r\n'
  f.write('DTEND;TZID=Asia/Shanghai:{}T{}'.format(date, time_end))
  f.write('\n')
  res_txt += 'DTEND;TZID=Asia/Shanghai:{}T{}'.format(date, time_end)
  res_txt += '\r\n'
  f.write('BEGIN:VALARM')
  f.write('\n')
  res_txt += 'BEGIN:VALARM'
  res_txt += '\r\n'
  f.write('X-WR-ALARMUID:F03864BD-41F4-40EC-BF20-1E4E7930ED92')
  f.write('\n')
  res_txt += 'X-WR-ALARMUID:F03864BD-41F4-40EC-BF20-1E4E7930ED92'
  res_txt += '\r\n'
  f.write('UID:' + randomUID())
  f.write('\n')
  res_txt += 'UID:' + randomUID()
  res_txt += '\r\n'
  f.write('TRIGGER:-PT5M')
  f.write('\n')
  res_txt += 'TRIGGER:-PT5M'
  res_txt += '\r\n'
  f.write('ATTACH;VALUE=URI:Chord')
  f.write('\n')
  res_txt += 'ATTACH;VALUE=URI:Chord'
  res_txt += '\r\n'
  f.write('ACTION:AUDIO')
  f.write('\n')
  res_txt += 'ACTION:AUDIO'
  res_txt += '\r\n'
  f.write('END:VALARM')
  f.write('\n')
  res_txt += 'END:VALARM'
  res_txt += '\r\n'
  f.write('END:VEVENT')
  f.write('\n')
  res_txt += 'END:VEVENT'
  res_txt += '\r\n'
  # print(res_txt)

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
      write_file(f, name, place, date, time_start, time_end)
    else:
      week_item_begin = week_item.split('-')[0]
      week_item_end = week_item.split('-')[1]
      # print(week_item_begin, week_item_end)
      for week_iter in range(int(week_item_begin)+begin_week-1, int(week_item_end)+begin_week):
        d = year + '-W' + str(week_iter) + '-' + str(time_seven)
        r = datetime.datetime.strptime(d, "%Y-W%W-%w")
        date = r.strftime('%Y%m%d')
        # print(name, place, date, time_start, time_end)
        write_file(f, name, place, date, time_start, time_end)
      # date.append(a)
      # print(name,place,date,time_start,time_end)

f.write('END:VCALENDAR')
res_txt += 'END:VCALENDAR'
f.close()

os.remove("./a.xls")

import urllib.parse
for i in range(9900,10000):
  pb.print_next()

res_txt = urllib.parse.quote(res_txt, safe='~@#$&()*!+=:;,.?/\'')
#使用二进制格式保存转码后的文本
res_txt = 'data:text/calendar,' + res_txt
f=open('direct.txt','w',encoding='utf-8')
f.write(res_txt)
f.close()
print('--------------------DONE--------------------')
print('请查看README了解如何导入和使用')
