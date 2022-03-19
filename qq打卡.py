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

personqq = {'1091003274' : '李俣霖' , '1391274373' : '孙国胜' , '930530078' : '郝文婷' , '2320788292' : '刘天阔' , '609691476' : '孟凯' , '2394316673' : '李名扬' , '3100827413' : '殷衍凯' , '2134873537' : '张啸晨' , '1092141625' : '白子轩' , '2405198667' : '康志毅' ,
'1409317640' : '董玉烁' , '2024806229' : '张承达' , '2859226713' : '王浩' , '2980508137' : '翟淑君' , '3503840690' : '牛得嘉' , '2687649890' : '蒲李忠垚' , '2948340731' : '滕绍勇' , '1508069064' : '马欣宇' , '1706593792' : '杨鸿泽' , '2020198567' : '王晨璐' ,
'1665453106' : '刘雨涵' , '2802169662' : '张浩宇' , '2149067539' : '陈钰婷' , '1052165891' : '张世凯' , '717478614' : '董凯铭' , '1846921494' : '谭博文' , '1822188253' : '李冰烁' , '2567412958' : '殷昕泽' , '482323327' : '康益嘉' , '2900169374' : '张心悦' ,
'3151658783' : '吴政扬' , '2889405754' : '黄灵圣' , '2952496878' : '于文睿' , '2985870839' : '刘润青' , '1551477697' : '刘秦志' , '1787752138' : '王钰淇' , '312367013' : '桑玉坤' , '494993408' : '刘元琦' , '1911319177' : '祖丽凯尔' , '3391200591' : '周星宇' ,
'2911564088' : '冯煜章' , '782591269' : '侯志澍' , '1460505243' : '郑家鑫' , '3216858409' : '赵恩惠' , '1136581674' : '阿孜古丽' , '1910529908' : '李府洵','2245954481' : '邴秀洁' , '744693811' : '陈德堃' , '2146455270' : '黄晓萌' , '1969876832' : '李紫妍' ,
'1851356925' : '孙泓畅' , '1306690852' : '孙绮笛' , '3212578471' : '宋馨坤' , '1425704680' : '王沛霖' , '983008127' : '杨馥铭' , '1400309344' : '张志成' , '3153786128' : '张梓煜' , '1322156577' : '艾德钰' , '2363104110' : '崔浩天' , '2672732213' : '陈艺杰' ,
'1627781905' : '曹曜齐' , '1639179799' : '车资璇' , '2906696660' : '董岱桦' , '749826833' : '狄思妍' , '1907893548' : '董珍绮' , '3132802447' : '古再丽努尔' , '2363801362' : '黄钧策' , '2411845903' : '韩金龙' , '1304400907' : '贾艺佳' , '2410363431' : '刘居鑫' ,
'1480634414' : '李良玉' , '1332158395' : '李润泽' , '2778816980' : '齐冠瑜' , '2495285006' : '孙宁泽' , '2812775446' : '孙启霖' , '805992465' : '孙圣凯' , '2136286057' : '宋兆基' , '951957641' : '王珩宇' , '2982239715' : '王金彤' , '1599101275' : '王嘉伟' ,
'2188774248' : '王俊逸' , '1250844098' : '王璐泽' , '2922513642' : '王新宇' , '2608688485' : '王元清' , '1449762499' : '王宜泽' , '2329626703' : '伊卜拉伊木' , '2074772701' : '姚茂恒' , '1345736696' : '郑锦扬' , '3256416569' : '张家原' , '1815869455' : '张昕星' ,
'2021866989' : '张旭颖' , '3574604744' : '张耀文' , '3166113775' : '张潆心' , '2312207801' : '张仔坤' , '3277406690' : '张子悦'}

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
