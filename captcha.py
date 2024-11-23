# from request import http


# def game_captcha(gt: str, challenge: str): 
#     rep = http.post( 
#         url= "http://api.rrocr.com/api/recognize.html", 
#         data={
#                 "appkey": "",
#                 "gt": gt,
#                 "challenge" : challenge,
#                 "referer" : "https://api-takumi.mihoyo.com/event/luna/sign" 
#             } 
#         ).json() 
#     return rep["data"]["validate"]# 失败返回None 成功返回validate

# def bbs_captcha(gt: str, challenge: str):
#     rep = http.post( 
#         url= "http://api.rrocr.com/api/recognize.html", 
#         data={
#                 "appkey": "",
#                 "gt": gt,
#                 "challenge" : challenge,
#                 "referer" : "https://bbs-api.miyoushe.com/apihub/app/api/signIn" 
#             } 
#         ).json() 
#     return rep["data"]["validate"]# 失败返回None 成功返回validate


import config
import tools
from loghelper import log
from request import http

import yaml

# 加载 config.yaml 文件
with open("config/config.yaml", "r", encoding="utf-8") as file:
    config_yaml = yaml.safe_load(file)

# 使用 YAML 配置
config = {
    "captcha": {
        "token": config_yaml["captcha"]["token"]
    }
}

# 测试 token 加载
# print(config["captcha"]["token"])

# 打码apikey
token = config['captcha']['token']

def game_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge, 'https://passport-api.mihoyo.com/account/ma-cn-passport/app/loginByPassword')
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def bbs_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge,
                       "https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id"
                       "=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon")
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def geetest(gt: str, challenge: str, referer: str):
    response = http.post('http://api.rrocr.com/api/recognize.html', params={
        'appkey': config.config['captcha']['token'],
        'gt': gt,
        'challenge': challenge,
        'referer': referer
    }, timeout=60000)
    data = response.json()
    if data['status'] != 0:
        log.warning(data['msg'])  # 打码失败输出错误信息
        return None
    return data['data']  # 失败返回None 成功返回validate