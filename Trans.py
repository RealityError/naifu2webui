# -*- coding: utf-8 -*-
# @Time : 2022/12/14 
# @Author : 白猫猫
# @File : Trans.py
# @Software: Vscode|虚拟环境|3.10.6

'''
调用百度的翻译api，实现中文prompt
'''

import requests
from config import API_Key,Secret_Key
from log import logger

#检测是否为中文字符，免得多次消耗翻译次数
def is_chinese(string):
    """
    检查整个字符串是否包含中文
    需要检查的字符串 string: str
    return: bool  
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def trans(text,from_lang,to_lang) -> str:
    #先检测一下是否为中文
    if is_chinese(text) is False:
        return text 
    
    #因为百度api时不时变动，我这里已经改了两次，建议使用时先测试一下
    
    #获取token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_Key+'&client_secret='+Secret_Key
    response = requests.get(host)
    #获取token
    token = response.json()["access_token"]
    url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + token
    
    
    term_ids = ''  # 术语库id，多个逗号隔开
    #发送翻译请求，获取翻译接结果
    try:
        while 1:
            headers = {'Content-Type': 'application/json'}
            payload = {'q': text, 'from': from_lang, 'to': to_lang, 'termIds': term_ids}
            r = requests.post(url, params=payload, headers=headers)
            result = r.json()["result"]["trans_result"][0]['dst']
            if result != "":
                break
            else:
                logger.warning("翻译模块未成功翻译，重试中")
    except:
        logger.error("翻译模块错误,请检查设定")
        result = "*ERROR*"
        return result
    logger.info(""+ text)#这里输出一下原文，方便后台查看和对照   
    logger.info("翻译："+result)   
    return result
    
    
    


