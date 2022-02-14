import uuid
import time
import re


def get_order_id():
    # 根据当前时间 网卡等信息产生的随机字符串 去掉分隔符
    uid = str(uuid.uuid4()).replace('-', '')
    # 正则取数字
    uid = re.sub(r'[^0-9]', '', uid)
    # 取前8位
    uid = uid[0:8]
    formatted_today = time.strftime('%y%m%d%H%M%S')
    order_id = 'EE'+formatted_today+uid
    return order_id


if __name__ == '__main__':
    id = get_order_id()
    print(id)
