
import xlrd
import random
import string
import re
import datetime

# 常量
year = '2021' # 今年
begin_week = 36 # 开学的当周
year_week = 52 # 今年总周数

class lesson:
  name = ''
  week = ''
  place = ''
  section = ''
  time = ''

wb = xlrd.open_workbook("./a.xls")

# from openpyxl import load_workbook

# #打开一个workbook
# wb = load_workbook(filename="./a.xls")

#获取当前活跃的worksheet,默认就是第一个worksheet

ws = wb.sheet_by_index(0)
# print(ws)

# 有效行数
nrows = ws.nrows
ncols = ws.ncols
# print(nrows, ncols)
# for r in range(4,18):
#   return 0
# row_3 = ws.row_values(2)
# print(row_3)

# 获取时间表

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
# print(len(all_lesson))
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
  for week_item in week_all:
    if len(week_item) == 1:
      week_item_begin = week_item
      week_item_end = week_item
    else:
      week_item_begin = week_item.split('-')[0]
      week_item_end = week_item.split('-')[1]
    # print(week_item_begin, week_item_end)
    for week_iter in range(int(week_item_begin)+begin_week-2, int(week_item_end)+begin_week-1):
      d = year + '-W' + str(week_iter) + '-' + str(time_seven)
      r = datetime.datetime.strptime(d, "%Y-W%W-%w")
      date = r.strftime('%Y%m%d')
      # date.append(a)
      # print(name,place,date,time_start,time_end)
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
f.write('END:VCALENDAR')
res_txt += 'END:VCALENDAR'
f.close()
# print(res_txt)

import urllib.parse
# res_txt = quote(res_txt, 'GBK')

# res_txt = 'data:text/calendar,BEGIN:VCALENDARVERSION:2.0' + res_txt

# f=open('direct.txt','w',encoding='GBK')
# f.write(res_txt)
res_txt = urllib.parse.quote(res_txt, safe='~@#$&()*!+=:;,.?/\'');
#使用二进制格式保存转码后的文本
res_txt = 'data:text/calendar,' + res_txt
f=open('direct.txt','w',encoding='utf-8')
f.write(res_txt)
f.close()