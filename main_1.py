# -*- coding: utf-8 -*-
import requests
from requests import RequestException
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import os
 
start=11244  #起始图片ID，打开任何一个图集，链接最后的那一串数字，五位数。 24656
end=30000  #终止图片ID，起始初始建议间隔大一些，然后然他自动遍历搜索有效地址 25370
 
base_url='https://www.nvshens.com/g/'  #宅男女神美图图片专栏下的基本网址

savepath = "./download_11/"  # 保存图片地址
isExists=os.path.exists(savepath)
if not isExists:
    os.makedirs(savepath)
    
timeset = 10  # 延时
 
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    
headers1={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Upgrade-Insecure-Requests":"1",
"User-Agent":user_agent,
}
headers2={
'Accept':'image/webp,image/*,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
"If-None-Match":"ce118ca4a39cd31:0",
'User-Agent':user_agent,
}
 
def tes2_url(url):
    print('正在访问：' + url)
    try:#确保每一个requests都有异常处理
        response = requests.get(url, headers=headers1, timeout=timeset)
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.select('#htilte'):#是否有标题，判断该页面下是否有图片集
            url_true=url
            return url_true
        else:
            print('无效地址：' + url)
            pass
    except:
        pass
 
def url_jiexi(url_true):
    response = requests.get(url_true, headers=headers1, timeout=timeset)
    soup = BeautifulSoup(response.text, 'lxml')
    imglist = soup.find_all('img')
    try:
        title = soup.select_one('#htilte').text 
        imag_num = int(re.sub("\D", "", soup.select_one('#dinfo > span').text[:3]))#正则表达式获得具体数字
        imag_base = imglist[1].attrs['src'][:-5]
        print('title:' + title)
        print('image number:' + str(imag_num))  
        print('image base:' + imag_base)
        return (title,imag_num,imag_base)
    except:
        return None
    
def download_image(title,imag_base,i):
    imag_url=imag_base+str(i).zfill(3)+".jpg"
    print('正在下载：' + imag_url)#！！很重要，获得一个调制信息
    try:
        response = requests.get(imag_url, headers=headers2,timeout=timeset)
        print('status code:' + str(response.status_code))
        if response.status_code == 200:
            print("请求图片成功")
            save_image(response.content, title, i)
        else:
            pass
        return None
    except RequestException:
        print('请求图片出错：' + imag_url)
        return None
 
def save_image(content,title,i):#创建对应分类的文件夹，并且保存图片。
    dir_name_or=str(title.encode('utf-8'))[:100].strip()
    dir_name = re.sub("[\s+\.\!\/]+", "",dir_name_or)
    print(dir_name)
    file_path = savepath + dir_name.decode('utf-8') + '_%s.jpg' % ( str(i).zfill(3) )  # 要decode回来
    with open(file_path,'wb') as f:
        f.write(content)
    print("写入图片成功")
 
def main(i):
        url=base_url+str(i)
        url_true=tes2_url(url)
        if url_true:
            title, imag_num,imag_base =url_jiexi(url_true)
            for i in range(1, int(imag_num)):
                download_image(title,imag_base,i)
 
if __name__ == '__main__':
#    pool=Pool()
#    pool.map(main,[i for i in range(start,end)])
    for i in range(start,end):
        main(i)
    print('finish')