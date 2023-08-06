# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 9:37
# @Author  : ZhangWenJun
# @File    : Trend.py
# @conModule :allure历史趋势

import requests

def getip():
    '''获取ip'''
    url = "https://icanhazip.com/"
    payload = ""
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text.rstrip('\n')

if __name__ == '__main__':
    getip()
