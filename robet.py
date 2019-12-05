# @author：从北相北
# @弹幕聊天机器人
import json, time
import re, requests
import threading


def open():
    # 填入cookie，解析得到token，调用线程模块中的定时器，使用get方法得到实时dm
    cookie = " "
    token = re.search(r'bili_jct=(.*?);', cookie).group(1)

    url = 'https://api.live.bilibili.com/ajax/msg'
    form = {
        'roomid': roomid,
        'visit_id': '',
        'csrf_token': token,  # csrf_token就是cookie中的bili_jct字段;且有效期是7天!!!
    }
    html = requests.post(url, data=form)
    result = html.json()['data']['room']
    for i in result:
        if i not in dm:
            dm.append(i)
            AImsg = qkrobot(i['text'])
            # 调用ai接口
            time.sleep(10)
            # 设置休眠时间
            getlive(i['uid'],i['text'],AImsg, token, cookie)
            print(i)
            # 发送AI的回复
        # print('[' + i['nickname'] + ']:' + i['text'])
    t = threading.Timer(2, open)
    t.start()


def qkrobot(msg):
    urls = "http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + msg
    # print(urls)
    res = requests.request('get', urls)
    response_dict = json.loads(res.text)
    result = response_dict['content']
    # print(result)
    return result


def getlive(mi,mt,AImsg, token, cookie):
    url_send = 'https://api.live.bilibili.com/msg/send'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': cookie
    }
    data = {
        'color': '16777215',
        'fontsize': '25',
        'mode': '1',
        'msg': AImsg,
        'rnd': int(time.time()),
        'roomid': roomid,
        'csrf_token': token,
        'csrf': token
    }
    try:
        if re.match(r'^(#)',mt):
            print("略过点歌")

        elif mi==123456:
            #自己的uid
            print("不要自言自语哦")
        else:
            print(mi)
            # print()
            html_send = requests.post(url_send, data=data, headers=headers)
            result = html_send.json()
            print(result)
    except:
        raise



if __name__ == '__main__':
    dm = []
    roomid = "21574137"
    open()
    # qkrobot('你好')

    # 要认证，不用这个接口了
    # URL = "http://openapi.tuling123.com/openapi/api/v2"
    # HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}
    # TURING_KEY = "18f30b1316204d97b9e70b7acf73785d"
    # def robot(text=""):
    #     data = {
    #         "reqType": 0,
    #         "perception": {
    #             "inputText": {
    #                 "text": ""
    #             },
    #             "selfInfo": {
    #                 "location": {
    #                     "city": "杭州",
    #                     "street": "网商路"
    #                 }
    #             }
    #         },
    #         "userInfo": {
    #             "apiKey": TURING_KEY,
    #             "userId": "starky"
    #         }
    #     }
    #
    #     data["perception"]["inputText"]["text"] = text
    #     response = requests.request("post", URL, json=data, headers=HEADERS)
    #     response_dict = json.loads(response.text)
    #
    #     result = response_dict["results"][0]["values"]["text"]
    #     print("the AI said: " + result)
    #     return result
