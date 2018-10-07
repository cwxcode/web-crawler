# -*-coding:utf-8-*-
import  urllib2  # 在python2中使用
#import urllib.request  # 在python3中使用
#import urllib.error  # 在python3中使用
from lxml import etree
import os
"""
第一步: 从 http://www.nvshens.com/rank/sum/ 开始抓取MM点击头像的链接(注意是分页的)
第二步：http://www.nvshens.com/girl/21751/ 抓取每一个写真集合的链接(注意是分页的)
第三步：http://www.nvshens.com/g/19671/1.html 在写真图片的具体页面抓取图片(注意是分页的)
"""
 
web_0 = "http://www.nvshens.com/"  # 要爬虫的网址
web_1 = "https://www.nvshens.com/rank/hunxue/"  # 起始网址

savepath = "./download_07/"  # 保存图片地址
isExists=os.path.exists(savepath)
if not isExists:
    os.makedirs(savepath)
    
timeset = 1  # 延时

#count = 0  # 爬虫图片数量
 
# javascript:alert(navigator.userAgent) 获得浏览器User-agent  防止出现反爬虫，可以用设置header或者代理等方式
#user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
header = {
            "User-Agent": user_agent,  # http的头域
            "Connection": "keep-alive",
         }
 
"""
从起始页面 http://www.nvshens.com/rank/sum/ 开始获取排名的页数和每一页的url
"""
def  mmRankSum():
    pages = web_1
    try:
        req = urllib2.Request(web_1, headers=header)
        html = urllib2.urlopen(req, timeout=timeset)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        
        #首先获取页码数,然后用循环的方式挨个解析每一个页面
        pages = htmlpath.xpath('//div[@class="pagesYY"]/div/a/@href')
        
        for i in range( len(pages)  ):  # 为什么减 2 ？？  获取第一页的链接少了吗,只获取了2/3/4.htm  ？？
            pagesitem=web_1 + pages[i]
            mmRankitem(pagesitem)  # 如 https://www.nvshens.com/rank/sum/3.html
            
    except Exception:
        pass       
        
 
"""
参数 url : 分页中每一页的具体url地址
通过传过来的参数，使用  lxml和xpath 解析 html，获取每一个MM写真专辑页面的url
"""
def mmRankitem(url):
    try:
        req = urllib2.Request(url, headers=header)
        html = urllib2.urlopen(req, timeout=timeset)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        pages = htmlpath.xpath('//div[@class="rankli_imgdiv"]/a/@href')
        for i in range(len(pages)):
            print  (web_0 + pages[i]+"album/")  # album 专辑 例如 https://www.nvshens.com/girl/21751/album/
            getAlbums(web_0 + pages[i]+"/album/")
    except Exception:
        pass
 
 
"""
参数 url : 每一个MM专辑的页面地址
通过传过来的参数，获取每一个MM写真专辑图片集合的地址
"""
def getAlbums(girlUrl):
    try:
        req = urllib2.Request(girlUrl, headers=header)
        html = urllib2.urlopen(req, timeout=timeset)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        pages = htmlpath.xpath('//div[@class="igalleryli_div"]/a/@href')
        for i in range(len(pages)):
            getPagePicturess(web_0 + pages[i])  # 如 https://www.nvshens.com/g/20169/
    except Exception:
        pass      
 
 
"""
参数 url : 每一个MM写真专辑图片集合的地址
通过传过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址
"""
def getPagePicturess(albumsurl):
    try:
        req = urllib2.Request(albumsurl, headers=header)
        html = urllib2.urlopen(req, timeout=timeset)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        pages = htmlpath.xpath('//div[@id="pages"]/a/@href')  
        for i in range(len(pages)):  # 为什么减2 ？？？
            savePictures(web_0 + pages[i])  # 如 https://www.nvshens.com/g/20169/3.html
    except Exception:
        pass 
 
    
"""
参数 url : 每一个MM写真专辑图片集合的地址(经过分页检测)
通过传过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。
"""
def savePictures(itemPagesurl):
    header = {
        "User-Agent": user_agent,
         "Connection": "keep-alive"
        , "Referer": "image / webp, image / *, * / *;q = 0.8"
        , "Accept":"image/webp,image/*,*/*;q=0.8"
    }
    pages = itemPagesurl  # 先声明pages
    try:
        req = urllib2.Request(itemPagesurl, headers=header)
        html = urllib2.urlopen(req, timeout=timeset)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
#        print (itemPagesurl)  # 打印
        pages = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')
        names = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt')
    except Exception:
        pass
    for i in range(len(pages) ):
        print (pages[i])  # 打印  如 https://www.nvshens.com/img.html?img=https://img.onvshen.com:85/gallery/21751/20169/007.jpg

        try:
 
            headers = {
                "User-Agent": user_agent,
                 "Connection": "keep-alive"
                , "Referer": pages[i]
            }
            req = urllib2.Request(pages[i], headers=headers)
 
            urlhtml = urllib2.urlopen(req, timeout=timeset)  # 连接被远端重置，需要降低请求频率，或者用多个代理
 
            respHtml = urlhtml.read()
 
            binfile = open(savepath + '%s.jpg' % ( names[i] ) , "wb")
            binfile.write(respHtml);
            binfile.close();
            print (names[i])  # 打印
#            global count
#            count += 1
        except Exception :
            print('pass ' + str(i))  # 打印
            pass
 
 
mmRankSum()  # 执行
#print('Total:' + str(count))
print ('finish')