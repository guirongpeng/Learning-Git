import base64
import hashlib
import hmac
import json
import time
import requests
import urllib
from collections import OrderedDict
# 这是分支test_branch，并且再本地修改
class Translate:
    def __init__(self):
        self.appid = '20240301001978679'
        self.seckey = '9gcSsvAsujFggpqJoqjJ'

    def create_quote_job(self, from_lang, to_lang, extend, file_name, file_path):
        url = 'https://fanyi-api.baidu.com/transapi/doctrans/createjob/quote'
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        input_data = {
            'from': from_lang,
            'to': to_lang,
            'input': {
                'content': content,
                'format': extend,
                'filename': file_name
            }
        }
        timestamp = int(time.time())
        sign = self.create_sign(timestamp, input_data)
        headers = self.create_headers(timestamp, sign)
        response = requests.post(url, headers=headers, json=input_data)
        return response.text

    def query_quote(self, file_id):
        url = 'https://fanyi-api.baidu.com/transapi/doctrans/query/quote'
        input_data = {'fileId': file_id}
        timestamp = int(time.time())
        sign = self.create_sign(timestamp, input_data)
        headers = self.create_headers(timestamp, sign)
        response = requests.post(url, headers=headers, json=input_data)
        return response.text

    def create_trans_job(self, from_lang, to_lang, extend, file_name, file_path, output=''):
        url = 'https://fanyi-api.baidu.com/transapi/doctrans/createjob/trans'
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        input_data = {
            'from': from_lang,
            'to': to_lang,
            'input': {
                'content': content,
                'format': extend,
                'filename': file_name
            },
            'output': {
                'format': output
            }
        }
        timestamp = int(time.time())
        sign = self.create_sign(timestamp, input_data)
        headers = self.create_headers(timestamp, sign)
        response = requests.post(url, headers=headers, json=input_data)
        return response.text

    def query_trans(self, request_id):
        url = 'https://fanyi-api.baidu.com/transapi/doctrans/query/trans'
        input_data = {'requestId': request_id}
        timestamp = int(time.time())
        sign = self.create_sign(timestamp, input_data)
        headers = self.create_headers(timestamp, sign)
        response = requests.post(url, headers=headers, json=input_data)
        return response.text

    def create_sign(self, timestamp, input_data):
        query_str = json.dumps(input_data)
        sign_str = '{}{}{}'.format(self.appid, timestamp, query_str)
        sign = base64.b64encode(hmac.new(self.seckey.encode('utf-8'), sign_str.encode('utf-8'), digestmod=hashlib.sha256).digest())
        return sign

    def create_headers(self, timestamp, sign):
        return {
            'Content-Type': 'application/json',
            'X-Appid': self.appid,
            'X-Sign': sign,
            'X-Timestamp': str(timestamp),
        }

    def url_encoder(self, params):
        return urllib.parse.urlencode(params)


from_lang = 'en'
to_lang = 'zh'
file_path = r"D:\Code_soft\anaconda_soft\df\help_other\QH-work\data\data\ALTAIR_HELP\docs.xlsx"
extend = 'xlsx'
output = 'xlsx'
file_name = 'ceshi.xlsx'
trans_obj = Translate()

# # 创建报价服务
# quote_ret = trans_obj.create_quote_job(from_lang, to_lang, extend, file_name, file_path)
# print(quote_ret)

# # 查询报价结果
# file_id = 'd82b4084f8abd83e19a3dbf001a4cf35'
# query_quote_ret = trans_obj.query_quote(file_id)
# print(query_quote_ret)

# 创建翻译服务
trans_ret = trans_obj.create_trans_job(from_lang, to_lang, extend, file_name, file_path, output)
print(trans_ret)

# 查询翻译结果
# request_id = 3267102
# query_trans_ret = trans_obj.query_trans(request_id)
# print(query_trans_ret)
