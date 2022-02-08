# author z at 20220206
from django.conf import settings
import requests
from xml.dom.minidom import parse
import xml.dom.minidom

# 发送API
"""
http://sms.hutonginfo.com:9000/sms.aspx?action=send&userid=43&account=15638965253&password=25251425\
&mobile=15638965253&content=【悦悦读书】你的验证码12344765&sendTime=&extno=
"""
url_send = "http://sms.hutonginfo.com:9000/sms.aspx?action=send"
# 查询API http://sms.hutonginfo.com:9000/sms.aspx?action=overage&userid=12&account=账号&password=密码
url_info = "http://sms.hutonginfo.com:9000/sms.aspx?action=overage"

userId = settings.SMS_USER_ID
account = settings.SMS_ACCOUNT
password = settings.SMS_PASSWORD


def send_sms_single(mobile, content):
    data = {
        "userid": userId,
        "account": account,
        "password": password,
        "mobile": mobile,
        "content": content,
        "sendTime": '',
        "extno": '',
    }
    res = requests.get(url=url_send, data=data)
    result = res.content.decode()
    print(result)
    # 使用minidom解析器打开 XML 文档
    dom_tree = xml.dom.minidom.parseString(res.content)
    root_node = dom_tree.documentElement
    print("节点名", root_node.nodeName)

    # 默认是失败
    return_status = 'failed'
    return_msg = '未知错误，请联系管理员'

    msg_list = []
    for node in root_node.childNodes:
        msg_list.append(node.nodeName)

    if 'returnstatus' in msg_list:
        status = root_node.getElementsByTagName('returnstatus')[0]
        return_status = status.childNodes[0].data
        print('returnstatus:', status.childNodes[0].data)
    if 'message' in msg_list:
        message = root_node.getElementsByTagName('message')[0]
        return_msg = message.childNodes[0].data
        print('message:', message.childNodes[0].data)
    if 'successCounts' in msg_list:
        success_counts = root_node.getElementsByTagName('successCounts')[0]
        return_sussess_counts = success_counts.childNodes[0].data
        print('successCounts:', success_counts.childNodes[0].data)
    response = {'result': return_status, 'message': return_msg}
    return response


def sms_info():
    data = {
        "userid": userId,
        "account": account,
        "password": password,
    }
    res = requests.get(url=url_info, data=data)
    result = res.content.decode()
    print(result)

    # 使用minidom解析器打开 XML 文档
    dom_tree = xml.dom.minidom.parseString(res.content)
    root_node = dom_tree.documentElement
    print("节点名", root_node.nodeName)

    msg_list = []
    for node in root_node.childNodes:
        msg_list.append(node.nodeName)

    if 'payinfo' in msg_list:
        pay_info = root_node.getElementsByTagName('payinfo')[0]
        print('payinfo:', pay_info.childNodes[0].data)
    if 'overage' in msg_list:
        overage = root_node.getElementsByTagName('overage')[0]
        print('overage:', overage.childNodes[0].data)
    if 'sendTotal' in msg_list:
        send_total = root_node.getElementsByTagName('sendTotal')[0]
        print('sentTotal:', send_total.childNodes[0].data)
