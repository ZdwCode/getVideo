# /20220218/5TQqukCg/index.m3u8"
# https://ukzy.ukubf2.com/20220218/5TQqukCg/index.m3u8?skipl=1
import re;
import os;
import requests;
import asyncio;
import aiohttp;
import aiofiles;
from bs4 import BeautifulSoup
def get_iframe_src(main_url):
    resp=requests.get(main_url)
    #匹配到iframe标签中的src
    page = BeautifulSoup(resp.text,'html.parser')
    src = page.find('iframe').get('src')
    return src;
    #return 'https://ukzy.ukubf2.com/share/vfBeQrzIq3K4UB22'


def get_playlist_m3u8_url(url):
    resp=requests.get(url)
    obj=re.compile(r'var playlist.*?"url":"(?P<m3u8_url>.*?)"}',re.S)
    m3u8_url_playlist=obj.search(resp.text).group('m3u8_url')
    m3u8_url_playlist #/20220218/5TQqukCg/2000kb/hls/index.m3u8
    return m3u8_url_playlist;


def download_m3u8_file(m3u8_url):
    resp=requests.get(m3u8_url);
    with open('测试_m3u8.txt',mode='w',encoding='utf-8') as f:
        f.write(resp.text)
    print('测试_m3u8.txt下载完成')


async def ts_download(ts_url,name,session):
    '''下载ts文件'''
    async with session.get(ts_url) as resp:
        async with aiofiles.open(f'测试/{name}',mode='wb') as f:
            await f.write(await resp.content.read())
            print(name)

    print(f'{name}下载完毕');


async def aio_download(up_url):
    tasks=[]
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('测试_m3u8.txt',mode='r',encoding='utf-8') as f:
            async for line in f:
                if not line.startswith('#'):
                    line=line.strip();
                    ts_url = up_url +line;
                    name=line.split('/')[-1]
                    #开始封装一个一个的下载任务
                    task=asyncio.create_task(ts_download(ts_url,name,session))
                    tasks.append(task)
            await asyncio.wait(tasks)


def merge_ts():
    name_list=[]
    with open('测试_m3u8.txt',mode='r',encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                line=line.strip();
                name=line.split('/')[-1]
                ts_name=name
                name_list.append(ts_name)
        s="+".join(name_list)
        os.system(f'copy \b {s} 测试.mp4');

def main(main_url):
    main_src=get_iframe_src(main_url);
    #获取视频连接的m3u8;
    m3u8_url_playlist=get_playlist_m3u8_url(main_src)
    #拼接地址
    domain=main_src.split('/share')[0]
    #domain  https://ukzy.ukubf2.com
    m3u8_url_playlist=domain+m3u8_url_playlist
    # m3u8_url_playlist https://ukzy.ukubf2.com/20220218/5TQqukCg/2000kb/hls/index.m3u8
    #下载m3u8文件
    download_m3u8_file(m3u8_url_playlist)

    #读取m3u8文件下载一个一个的视频
    #m3u8文件中都是相对地址 需要我们手动拼接
    up_url=domain
    asyncio.run(aio_download(up_url))

    #合并视频

    merge_ts();
if __name__ == '__main__':
    url='http://www.jsjylh.com/vloge/175221-1-1.html'
    main(url)