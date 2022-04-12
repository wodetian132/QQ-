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

global run_id
run_id = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
global puk
puk = "10110"
global puk_out
puk_out = "10110"
global lasttime
lasttime = ""

huancun = []

personqq = {'QQnumber': 'name',}

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
    ttii = time.strftime("[%H:%M:%S]", time.localtime())
    qqnumber = str(qqnumber1)
    if qqnumber in personqq:
        if personqq[qqnumber] in search_data:
            a = ttii+"你已经打卡了："+personqq[qqnumber]
            return a
        else:
            search_data.append(personqq[qqnumber])
            a = ttii+"打卡成功,姓名:"+personqq[qqnumber]
            return a
    else:
        a = "打卡失败,原因:QQ号错误"
        return a

def delete_result(qqnumber1):
    ttii = time.strftime("[%H:%M:%S]", time.localtime())
    qqnumber = str(qqnumber1)
    if qqnumber in personqq and personqq[qqnumber] in search_data:
        search_data.remove(personqq[qqnumber])
        a = ttii+"签退成功,姓名:"+personqq[qqnumber]
        return a
    else:
        a = ttii+personqq[qqnumber]+" 签退失败,原因:QQ号错误或未签到"
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

def main_program():
    global mood
    global sat
    global lasttime
    global puk
    global huancun
    while True:
        time.sleep(0.1)
        rev = rev_msg()
        if rev["post_type"] == "message":
            #print(rev)
            qqcontext = rev['raw_message']  # 转存内容
            qq = rev['sender']['user_id']  # 转存发送者信息
            if rev["message_type"] == "private":  # 私聊
                if "结束" in qqcontext and "pin" in qqcontext:
                    mood = 0
                    print("————打卡被结束————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "打卡结束"})
                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':"打卡已经结束"})
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
                    lasttime = ""
                    return 0
                if "恢复" in qqcontext and "0" in qqcontext:
                    mood = 1
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经恢复啦"})
                    continue
                if "暂停" in qqcontext and "0" in qqcontext:
                    print("————暂停————")
                    pp = input(">>>")
                    print("—————恢复—————")
                if "课中" in qqcontext and "0" in qqcontext:
                    print("————课中签到————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已开启"})
                if "重启" in qqcontext and "pin" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经重启"})
                    sat = 2
                    return 0
                if "set" in qqcontext and "0" in qqcontext :
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"现在是签到阶段，发送你的口令"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                puk = rev['raw_message']
                                mood = 1
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，口令为："+puk })
                                break
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送截止时间(格式：01点05分06(24小时制))(秒可以省略，发送0代表不限时间)"})
                    lasttime = ""
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                if rev['raw_message'] == "0":
                                    break
                                for an in rev['raw_message']:
                                    if an >= "0" and an <= "9":
                                        lasttime = lasttime + an
                                if len(lasttime) < 6:
                                    lasttime = lasttime+"00"
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，截止时间为："+lasttime })
                                break
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"是否现在公布"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                if "是" in rev['raw_message'] or "Y" in rev['raw_message'] or "y" in rev['raw_message']:
                                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"公布完成" })
                                    tim = time.strftime("[%H:%M:%S]", time.localtime())
                                    detail = "签到打卡通知"+tim + '\n' +"口令："+puk+"\n"+"截止时间："+lasttime[0:2]+":"+lasttime[2:4]+":"+lasttime[4:6]
                                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':detail})
                                if "否" in rev['raw_message'] or "N" in rev['raw_message'] or "n" in rev['raw_message']:
                                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"好的，打卡设置已完成" })
                                break
                if "settime" in qqcontext:
                    lasttime = ""
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送截止时间"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                for an in rev['raw_message']:
                                    if an != "点":
                                        lasttime = lasttime + an
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，截止时间为："+lasttime })
                                break
                if lasttime != "":
                    re = lasttime
                    sw = time.strftime("%H%M%S", time.localtime())
                    if int(sw) > int(re):
                        mood = 0
                        print("————时间截止————")
                if "puk" in qqcontext and "pin" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':puk})
                    continue
                #if puk in qqcontext and mood == 1:
                #    se = creat_result(rev['user_id'])
                #    print("----------",se)
                #    send_msg({'msg_type': 'private', 'number': qq, 'msg': se})
                #    res = open(f'J:\\Users\\1\\Desktop\\result\\result_in_{puk}.txt', 'a+', encoding='UTF-8')
                #    res.write(f"{se} ")
                #    res.close()
                #    continue
                if "showpin" in qqcontext:
                    tim = time.strftime("[%H:%M:%S]", time.localtime())
                    detail = "打卡通知"+tim + '\n' +"口令："+puk+"\n"+"截止时间："+lasttime
                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':detail})
                if mood == 1:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不开放私聊打卡"})
                else:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不开放私聊打卡"})
            if rev["message_type"] == "group":  # 群聊
                if rev["group_id"] == 234901344 :
                    if lasttime != "" and puk in qqcontext:
                        re = lasttime
                        sw = time.strftime("%H%M%S", time.localtime())
                        if int(sw) > int(re):
                            mood = 0
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':f"[CQ:at,qq={qq}] 时间已过"})
                            print("————时间截止————")
                    if puk in qqcontext and mood == 1:
                        se = creat_result(rev['user_id'])
                        if "你" in se:
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':f"[CQ:at,qq={qq}] {se}"})
                        huancun.append(se)
                        mee = ""
                        if len(huancun)>=5:
                            for i in huancun:
                                mee = mee+i+"\n"
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':mee})
                            huancun = []
                            mee = ""
                        print("----------",se)
                        res = open(f'J:\\Users\\1\\Desktop\\result\\result_in_{puk}_{run_id}.txt', 'a+', encoding='UTF-8')
                        res.write(f"{se}\n")
                        res.close()
                        continue


                    

