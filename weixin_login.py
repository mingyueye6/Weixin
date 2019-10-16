# coding: utf-8
import requests


APPID = ""
SECRET = ""

class weixin_login(object):

    # 第一步：移动应用微信授权登录,获取code

    # 第二步：通过 code 获取 access_token
    def get_access_token(self, code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(APPID, SECRET, code)
        res = requests.get(url)
        res.encoding = 'utf-8'
        res = res.json()
        access_token = res.get('access_token', '')
        openid = res.get('openid', '')
        return (access_token, openid)

    # 第三步：通过access_token调用接口,获取用户信息
    def get_infos(self, code):
        access_token, openid = self.get_access_token(code)
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}'.format(access_token, openid)
        res = requests.get(url)
        res.encoding = 'utf-8'
        res = res.json()
        print(res)
        return res



if __name__ == '__main__':
    weixin = weixin_login()
    weixin.get_infos('code')


# 用户信息
# 参数	说明
# openid	普通用户的标识，对当前开发者帐号唯一
# nickname	普通用户昵称
# sex	普通用户性别，1 为男性，2 为女性
# province	普通用户个人资料填写的省份
# city	普通用户个人资料填写的城市
# country	国家，如中国为 CN
# headimgurl	用户头像，最后一个数值代表正方形头像大小（有 0、46、64、96、132 数值可选，0 代表 640*640 正方形头像），用户没有头像时该项为空
# privilege	用户特权信息，json 数组，如微信沃卡用户为（chinaunicom）
# unionid	用户统一标识。针对一个微信开放平台帐号下的应用，同一用户的 unionid 是唯一的。