#/usr/bin/env python3
#encoding:utf-8


__author__ = 'Ryan'

'''
 爬取12306的火车票信息，单线程
 不入库，热点城市班次多的时候，比较卡，仅做参考吧，可以使用Climb_NumPriceOfTrain_Multithreading.py多线程来获取
'''


import requests
import json
import redis
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 通用获取response的html.parse文本
def get_response(url, params=None):
    response = requests.get(url, params=params, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser').get_text()
    return soup

# 地区缩写对照存入redis
def save_to_redis():
    # 取得地区与地区缩写对照表
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    info = get_response(url)
    info2 = info[20:-2]
    temp_list = info2.split('|')
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 连接
    r.flushall()
    for i in range(0, len(temp_list) - 1, 5):
        local_name = temp_list[i + 1]
        short_name = temp_list[i + 2]
        r.set(local_name, short_name)  # 添加
        r.set(short_name, local_name)

# 传入地区获取缩写
def get_short_naem(name):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 连接
    short_name = r.get(name)
    return short_name

# 查询票价，存入redis
def check_ticket_price(train_num, train_no, from_station_no, to_station_no, seat_types, train_date):
    year = train_date[0:4]
    month = train_date[4:6]
    day = train_date[6:8]
    train_date = year + '-' + month + '-' + day
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'
    params = {'train_no': train_no,
              'from_station_no': from_station_no,
              'to_station_no': to_station_no,
              'seat_types': seat_types,
              'train_date': train_date
              }
    soup = get_response(url, params)
    info = json.loads(soup)
    price_list = info['data']
    tdz_price = price_list.get('A9', '--')  # 商务座价格
    ydz_price = price_list.get('M', '--')  # 一等座价格
    edz_price = price_list.get('O', '--')  # 二等座价格
    gjrw_price = price_list.get('A6', '--')  # 高级软卧价格
    rw_price = price_list.get('A5', '--')  # 软卧价格
    dw_price = price_list.get('A4', '--')  # 动卧价格
    yw_price = price_list.get('A3', '--')  # 硬卧价格
    rz_price = price_list.get('A2', '--')  # 软座价格
    yz_price = price_list.get('A1', '--')  # 硬座价格
    wz_price = price_list.get('WZ', '--')  # 无座价格
    qt_price = price_list.get('OT', '--')  # 其他价格
    ticket_price_list = []
    ticket_price_list.append(tdz_price)
    ticket_price_list.append(ydz_price)
    ticket_price_list.append(edz_price)
    ticket_price_list.append(gjrw_price)
    ticket_price_list.append(rw_price)
    ticket_price_list.append(dw_price)
    ticket_price_list.append(yw_price)
    ticket_price_list.append(rz_price)
    ticket_price_list.append(yz_price)
    ticket_price_list.append(wz_price)
    ticket_price_list.append(qt_price)
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 连接
    key_name = str(train_num)+'_price_list'
    r.set(key_name, ticket_price_list)

# 检查班次
def check_ticket_nums(from_station, to_station, time=None):
    thread = []
    if time == None:
        time = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    from_station_shortname = get_short_naem(from_station)
    to_station_shortname = get_short_naem(to_station)
    url = 'https://kyfw.12306.cn/otn/leftTicket/query'
    params = {
        'leftTicketDTO.train_date': time,  # 乘车时间
        'leftTicketDTO.from_station': from_station_shortname,  # 出发点
        'leftTicketDTO.to_station': to_station_shortname,  # 目的地
        'purpose_codes': 'ADULT'  # 票种
    }
    soup = get_response(url, params)
    print soup
    list = json.loads(soup)
    local_map = list['data']['map']
    ticket_info_list = list['data']['result']
    train_num_list = []
    for i in ticket_info_list:
        y = i.split('|')
        is_reserve = y[1]  # 是否可预定
        if is_reserve == '预订':
            train_num = y[3]  # 车次
            train_num_list.append(train_num)
            train_start_local = y[4]  # 列车起点
            train_end_local = y[5]  # 列车终点
            start_local = y[6]  # 上车点
            end_local = y[7]  # 到达点
            start_time = y[8]  # 出发时间
            end_time = y[9]  # 到达时间
            need_time = y[10]  # 历时
            tdz_tickets = y[-4] or '--'  # 商务座特等座 1
            ydz_tickets = y[-5] or '--'  # 一等 1
            edz_tickets = y[-6] or '--'  # 二等 1
            gjrw_tickets = y[-15] or '--'  # 高级软卧 1
            rw_tickets = y[-13] or '--'  # 软卧 1
            dw_tickets = y[-3] or '--'  # 动卧
            yw_tickets = y[-8] or '--'  # 硬卧 1
            rz_tickets = y[-12] or '--'  # 软座 1
            yz_tickets = y[-7] or '--'  # 硬座 1
            wz_tickets = y[-10] or '--'  # 无座 1
            # qt_tickets = y[-14] or '--'  # 其他 1
            train_no = y[2]  # 车次编码，查询票价用
            from_station_no = y[16]  # 出发地编号，查询票价用
            to_station_no = y[17]  # 目的地编号，查询票价用
            seat_types = y[-1]  # 椅子类型，查询票价用
            train_date = y[13]  # 出发时间，查询票价用
            start_local_chinses_name = local_map[start_local]  # 上车站点中文名
            end_local_chinses_name = local_map[end_local]  # 下车站点中文名
            train_start_chinses_name = get_short_naem(train_start_local).decode('utf-8')  # 列车起点中文名
            train_end_chinses_name = get_short_naem(train_end_local).decode('utf-8')  # 列车终点中文名
            train_info_list = [train_num, train_start_local, train_end_local, start_time, end_time, need_time,
                               tdz_tickets, ydz_tickets, edz_tickets, gjrw_tickets, rw_tickets, dw_tickets, yw_tickets,
                               rz_tickets, yz_tickets, wz_tickets, train_start_chinses_name, train_end_chinses_name,
                               start_local_chinses_name, end_local_chinses_name]
            r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 连接
            key_name = str(train_num) + '_other_list'
            r.set(key_name, train_info_list)
            r.set('train_num_list', train_num_list)
            #check_ticket_price(train_num, train_no, from_station_no, to_station_no, seat_types, train_date)
            name = threading.Thread(target=check_ticket_price, args=(train_num, train_no, from_station_no, to_station_no, seat_types, train_date))
            thread.append(name)
    return thread

def write_to_html(time, from_station, to_station):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # 连接
    # temp_list = str(r.get('train_num_list'))
    train_num_list = list(eval(r.get('train_num_list')))
    head_view1 = """
       <!DOCTYPE html>
       <html lang="en">
       <head>
         <head>
           <meta charset="utf-8">
           <title>列车运行</title>
           <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
           <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
           <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
           <style>
                 td {text-align: center}
                 th {text-align: center}
             </style>
       </head>
       <body>
       <div class="container">
         <div class="col-md-6 col-lg-12 col-sm-8">
         <table class="table table-striped table-bordered table-hover table-condensed table-responsive">
        """
    head_view2 = '<caption class="text-muted">' + time + from_station + ' 到 ' + to_station + '的列车运行表</caption>'
    head_view3 = """ <thead>
           <tr>
               <th>车次</th>
               <th>上车点/下车点</th>
               <th>发车时间/到达时间</th>
               <th>耗时</th>
               <th>列车起点/列车终点</th>
               <th>特等座</th>
               <th>一等座</th>
               <th>二等座</th>
               <th>高级软卧</th>
               <th>软卧</th>
               <th>动卧</th>
               <th>硬卧</th>
               <th>软座</th>
               <th>硬座</th>
               <th>无座</th>
              </tr></thead><tbody>
           """
    head_view = head_view1 + head_view2 + head_view3
    under_view = """  </tbody>
       </table>
             </div>
           </div>
       </body>
       </html>"""
    with open('climb_ticket_price.html', 'wb') as fp:
        fp.write(head_view.encode('utf-8').strip())
        for train_num in train_num_list:
            key_name1 = str(train_num) + '_price_list'
            key_name2 = str(train_num) + '_other_list'
            try:
                temp1 = list(eval(r.get(key_name1)))
            except:
                print(key_name1, r.get(key_name1))
            temp2 = list(eval(r.get(key_name2)))
            train_price_list = [str(i) for i in temp1]
            train_other_list = [str(x) for x in temp2]
            table_view = '<tr><td>' + train_num + '</td><td>' + train_other_list[-2] + '/' + train_other_list[-1] + '</td>' \
                    '<td>' + train_other_list[3] + '/' + train_other_list[4] + '</td><td>' + train_other_list[5] + '</td><td>' \
                         + train_other_list[-4] + '|' + train_other_list[-3] + '</td><td>' + train_other_list[6] + '|' + train_price_list[0] + \
                     '</td><td>' + train_other_list[7] + '|' + train_price_list[1] + '</td><td>' + train_other_list[8] + '|' + train_price_list[2] + \
                     '</td><td>' + train_other_list[9] + '|' + train_price_list[3] + '</td><td>' + train_other_list[10] + '|' + \
                         train_price_list[4] + '</td><td>' + train_other_list[11] + '|' + train_price_list[5] + '</td><td>' + \
                         train_other_list[12] + '|' + train_price_list[6] + '</td><td>' + train_other_list[13] + '|' + train_price_list[7] + \
                     '</td><td>' + train_other_list[14] + '|' + train_price_list[8] + '</td><td>' + train_other_list[15] + '|' + \
                         train_price_list[9] + '</tr>'
            fp.write(table_view.encode('utf-8').strip())
        fp.write(under_view.encode('utf-8').strip())
    fp.close()

if __name__ == "__main__":
    from_station = '南京'
    to_station = '太和北'
    time = '2018-06-16'
    save_to_redis()
    threadlist = check_ticket_nums(from_station, to_station, time)
    for t in threadlist:
        t.setDaemon(True)
        t.start()
    t.join()
    write_to_html(time, from_station, to_station)
    print('all over.')