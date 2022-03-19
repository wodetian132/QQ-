from ast import Pass
from doctest import OutputChecker
import socket
import json
import time

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5710))
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n\r\n
'''

personqq = {'qqnumber' : 'name' ,}

def setup():
    global mood
    global sat
    search_data = []
    mood = 0
    sat = 1
    print("----The program will run.----\n\n\n")

def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5701))

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


# 定位有效信息
def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i] == "{" and msg[-1] == "\n":
            return json.loads(msg[i:])
    return None


# 需要循环执行，返回值为json格式
def rev_msg():  # json or None
    conn, Address = ListenSocket.accept()
    Request = conn.recv(2048).decode('utf-8', 'ignore')
    # print(Request)
    rev_json = request_to_json(Request)
    # print(rev_json)
    conn.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    conn.close()
    return rev_json

def creat_result(qqnumber1):
    qqnumber = str(qqnumber1)
    if qqnumber in personqq:
        if personqq[qqnumber] in search_data:
            a = "你已经打卡了："+personqq[qqnumber]
            return a
        else:
            search_data.append(personqq[qqnumber])
            a = "打卡成功,姓名:"+personqq[qqnumber]
            return a
    else:
        a = "打卡失败,原因:QQ号错误"
        return a

def delete_result(qqnumber1):
    qqnumber = str(qqnumber1)
    if qqnumber in personqq and personqq[qqnumber] in search_data:
        search_data.remove(personqq[qqnumber])
        a = "签退成功,姓名:"+personqq[qqnumber]
        return a
    else:
        a = "签退失败,原因:QQ号错误或未签到"
        return a

def qqsearch(kk):
    nam = open('J:\\Users\\1\\Desktop\\name.txt', 'r', encoding='UTF-8')
    searchresult = []
    while True:
        name = nam.readline()
        if name[0:2] == "en":
            break
        lon = len(name)
        n = 0
        con = 0
        while True:
            k = kk[n:n + lon - 1]
            if k[0:2] == "aa":
                break
            n += 1
            if k + '\n' == name:
                con = 1
                break
        if con == 0:
            searchresult.append(name)
    return searchresult

def mainprogram():
    global mood
    global sat
    puk = "qazwsxedc"
    while True:
        time.sleep(0.02)
        rev = rev_msg()
        if rev["post_type"] == "message":
        # print(rev)
            qqcontext = rev['raw_message']  # 转存内容
            qq = rev['sender']['user_id']  # 转存发送者信息
            if rev["message_type"] == "private":  # 私聊
                if puk in qqcontext and mood == 1:
                    se = creat_result(rev['user_id'])
                    print("----------",se)
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': se})
                    res = open(f'J:\\Users\\1\\Desktop\\result\\result_in_{puk}.txt', 'a+', encoding='UTF-8')
                    res.write(f"{se} ")
                    res.close()
                    continue
                if "结束" in qqcontext and "pin" in qqcontext:
                    mood = 0
                    print("————打卡被结束————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "打卡结束"})
                    continue
                if "结果" in qqcontext or "查询" in qqcontext:
                    print("接到查询:",qq)
                    ae = ''.join(search_data)
                    ed = qqsearch(ae+'aaaaaaaa')
                    re = ''.join(ed)
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"未签到:\n"+re})
                    continue
                if "签退" in qqcontext and "pin" in qqcontext:
                    print("————开始签退————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "开始签退"})
                    mood = 1
                    sat = 0
                    return 0
                if "恢复" in qqcontext and "pin" in qqcontext:
                    mood = 1
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经恢复啦"})
                    continue
                if "暂停" in qqcontext and "pin" in qqcontext:
                    print("————暂停————")
                    pp = input(">>>")
                    print("—————恢复—————")
                if "setpuk" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送你的口令"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                puk = rev['raw_message']
                                mood = 1
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，口令为："+puk })
                                break
                    continue
                if "puk" in qqcontext and "pin" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':puk})
                    continue
                if mood == 1:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"口令错误"})
                else:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不处于打卡时间内"})

def outprogram():
    global mood
    global sat
    puk_out = "qazwsxedc"
    while True:
        time.sleep(0.02)
        rev = rev_msg()
        if rev["post_type"] == "message":
        # print(rev)
            qqcontext = rev['raw_message']  # 转存内容
            qq = rev['sender']['user_id']  # 转存发送者信息
            if rev["message_type"] == "private":  # 私聊
                if puk_out in qqcontext and mood == 1:
                    se = delete_result(rev['user_id'])
                    print("----------",se)
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': se})
                    res = open(f'J:\\Users\\1\\Desktop\\result\\result_out_{puk_out}.txt', 'a+', encoding='UTF-8')
                    res.write(f"{se} ")
                    res.close()
                    continue
                if "结束" in qqcontext and "pin" in qqcontext:
                    mood = 0
                    print("————签退被结束————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "打卡结束"})
                    continue
                if "返回签到" in qqcontext and "pin" in qqcontext:
                    mood = 1
                    sat = 1
                    print("————签到重新开始————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "签到开始"})
                    return 0
                if "结果" in qqcontext or "查询" in qqcontext:
                    print("接到查询:",qq)
                    ae = ''.join(search_data)
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"未签退:\n"+ae})
                    continue
                if "暂停" in qqcontext and "pin" in qqcontext:
                    print("————暂停————")
                    pp = input(">>>")
                    print("—————恢复—————")
                if "恢复" in qqcontext and "pin" in qqcontext:
                    mood = 1
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经恢复啦"})
                    continue
                if "setpuk" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送你的口令"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                puk_out = rev['raw_message']
                                mood = 1
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，口令为："+puk_out })
                                break
                    continue
                if "puk" in qqcontext and "pin" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':puk_out})
                    continue
                if "重启" in qqcontext and "12138" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"REBOOT"t})
                    setup()
                    return 0
                if mood == 1:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"口令错误"})
                else:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不处于打卡时间内"})



global mood
global sat
setup()
while True:
    print("—————已启动—————\n\n\n")
    try:
        if sat == 1:
            mainprogram()
        if sat == 0:
            outprogram()
    except:
        print("—————ERROR—————\n\n\n")
