# coding: utf-8
import hashlib
import os
import random
import requests
import xmltodict as xmltodict

project_path = os.path.dirname(os.path.abspath(__file__)) # 项目所在路径
APPID = ''
MCHID = ''
APIKEY = ''
CERT_PATH = os.path.join(project_path, 'apiclient_cert.pem')
KEY_PATH = os.path.join(project_path, 'apiclient_key.pem')
NOTIFY_URL = ''

class weixin_pay(object):

    # 生成随机字符串
    def get_nonce_str(self, length=32):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    # 获取格式化参数
    def get_string(self, params):
        slist = sorted(params)
        buff = []
        for k in slist:
            if not params[k]:
                continue
            v = str(params[k])
            buff.append("{0}={1}".format(k, v))
        return "&".join(buff)

    # 生成sign密钥
    def get_sign(self, params):
        # 按照参数名ASCII字典序排序
        stringA = self.get_string(params)
        # 拼接API密钥，生成sign
        stringSignTemp = stringA + '&key=' + APIKEY  # APIKEY密钥
        sign = (hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()).upper()
        return sign

    # 定义字典转XML的函数
    def dict_to_xml(self, params):
        xml = "<xml>"
        for k, v in params.items():
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        return xml

    # 验证sign密钥
    def check_sign(self, params):
        _sign = params['sign']
        del params['sign']
        # 按照参数名ASCII字典序排序
        stringA = self.get_string(params)
        # 生成sign，拼接API密钥
        stringSignTemp = stringA + '&key=' + APIKEY  # APIKEY密钥
        sign = (hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()).upper()
        if _sign == sign:
            return True
        return False

    # 统一下单
    def get_prepay_id(self, out_trade_no, total_fee, body):
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        params = {
            'appid': APPID,  # appid
            'mch_id': MCHID,  # 商户号
            'body': body,  # 商品描述
            'nonce_str': self.get_nonce_str(16),  # 16位随机字符串
            'out_trade_no': out_trade_no,  # 商户订单号
            'total_fee': str(total_fee),  # 订单金额，以分为单位
            'notify_url': NOTIFY_URL,  # 通知地址
            'trade_type': 'APP'  #
        }
        params['sign'] = self.get_sign(params)
        xml = self.dict_to_xml(params)
        xml = xml.encode('utf-8')
        res = requests.post(url, data=xml)
        res = res.content.decode()
        xmlresp = xmltodict.parse(res)['xml']
        if self.check_sign(xmlresp):
            print(xmlresp)
            return xmlresp
        else:
            return {}

    # 申请退款
    def application_refund(self, out_refund_no, total_fee, refund_fee, transaction_id=None, out_trade_no=None, refund_desc=None):
        url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        params = {
            'appid': APPID,  # appid
            'mch_id': MCHID,  # 商户号
            'nonce_str': self.get_nonce_str(16),  # 16位随机字符串
            'out_refund_no': out_refund_no,  # 商户退款单号
            'total_fee': str(total_fee),  # 订单金额，以分为单位
            'refund_fee': str(refund_fee),  # 退款金额，以分为单位
        }
        if transaction_id:
            params['transaction_id'] = transaction_id  # 微信订单号
        else:
            params['out_trade_no'] = out_trade_no  # 商户订单号
        if refund_desc:
            params['refund_desc'] = refund_desc
        params['sign'] = self.get_sign(params)
        xml = self.dict_to_xml(params)
        xml = xml.encode('utf-8')
        # 退款请求需要双向证书
        res = requests.post(url, data=xml, cert=(CERT_PATH, KEY_PATH), verify=True)
        res = res.content.decode()
        xmlresp = xmltodict.parse(res)['xml']
        if self.check_sign(xmlresp):
            print(xmlresp)
            return xmlresp
        else:
            return {}



if __name__ == '__main__':
    weixin = weixin_pay()
    weixin.application_refund('TR273556812175100040', 1, 1, transaction_id='4200000443201910166217092818', refund_desc='测试')