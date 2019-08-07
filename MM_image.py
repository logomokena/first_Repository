#-*- coding: utf-8 -*-
'''
@author:logomokena
@time:2019/08/05
@version:python3.7
'''
from requests_html import HTMLSession
import os

class get_img(object):

    #图片保存
    def save_data(self,link,image_page,folder_name):
        data = HTMLSession().get(link)
        #file_page = str(file_page)
        print(folder_name)
        with open(r"E:\MM_image"+os.sep+folder_name+os.sep+str(image_page)+".jpg","wb") as f_img:
            f_img.write(data.content)

    #创建文件夹
    def confirm_path(self,folder_name):
        if not os.path.exists(r"E:\MM_image\\"+folder_name):
            os.makedirs(r"E:\MM_image\\"+folder_name)


    #默认爬取方法(获取所有图库的url链接,并存储到.txt文件里面取)
    def parse(self,url):
        response = HTMLSession().get(url)
        links = response.html.xpath("//div[@class='w1000 box03']/ul[@class='product01']/li/a/@href",first=False)

        #获取图库名字
        foldernames = response.html.xpath("//div[@class='w1000 box03']/ul[@class='product01']/li/a/@alt",first=False)

        #获取url中的日期
        url_date = []
        datelist = response.html.xpath("//div[@class='w1000 box03']/ul[@class='product01']/li/a/@href")
        for i in datelist:
            url_date.append(i[:-10])

        # 将数据传给get_parse
        for i in range(0,20):
            page = 1
            # 创建存放图片的子文件夹
            print(foldernames[i],"：",links[i],"---->>",url_date[i])
            self.confirm_path(foldernames[i])
            self.get_parse(links[i],page,foldernames[i],url_date[i])

        #将链接写入.txt文件
#        with open(r"C:\Users\admin\Desktop\text.txt","a") as f:
#            for i in range(0,20):
#                print(foldernames[i],"：",links[i])
#                f.write(foldernames[i]+"："+links[i]+"\n")

        #获取下一页url链接
        next_url = response.html.xpath("//div[@class='w1000 box03']/div[@class='page']/ul/li[contains(string(),'下一页')]/a/@href",first=False)
        while next_url:
            self.parse("https://www.169tp.com/wangyouzipai/"+next_url[0])

        #读取text.txt以获取链接
#        with open(r"C:\Users\admin\Desktop\text.txt","r") as fr:
#            links_read = fr.read()
#            links_new = list(links_read.split("\n"))
#            print("links_new:",links_new)
#            print(type(links_new))

    #图片url爬取，并将图片url传给save_data
    def get_parse(self,first_url,page,folder,link_date):
        #获取图片url的链接
        try:
            response = HTMLSession().get(first_url)
        except:
            print("获取图片链接失败！")
        #用xpath获取该响应内所有的图片链接
        links = response.html.xpath("//div[@class='w1280']/div[@class='in_banner']/div[@class='big-pic']/div[@class='big_img']/p/img/@src",first=False)
        print("page:",page,"links:",links)
        #调取save_data保存图片
        for link in links:
            print("*"*5,link,":",folder,"*"*5)
            self.save_data(link,page,folder)
            page+=1
        #获取下页链接
        next_link = response.html.xpath("//div[@class='w1280']//div[@class='big-pic']/div[@class='dede_pages']/ul/li[contains(string(),'下一页')]/a/@href",first=False)
#        next_linking = str(next_link[0])
        print("next_link:",next_link)
#        print("next_link[0]",next_link[0])
#        print(type(next_link))
#        print(next_link.index('43673_2.html'))
        print("len:",len(next_link))
        if not next_link[0]=="#":
            self.get_parse(link_date+next_link[0],page,folder,link_date)


def main():
    url = "https://www.169tp.com/wangyouzipai/"
    image = get_img()
    image.parse(url)

def amain():
    url = "https://www.169tp.com/wangyouzipai/2019/0420/43673.html"
    image = get_img()
    image.get_parse(url,1,"小萝莉闺房养眼自拍")

main()
