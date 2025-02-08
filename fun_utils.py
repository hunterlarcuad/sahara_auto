"""
utils
"""
import os
import sys
import json
import requests
from datetime import datetime
from dateutil import tz
from datetime import timezone
from datetime import timedelta
import socket
import time
import re

DEF_URL_DINGTALK = "https://oapi.dingtalk.com/robot/send"
access_token = "0313ed7471f2910596c1d91cef6569c132"  # noqa


def conv_time(ts, style=1):
    """
    ts: second
    style:
        1: 2022-10-20
        2: 2022-10-20T20:51:11+0800
        3: 2022-10-20 00:00:00
        4: 20:51
        5: 2022-10-20 20:51:11
    """
    to_zone = tz.gettz('Asia/Shanghai')
    if style == 1:
        t_format = "%Y-%m-%d"
    elif style == 2:
        t_format = "%Y-%m-%dT%H:%M:%S+0800"
    elif style == 3:
        t_format = "%Y-%m-%d 00:00:00"
    elif style == 4:
        t_format = "%H:%M"
    elif style == 5:
        t_format = "%Y-%m-%d %H:%M:%S"
    else:
        print("conv_time parameter is error.")
        sys.exit(1)
    dt = datetime.utcfromtimestamp(ts)
    # local = dt.astimezone(to_zone)
    local = dt.replace(tzinfo=timezone.utc).astimezone(to_zone)
    s_date = local.strftime(t_format)
    return s_date


def format_ts(ts, style=1, tz_offset=0):
    """
    ts: second
    style:
        1: 2022-10-20
        2: 2022-10-20T20:51:11+0800
        3: 2022-10-20 00:00:00
        4: 20:51
        5: 2022-10-20 20:51:11
    tz_offset:
        timezone offset in hours from UTC
        e.g., 0 for UTC, 8 for Asia/Shanghai
    """
    if style == 1:
        t_format = "%Y-%m-%d"
    elif style == 2:
        t_format = "%Y-%m-%dT%H:%M:%S"
    elif style == 3:
        t_format = "%Y-%m-%d 00:00:00"
    elif style == 4:
        t_format = "%H:%M"
    elif style == 5:
        t_format = "%Y-%m-%d %H:%M:%S"
    else:
        print("conv_time parameter is error.")
        sys.exit(1)
    # Convert timestamp to datetime object in UTC
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)

    # Calculate the target timezone
    to_zone = timezone(timedelta(hours=tz_offset))

    # Convert to target timezone
    local = dt.astimezone(to_zone)

    # Format the datetime object to the specified style
    s_date = local.strftime(t_format)

    # Append the timezone offset to the formatted string if style is 2
    if style == 2:
        s_date += f"{tz_offset:+03d}00"

    return s_date


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def ding_msg(content, access_token, msgtype="markdown"):
    lst_phone = []

    s_ip = get_host_ip()
    if "markdown" == msgtype:
        content["text"] += (
            "\n###### Update:{time}"
            "\n###### From:{ip}".format
            (
                time=conv_time(time.time(), 5),
                ip=s_ip
            )
        )
    else:
        content += (
            "\nUpdate:{time}"
            "\nFrom:{ip}".format
            (
                time=conv_time(time.time(), 5),
                ip=s_ip
            )
        )
    data = {
        "msgtype": msgtype,
        msgtype: content,
        "at": {
            "atMobiles": lst_phone,
            "isAtAll": False
        }
    }
    data = json.dumps(data)
    print(data)

    headers = {"Content-Type": "application/json; charset=utf-8"}
    resp = requests.post(
        url="{0}?access_token={1}".format(DEF_URL_DINGTALK, access_token),
        data=data,
        headers=headers,
        timeout=3
    )

    print(resp.content)


def ts_human(n_sec):
    s_ret = ""
    n_hour = 0
    n_min = 0
    n_sec = int(n_sec)
    if n_sec >= 3600:
        n_hour = int(n_sec / 3600)
        n_sec = n_sec % 3600
    if n_sec >= 60:
        n_min = int(n_sec / 60)
        n_sec = int(n_sec % 60)

    if n_hour:
        s_ret += "{}h".format(n_hour)
    if n_min:
        s_ret += "{}m".format(n_min)
    if n_sec:
        s_ret += "{}s".format(n_sec)

    return s_ret


