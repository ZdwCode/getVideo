# 找到未加密的参数
# 想办法把参数进行加密  （必须参考网易的逻辑）
# 请求到网易拿到评论
import requests
from Crypto.Cipher import AES;
from base64 import b64encode
import json

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
# 第一个参数
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_1901371647",
    "threadId": "R_SO_4_1901371647"
}
# 第二个参数
e = '010001'
# 第三个参数
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
# 第四个参数
g = '0CoJUm6Qyw8W8jud'

i = "gcbRwuLzJcbzxAPC"


def get_ensSecKey():
    return "24caa54f2cccf556753a02162ae1f2c37d9ae4af3289e9b773100a3c2d284b94232ac513680119fdb38b3551f18f1e6bb6fd00d49507502da30df2e0d361e01c702be2dd4b31a97a25e95f00e2cdd5663a6ba0e6b328dd073d1c5e1b2a0278accce59c3645065ef1f61e965ef505e8f9842e8f1e0680242e511b8fc37aadc522"


def get_params(data):
    first = enc_params(data, g);
    secend = enc_params(first, i);
    return secend;


def to_16(data):
    pad = 16 - len(data) % 16;
    data += chr(pad) * pad
    return data


def enc_params(data, key):
    aes = AES.new(key=key.encode('utf-8'), iv="0102030405060708".encode('utf-8'), mode=AES.MODE_CBC)
    data = to_16(data)
    bs = aes.encrypt(data.encode('utf-8'))  # 加密的内容长度必须是16的倍数
    return str(b64encode(bs), "utf-8")


'''
function a(a =16 ) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c  #最后c就是一个16位的随机字符串
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, { #c是密钥
            iv: d,#偏移量
            mode: CryptoJS.mode.CBC #加密模式
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { d:就是我们的数据i7b——>data,e:固定值 010001，f：很长的一个定值 g:也是一个定值
        var h = {}
          , i = a(16);==>i就是一个16位的随机值
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),==>parems --两次加密
        h.encSecKey = c(i, e, f),==>encSeckey
        h
    }

var bVj7c = window.asrsea(JSON.stringify(i7b), bsR1x(["流泪", "强"]), bsR1x(Xp4t.md), bsR1x(["爱心", "女孩", "惊恐", "大笑"]));

'''

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
resp = requests.post(url, data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_ensSecKey()
})
resp.encoding = 'utf-8'
dic = resp.json();
comments = dic['data']['hotComments']
for comment in comments:
    content = comment['content']
    print(content)
    break;  # 测试用

