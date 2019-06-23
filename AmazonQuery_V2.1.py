import requests
from lxml import html
import threading
from tkinter import *
import time
# KEYWORD=""""
# page
# grip tape
# grip tape cleaner
# ""
# ANIS="B01LY7572N"
'''
    亚马逊查询类
'''
class AmazonQuery():

    def createThead(self,KEYWORD,ANIS):
        TheadPool = []
        self.page = 1
        self.count = 0
        try:
            while self.page <= 4: #查询四页
                th = threading.Thread(target=self.AmazonPageQuery, args=(KEYWORD,ANIS,self.page))
                TheadPool.append(th)
                # _thread.start_new_thread(self.AmazonPageQuery,(KEYWORD,ANIS,page))
                self.page+=1
            for th in TheadPool:
                th.start()
            for th in TheadPool:
                threading.Thread.join(th)
            if self.count == 0:
                print("p.4+")
                UI.t1.insert('insert', '%s  %s  p.4+\n' %(ANIS, KEYWORD))
        except:
            print("线程启动错误")
    def AmazonPageQuery(self,KEYWORD,ANIS,page):
        # print("线程启动")
        payload = {'k': KEYWORD, '__mk_zh_CN': '亚马逊网站', 'ref': 'nb_sb_noss', 'page': page } #向服务器传参
        # r = requests.get("https://www.amazon.com/s", params=payload, headers={
        #     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
        #                  '507.36 (KHTML, like Gecko) Chrome/74.0.3770.100 Safari/507.36'})
        r = requests.get("https://www.amazon.com/s", params=payload, headers={
            'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
        tree1 = html.etree
        tree = tree1.HTML(r.text)  # 将获取的页面数据封装
        ranking = tree.xpath("//div[@data-asin=\'" + ANIS + "\']/@data-index")
        if ranking != []:  # 没有数据就下一页
            for i in ranking:
                print("P.%d 排名:%s" % (page, i))
                UI.t1.insert('insert', '%s   %s   P.%s N.%s\n' % (ANIS, KEYWORD, page, i))
                self.count += 1
                # return
        else:
            print("此页没有")

'''
    UI界面类
'''
class UI():
    def __init__(self):
        top = Tk()
        top.title("亚马逊商品查询")
        labelframe = LabelFrame(top, width=240, height=200)
        labelframe.grid(column=0, row=0, rowspan=8, padx=8, pady=8)
        labelframe1 = LabelFrame(labelframe, text="商品信息", width=280, height=280)
        labelframe1.grid(column=7, row=0, rowspan=1, padx=1)
        commit = Button(labelframe1, text='查询', font=('宋体', '12'), command=self.start)

        commit.grid(column=1, row=8, padx=0, pady=2)
        # 两个文本框
        self.t2 = Text(labelframe1, width=27, height=1)
        self.t2.grid(column=1, row=0, columnspan=1, rowspan=2) #ANIS框
        self.t3 = Text(labelframe1, width=27, height=15)  #KEYWORD框
        self.t3.grid(column=1, row=5, columnspan=1, rowspan=2)
        button1_text = Button(labelframe1, command=self.clearANIS, text='清除', font=('宋体', '12'))
        button1_text.grid(column=3, row=0, padx=10, pady=8)
        button2_text = Button(labelframe1, command=self.clearKEYWORD, text='清除', font=('宋体', '12'))
        button2_text.grid(column=3, row=5, padx=8, pady=8)
        label4 = Label(labelframe1, text="ANIS").grid(row=0, padx=2)
        label5 = Label(labelframe1, text="KEYWORD").grid(row=5, padx=2)
        labelframe2 = LabelFrame(labelframe, text="执行信息")
        labelframe2.grid(column=0, row=0, padx=8, sticky=N)
        UI.t1 = Text(labelframe2, width=50, height=20)
        UI.t1.grid(column=0, row=0, columnspan=2, rowspan=6)  #
        button3_text = Button(labelframe2, command=self.clearBig, text='清除', width=4, font=('宋体', '12'))
        button3_text.grid(column=2, row=0)
        button3_text = Button(labelframe2, text='DOWN', width=4, font=('宋体', '12'))
        button3_text.grid(column=2, row=5)
        top.mainloop()
    def clearBig(self):
        UI.t1.delete('1.0','end')
    def clearANIS(self):
        self.t2.delete('1.0','end')
    def clearKEYWORD(self):
        self.t3.delete('1.0', 'end')
    def start(self):
        ANIS = self.t2.get('0.0',END)
        KEYWORD = self.t3.get('0.0',END)

        self.input(ANIS,KEYWORD)
    def input(self, ANIS, KEYWORD):
        ANIS= ANIS.strip()
        if (ANIS == ""):
            UI.t1.insert('insert','ANIS不能为空！\n')
            print('ANIS不能为空！')
            return
        KEYWORD = KEYWORD.strip()
        if (KEYWORD == ""):
            UI.t1.insert('insert','KEYWORD不能为空！\n')
            print('KEYWORD不能为空！')
            return

        treadPool = []
        UI.t1.insert('insert', '开始查询...\n')
        # for Key in KEYWORD.split("\n"):
        #     Amazon = AmazonQuery()
        #     print(Amazon)
        #     time.sleep(1)
        #     threading.Thread(target=Amazon.createThead, args=(Key.strip(), ANIS)).start()
        for i in range(50):
            Amazon = AmazonQuery()
            # print(Amazon)
            time.sleep(2)
            print(ANIS,KEYWORD)
            print(threading.Thread(target=Amazon.createThead, args=(KEYWORD.strip(), ANIS)).start())
            print("线程数：", threading.active_count())
        #     # UI.t1.insert('insert', '%s %s\n' % (ANIS,Key.strip()))
        #     # Amazon.createThead(Key.strip(), ANIS)

        print("线程数：", threading.active_count())
        UI.t1.insert('insert', '查询结束')
if __name__ == '__main__':
    # Amazon = AmazonQuery()
    ui = UI()

