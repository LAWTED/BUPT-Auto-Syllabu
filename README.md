# BUPT-Auto-Syllabu
#### ![](https://img.shields.io/badge/author-Lawted-lightpink) ![GitHub](https://img.shields.io/github/license/LAWTED/BUPT-Auto-Syllabu) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/LAWTED/BUPT-Auto-Syllabu) ![GitHub top language](https://img.shields.io/github/languages/top/LAWTED/BUPT-Auto-Syllabu?color=56ccf2) ![GitHub last commit](https://img.shields.io/github/last-commit/LAWTED/BUPT-Auto-Syllabu?color=yellow)

自动获取北邮课表导入苹果日历

## 环境配置

``` python
python 3.0
pip
```



## 使用方法

打开终端

```python
pip install -r requirements.txt
python process.py
# 然后按照提示操作
```

### 如果是`MacOS`的电脑

> 直接打开`apple_calendar.ics`便可以自动导入



### 如果是`Windos`的电脑

> 将`direct.txt `发送文件到手机(比如微信文件传输助手)， 再苹果手机中存储到文件，打开文件`direct.txt `复制所有内容，到`safari`浏览器中地址栏粘贴跳转，然后导入苹果日历



## 高级设置

打开`process.py`，找到头部的高级设置，可以设置详细信息

```python
# 高级设置
year = '2022' # 年份
xueqi = '2021-2022-2' # 学期数
begin_week = 9 # 开学的当周，苹果日历中查看，打开设置中的周数
year_week = 52 # 今年总周数
Combine_Trigger = True # 连着几节的课程是否合并
```