def get_date(is_utc=True):
    # 获取当前 UTC 时间的日期
    now = datetime.utcnow()

    # 格式化为 yyyymmdd
    s_date = now.strftime('%Y%m%d')

    return s_date


def load_file(file_in, idx_key=0, header=''):
    """
    Return:
        dict(key, list)
    跳过以 # 开头的行
    """
    d_ret = {}
    try:
        with open(file_in, 'r') as fp:
            # Skip the header line
            next(fp)
            for line in fp:
                if len(line.strip()) == 0:
                    continue
                if line.startswith('#'):
                    continue
                # 逗号分隔，字段中不能包含逗号
                fields = line.strip().split(',')
                s_key = fields[idx_key]
                d_ret[s_key] = fields
    except StopIteration:
        # print("File is empty.")
        pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'[load_file] An error occurred: {str(e)}')

    return d_ret


def save2file(file_ot, dic_status, idx_key=0, header=''):
    """
    header: 表头
    dic_status: 输出的字段列表
    idx_key: dic_status value 的主键下标
    """
    b_ret = True
    s_msg = ''

    dir_file_out = os.path.dirname(file_ot)
    if dir_file_out and (not os.path.exists(dir_file_out)):
        os.makedirs(dir_file_out)

    if not os.path.exists(file_ot):
        with open(file_ot, 'w') as fp:
            fp.write(f'{header}\n')

    try:
        # 先读取原有内容，合并至 dic_status
        if os.path.exists(file_ot):
            with open(file_ot, 'r') as fp:
                lines = fp.readlines()
                for line in lines[1:]:  # 跳过表头
                    fields = line.strip().split(',')
                    if len(fields) == 0:
                        continue
                    s_key = fields[idx_key]
                    if s_key in dic_status:
                        continue
                    dic_status[s_key] = fields

        lst_sorted = sorted(dic_status.keys())
        with open(file_ot, 'w') as fp:
            fp.write(f'{header}\n')
            for s_key in lst_sorted:
                s_out = ','.join(str(item) for item in dic_status[s_key])
                fp.write(f'{s_out}\n')
    except Exception as e:
        b_ret = False
        s_msg = f'[save2file] An error occurred: {str(e)}'

    return (b_ret, s_msg)


def time_difference(input_time_str):
    # 将传入的时间字符串转换为datetime对象
    input_time = datetime.strptime(input_time_str, "%Y-%m-%dT%H:%M:%S%z")

    # 获取当前时间，并设置为UTC时区
    current_time_utc = datetime.now(timezone.utc)

    # 将当前时间转换为传入时间的时区
    current_time = current_time_utc.astimezone(input_time.tzinfo)

    # 计算时间差并转换为秒
    time_diff_seconds = (input_time - current_time).total_seconds()

    time_diff_seconds = int(time_diff_seconds)

    return time_diff_seconds

def extract_numbers(s):
    # 使用正则表达式找到所有的数字
    numbers = re.findall(r'\d+', s)
    # 将找到的数字字符串转换为整数
    return [int(num) for num in numbers]


if __name__ == "__main__":
    """
    """

    input_time_str = "2024-09-09T18:21:22+0800"
    n_sec = time_difference(input_time_str)
    print(n_sec)
    sys.exit(-1)

    file_test = 'ttt.csv'
    dic_status = load_file(file_test, idx_key=0, header='')
    dic_status['p005'] = ['p005', 'DONE', 10, 5, -1]
    save2file(file_test, dic_status, idx_key=0, header='header')
    sys.exit(-1)

    s_token = 'ff930a850a7feebb7db0ea1f0e5b3032f175dab'  # noqa
    d_cont = {
        'title': 'my title',
        'text': (
            '- first line\n'
            '- second line\n'
        )
    }
    ding_msg(d_cont, s_token, msgtype="markdown")
