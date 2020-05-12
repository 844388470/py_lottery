from urllib import request

from bs4 import BeautifulSoup as bf
from io import BytesIO
import gzip

import sys
import random
import time
import datetime
import json

file_name = 'history.txt'

class Money():
  def __init__(self):
    self.ssq_list = self.get_ssq_history()
    self.dlt_list = self.get_dlt_history()
    self.buy_obj = self.get_buy_history()

  def get_ssq_history(self):
    headers={  'User-Agent':self.set_user_agent(),
      'Referer':'http://datachart.500.com/ssq/',
      'Content-Type':'application/x-www-form-urlencoded'
    }
    html = request.Request('http://datachart.500.com/ssq/history/history.shtml', headers=headers)
    response = request.urlopen(html)
    res = response.read()
    if response.info()['Content-Encoding'] == 'gzip':
        buff = BytesIO(res)
        f = gzip.GzipFile(fileobj=buff)
        soup = f.read()
        soup = bf(soup,'html.parser')
    else:
        soup = bf(res,'html.parser')
    lists = []
    for i, child in enumerate(soup.find(attrs={'id': 'tdata'}).children):
      if child != '\n' and child != ' ':
        lists.append({
          "No": child.contents[1].string,
          "red": str(int(child.contents[2].string))+'-'+str(int(child.contents[3].string))+'-'+str(int(child.contents[4].string))+'-'+str(int(child.contents[5].string))+'-'+str(int(child.contents[6].string))+'-'+str(int(child.contents[7].string)),
          "blue": str(int(child.contents[8].string)),
          "time": child.contents[-1].string
        })
    return lists

  def get_dlt_history(self):
    headers={  'User-Agent':self.set_user_agent(),
      'Referer':'http://datachart.500.com/dlt/',
      'Content-Type':'application/x-www-form-urlencoded'
    }
    html = request.Request('http://datachart.500.com/dlt/history/history.shtml', headers=headers)
    response = request.urlopen(html)
    res = response.read()
    if response.info()['Content-Encoding'] == 'gzip':
        buff = BytesIO(res)
        f = gzip.GzipFile(fileobj=buff)
        soup = f.read()
        soup = bf(soup,'html.parser')
    else:
        soup = bf(res,'html.parser')
    
    
    lists = []
    for i, child in enumerate(soup.find(attrs={'id': 'tdata'}).children):
      if child != '\n' and child != ' ':
        lists.append({
          "No": child.contents[1].string,
          "red": str(int(child.contents[2].string))+'-'+str(int(child.contents[3].string))+'-'+str(int(child.contents[4].string))+'-'+str(int(child.contents[5].string))+'-'+str(int(child.contents[6].string)),
          "blue": str(int(child.contents[7].string))+'-'+str(int(child.contents[8].string)),
          "time": child.contents[-1].string
        })
    return lists

  def set_user_agent(self):
      USER_AGENTS = [
          "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
          "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
          "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
          "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
          "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
          "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
          "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
          "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
      ]
      user_agent = random.choice(USER_AGENTS)
      return user_agent

  def get_buy_history(self):
    txt = []
    while True:
      try:
        with open(file_name, "r") as f:
          dataall = f.read()
          f.close()
        with open(file_name, "r") as f:
          data = f.readlines()
          f.close()
        for line in data:
          txt.append(line.strip('\n'))
        break
      except:
        set_buy_history('')
    return {
      'all':dataall,
      'value':txt
    }

  def set_buy_history(self,new):
    text = new
    if self.buy_obj['all'] != '':
      text = text + '\n' + self.buy_obj['all']
    with open(file_name, 'w') as file_object:
      file_object.write(text)

  def clear_buy_history(self):
    with open(file_name, 'w') as file_object:
      file_object.write('')
    self.buy_obj = self.get_buy_history()

  def shake_ssq_ball(self):
      ball_r = set()
      ball_b = str(random.choice(range(16)) + 1)
      while len(ball_r) < 6:
        ball_r.add(random.choice(range(33)) + 1)
      ball_r = list(ball_r)
      ball_r.sort()

      writes = {
        # "No": int(self.ssq_list[0]['No']) - 1,
        "No": int(self.ssq_list[0]['No']) + 1,
        "red": "-".join(str(i) for i in ball_r),
        "blue": ball_b,
        "type": 'ssq'
      }

      return json.dumps(writes)

  def shake_dlt_ball(self):
      ball_r = set()
      ball_b = set()
      while len(ball_r) < 5:
        ball_r.add(random.choice(range(35)) + 1)

      while len(ball_b) < 2:
        ball_b.add(random.choice(range(12)) + 1)
      ball_r = list(ball_r)
      ball_r.sort()
      ball_b = list(ball_b)
      ball_b.sort()

      writes = {
        # "No": int(self.dlt_list[0]['No']),
        "No": int(self.dlt_list[0]['No']) + 1,
        "red": "-".join(str(i) for i in ball_r),
        "blue": "-".join(str(i) for i in ball_b),
        "type": 'dlt'
      }
      return json.dumps(writes)

  def get_result(self):
      buy_list = self.buy_obj['value']
      win = []
      for i,items in enumerate(buy_list):
        item = json.loads(items)
        ball_r = item['red'].split('-')
        ball_b = item['blue']
        if item['type'] == 'ssq':
          for y in self.ssq_list:
            if y['No'] == str(item['No']):
              ball_r_win = y['red'].split('-')
              result_r = set(ball_r) & set(ball_r_win)
              result_b = set([ball_b]) & set([y['blue']])
              result_r_num = len(result_r)
              result_b_num = len(result_b)
              level = 0
              if result_r_num == 6 and result_b_num == 1:
                level = 1
                win.append(str(i + 1) + ':' + str(level) + '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
              elif result_r_num == 6:
                level = 2
                win.append(str(i + 1) + ':' + str(level) + '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
              elif result_r_num == 5 and result_b_num == 1:
                level = 3
                win.append(str(i + 1) + ':' + str(level) + '99999999999999999999')
              elif result_r_num == 5 or (result_r_num == 4 and result_b_num == 1):
                level = 4
                win.append(str(i + 1) + ':' + str(level) + '+6666666666')
              elif result_r_num == 4 or (result_r_num == 3 and result_b_num == 1):
                level = 5
                win.append(str(level) + '+')
              elif result_b_num == 1:
                level = 6
                win.append(str(level))
              break
        elif item['type'] == 'dlt':
          for y in self.dlt_list:
            if y['No'] == str(item['No']):
              ball_r_win = y['red'].split('-')
              ball_b_win = y['blue'].split('-')
              result_r = set(ball_r) & set(ball_r_win)
              result_b = set(ball_b.split('-')) & set(ball_b_win)
              result_r_num = len(result_r)
              result_b_num = len(result_b)
              level = 0
              if result_r_num == 5 and result_b_num == 2:
                level = 1
              elif result_r_num == 5 and result_b_num == 1:
                level = 2
              elif result_r_num == 5:
                level = 3
              elif result_r_num == 4 and result_b_num == 2:
                level = 4
              elif result_r_num == 4 and result_b_num == 1:
                level = 5
              elif result_r_num == 3 and result_b_num == 2:
                level = 6
              elif result_r_num == 4:
                level = 7
              elif (result_r_num == 3 and result_b_num == 1) or (result_r_num == 2 and result_b_num == 2):
                level = 8
              elif result_r_num == 3 or result_b_num == 2 or (result_r_num == 2 and result_b_num == 1):
                level = 9
              if level > 0:
                win.append('第'+ str(i + 1) + '个中了' + str(level) + '等奖')
              break
      print(win)

  def get_ball(self, type, num):
      main = ''
      if type == 'ssq':
        for i in range(num):
          main = main + self.shake_ssq_ball()
          if i != num - 1:
            main = main + '\n'
      elif type == 'dlt':
        for i in range(num):
          main = main + self.shake_dlt_ball()
          if i != num - 1:
            main = main + '\n'
      self.set_buy_history(main)
      self.buy_obj = self.get_buy_history()

  def testTime(self):
    i = 0; 
    r = ['10','14','24','25','33']
    b = ['11']

    while i < 1000000:
      print(i)
      ball_r = [str(random.choice(range(33)) + 1),str(random.choice(range(33)) + 1),str(random.choice(range(33)) + 1),str(random.choice(range(33)) + 1),str(random.choice(range(33)) + 1),str(random.choice(range(33)) + 1)]
      ball_b = str(random.choice(range(16)) + 1)
      result_r = set(r) & set(ball_r)
      result_b = set(b) & set(ball_b)
      if len(result_r) == 6 and len(result_b) == 1:
        break
      else:
        i = i + 1


# 启动
if __name__ == '__main__':
    # for i in range(100) :
    #   get_double_color_ball()
    # money.testTime()
    # money.clear_buy_history()
    # money.get_ball('ssq', 100)
    money = Money()
    # money.get_ball('dlt', 1)
    money.get_result()