def out_program():
    global mood
    global sat
    global puk_out
    global huancun
    lasttime = ""
    while True:
        time.sleep(0.1)
        rev = rev_msg()
        if rev["post_type"] == "message":
        # print(rev)
            qqcontext = rev['raw_message']  # 转存内容
            qq = rev['sender']['user_id']  # 转存发送者信息
            if rev["message_type"] == "private":  # 私聊
                if "结束" in qqcontext and "0" in qqcontext:
                    mood = 0
                    print("————签退被结束————")
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': "打卡结束"})
                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':"打卡已经结束"})
                    continue
                if "返回签到" in qqcontext and "0" in qqcontext:
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
                if "暂停" in qqcontext and "0" in qqcontext:
                    print("————暂停————")
                    pp = input(">>>")
                    print("—————恢复—————")
                if "恢复" in qqcontext and "0" in qqcontext:
                    mood = 1
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经恢复啦"})
                    continue
                if "set" in qqcontext and "0" in qqcontext :
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"现在是签退时间，发送你的口令"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                puk_out = rev['raw_message']
                                mood = 1
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，口令为："+puk_out })
                                break
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送截止时间(格式：01点05分01（24小时制))(秒可以省略，可以发送0代表无限制)"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                if rev['raw_message'] == "0":
                                    break
                                for an in rev['raw_message']:
                                    if an >="0" and an <="9":
                                        lasttime = lasttime + an
                                if len(lasttime) < 6:
                                    lasttime = lasttime + "00"
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，截止时间为："+lasttime })
                                break
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"是否现在公布"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                if "是" in rev['raw_message'] or "Y" in rev['raw_message'] or "y" in rev['raw_message']:
                                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"公布完成" })
                                    tim = time.strftime("[%H:%M:%S]", time.localtime())
                                    detail = "签退打卡通知"+tim + '\n' +"口令："+puk_out+"\n"+"截止时间："+lasttime[0:2]+":"+lasttime[2:4]+":"+lasttime[4:6]
                                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':detail})
                                if "否" in rev['raw_message'] or "N" in rev['raw_message'] or "n" in rev['raw_message']:
                                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"好的，打卡设置已完成" })

                                break
                if "puk" in qqcontext and "0" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':puk_out})
                    continue
                if "重启" in qqcontext and "0" in qqcontext:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"已经重启"})
                    sat = 2
                    return 0
                if "settime" in qqcontext:
                    lasttime = ""
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"发送截止时间"})
                    while True:
                        rev = rev_msg()
                        if rev["post_type"] == "message":
                            if rev['sender']['user_id'] == qq:
                                for an in rev['raw_message']:
                                    if an != "点":
                                        lasttime = lasttime + an
                                send_msg({'msg_type': 'private', 'number': qq, 'msg':"设置成功，截止时间为："+lasttime })
                                break
                if lasttime != "":
                    re = lasttime
                    sw = time.strftime("%H%M%S", time.localtime())
                    if int(sw) > int(re):
                        mood = 0
                        print("————时间截止————")
                if "showpin" in qqcontext:
                    tim = time.strftime("[%H:%M:%S]", time.localtime())
                    detail = "打卡通知"+tim + '\n' +"口令："+puk_out+"\n"+"截止时间："+lasttime
                    send_msg({'msg_type': 'group', 'number': 234901344, 'msg':detail})
                if mood == 1:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不开放私聊打卡"})
                else:
                    send_msg({'msg_type': 'private', 'number': qq, 'msg':"不开放私聊打卡"})
            if rev["message_type"] == "group":  # 群聊
                if rev["group_id"] == 234901344 :
                    if lasttime != "" and puk_out in qqcontext:
                        re = lasttime
                        sw = time.strftime("%H%M%S", time.localtime())
                        if int(sw) > int(re):
                            mood = 0
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':f"[CQ:at,qq={qq}] 时间已过"})
                            print("————时间截止————")
                    if puk_out in qqcontext and mood == 1:
                        se = delete_result(rev['user_id'])
                        if "你" in se:
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':f"[CQ:at,qq={qq}] {se}"})
                        huancun.append(se)
                        if len(huancun)>=5:
                            mee = ""
                            for i in huancun:
                                mee = mee+i+"\n"
                            send_msg({'msg_type': 'group', 'number': 234901344, 'msg':mee})
                            huancun = []
                            mee = ""
                        print("----------",se)
                        res = open(f'J:\\Users\\1\\Desktop\\result\\result_out_{puk_out}_{run_id}.txt', 'a+', encoding='UTF-8')
                        res.write(f"{se}\n")
                        res.close()
                        continue

print("----The program will run.----\n\n\n")
global mood
global sat
mood = 0
sat = 1
search_data = []
while True:
    print("—————已启动—————\n\n\n")
    if sat == 1:
        main_program()
    if sat == 0:
            out_program()
    if sat == 2:
        sat = 1
        mood = 0
        search_data = []
    print("—————ERROR—————\n\n\n")
