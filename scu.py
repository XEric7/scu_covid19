# -*- coding: utf8 -*-

import pytz
import requests
from datetime import datetime


s = requests.Session()


#填写地址信息，开发人员工具中对"https://wfw.scu.edu.cn/ncov/wap/default/save"的post请求可以查到
state="school"
if state=="home":
    geo_api_info=''
elif state=="school":
    geo_api_info='{"type":"complete","info":"SUCCESS","status":1,"cEa":"jsonp_867871_","position":{"Q":30.55209,"R":103.99365,"lng":103.99365,"lat":30.55209},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"028","adcode":"510116","businessAreas":[{"name":"白家","id":"510116","location":{"Q":30.562482,"R":104.006821,"lng":104.006821,"lat":30.562482}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"川大路三段","streetNumber":"363号","country":"中国","province":"四川省","city":"成都市","district":"双流区","township":"西航港街道"},"formattedAddress":"四川省成都市双流区西航港街道三八广场四川大学江安校区","roads":[],"crosses":[],"pois":[]}'
    


cookies_str=""  #登陆后的cookie信息
api_key = "SCT66990TERKRipWCNOiUk7OUSdbXZKtW"  # server酱的api，填了可以微信通知打卡结果，不填没影响

#将str类型cookies转换未dict类型
cookies_dict={}
for cookie in cookies_str.split('; '):
    cookies_dict[cookie.split('=')[0]]=cookie.split('=')[-1]
    


def get_daily(s: requests.Session):
    daily = s.get(url="https://wfw.scu.edu.cn/ncov/api/default/daily?xgh=0&app_id=scu",cookies=cookies_dict)
    j = daily.json()
    d = j.get('d', None)
    if d:

        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def submit(s: requests.Session, old: dict):
    new_daily = {
        'zgfxdq':old['zgfxdq'],  #今日是否在高风险地区
        'mjry':old['mjry'],#今日是否接触密接人员
        'csmjry':old['csmjry'],#近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触？
        'szxqmc':old['szxqmc'],         #所在校区
        'sfjzxgym':old['sfjzxgym'],#是否接种过新冠疫苗？
        'jzxgymrq':old['jzxgymrq'],#接种第一剂新冠疫苗时间
        'sfjzdezxgym':old['sfjzdezxgym'],#是否接种第二剂新冠疫苗？
        'jzdezxgymrq':old['jzdezxgymrq'],#接种第二剂新冠疫苗时间
        'tw':old['tw'],             #体温
        'sfcxtz':old['sfcxtz'],     #是否出现体征？
        'sfyyjc':old['sfyyjc'],   #是否到相关医院或门诊检查？
        'sfjcbh':old['sfjcbh'],#是否接触病患 ？疑似/确诊人群
        'sfcxzysx':old['sfcxzysx'],#是否出现值得注意的情况？
        'qksm':old['qksm'],#情况说明
        'jcjgqr':old['jcjgqr'],#检查结果
        'remark':old['remark'],#其他信息
        'address':old['address'],
        'geo_api_info': geo_api_info,
        'area':old['area'],
        'province':old['province'],
        'city':old['city'],
        'sfzx':old['sfzx'],         #是否在校
        'sfjcwhry':old['sfjcwhry'], #是否接触武汉人员
        'sfjchbry':old['sfjchbry'],#是否接触湖北人员
        'sfcyglq':old['sfcyglq'], #是否处于隔离期？
        'gllx':old['gllx'],#观察场所
        'glksrq':old['glksrq'],#观察开始时间
        'jcbhlx':old['jcbhlx'],#接触人群类型
        'jcbhrq':old['jcbhrq'],#接触时间
        'bztcyy':old['bztcyy'],#当前地点与上次不在同一城市，原因
        'sftjhb': old['sftjhb'],    #是否途经湖北
        'sftjwh':old['sftjwh'], #是否途经武汉
        'szcs':old['szcs'],#所在城市
        'szgj':old['szgj'],
        'fjsj':"0",   #未知信息
        'sfjxhsjc':old['sfjxhsjc'],
        'bzxyy':old['bzxyy'],  #是否回家
        'jcjg':old['jcjg'],
        'hsjcrq':old['hsjcrq'],
        'hsjcdd':old['hsjcdd'],
        'hsjcjg':old['hsjcjg'],
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
        'sfsfbh':old['sfsfbh'],
        'uid':old['uid'],
        'created':old['created'],
        'jcqzrq':old['jcqzrq'],
        'sfjcqz': old['sfjcqz'],
        'szsqsfybl':old['szsqsfybl'],
        'sfsqhzjkk':old['sfsqhzjkk'],
        'sqhzjkkys':old['sqhzjkkys'],
        'sfygtjzzfj':old['sfygtjzzfj'],
        'gtjzzfjsj':old['gtjzzfjsj'],
        'id':old['id'],
        'gwszdd':"",    #未知信息
        'sfyqjzgc':"",
        'jrsfqzys':"",
        'jrsfqzfy':"",
        'szgjcs':"",#所在地点
        'ismoved':old['ismoved'],
        

        }
    #r = s.post("http://192.168.0.3", data=new_daily,cookies=cookies_dict)
    r = s.post("https://wfw.scu.edu.cn/ncov/wap/default/save", data=new_daily,cookies=cookies_dict)
    print("提交信息:", new_daily)
    # print(r.text)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")

    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if api_key:
            message(api_key, result.get('m'), new_daily)
        

def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(key, title, body)
    requests.get(msg_url)


def main_handler(event, context):
    """
    腾讯云云函数入口
    """
    print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    yesterday = get_daily(s)
    print(yesterday)
    submit(s, yesterday)
