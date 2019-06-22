from selenium import webdriver
from tkinter import *
from selenium.webdriver.chrome.options import Options
# url = "https://www.amazon.com/"
# ANIS = "B00J8G96JS"
# KEYWORD = "grip tape" #测试数据
class AmazonQuery():
    def __init__(self):
        # service_args = []
        # service_args.append('--load-images=no')  ##关闭图片加载
        # service_args.append('--disk-cache=yes')  ##开启缓存
        # service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
        # self.dr = webdriver.PhantomJS(service_args = service_args)
        # chrome_options = Options()
        # # 无头模式启动
        # chrome_options.add_argument('--headless')
        # # 谷歌文档提到需要加上这个属性来规避bug
        # chrome_options.add_argument('--disable-gpu')
        # # 初始化实例
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # self.dr = webdriver.Chrome(options=chrome_options)
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        self.dr = webdriver.Chrome()
        top = Tk()
        top.title("亚马逊商品查询")
        labelframe = LabelFrame(top, width=240, height=200)
        labelframe.grid(column=0, row=0, rowspan=8, padx=8, pady=8)
        labelframe1 = LabelFrame(labelframe, text="商品信息", width=280, height=280)
        labelframe1.grid(column=7, row=0, rowspan=1, padx=1)
        commit = Button(labelframe1, text='查询', font=('宋体', '12'),command=self.start)
        commit.grid(column=1, row=8, padx=0, pady=2)
        #两个文本框
        self.t2 = Text(labelframe1, width=27, height=1)
        self.t2.grid(column=1, row=0, columnspan=1, rowspan=2)
        self.t3 = Text(labelframe1, width=27, height=1)
        self.t3.grid(column=1, row=5, columnspan=1, rowspan=2)
        # self.var1 = StringVar()
        # self.entry1 = Entry(labelframe1, width=27, textvariable='var1').grid(column=1, row=0, padx=12, pady=8, sticky=W)
        # self.var2 = StringVar()
        # entry2 = Entry(labelframe1, width=27, textvariable='var2').grid(column=1, row=5, padx=12, pady=12,sticky=W)
        button1_text = Button(labelframe1,command =self.clearANIS, text='清除', font=('宋体', '12'))
        button1_text.grid(column=3, row=0, padx=10, pady=8)
        button2_text = Button(labelframe1, command=self.clearKEYWORD, text='清除', font=('宋体', '12'))
        button2_text.grid(column=3, row=5, padx=8, pady=8)
        label4 = Label(labelframe1, text="ANIS").grid(row=0, padx=2)
        label5 = Label(labelframe1, text="KEYWORD").grid(row=5, padx=2)
        labelframe2 = LabelFrame(labelframe, text="执行信息")
        labelframe2.grid(column=0, row=0, padx=8, sticky=N)
        self.t1 = Text(labelframe2, width=50, height=20)
        self.t1.grid(column=0, row=0, columnspan=2, rowspan=6)  #
        # label6 = Label(labelframe2, text="").grid(column=2, row=1)
        # label6 = Label(labelframe2, text="").grid(column=2, row=2)
        # label6 = Label(labelframe2, text="").grid(column=2, row=3)
        button3_text = Button(labelframe2, command= self.clearBig,text='清除', width=4, font=('宋体', '12'))
        button3_text.grid(column=2, row=0)
        button3_text = Button(labelframe2, text='DOWN', width=4, font=('宋体', '12'))
        button3_text.grid(column=2, row=5)
        # Stepbar = Scrollbar(self.t1)
        # Stepbar.pack(side=RIGHT, fill=Y)
        # self.BugStep = Text(self.t1, width=70, height=20).pack(side=LEFT)
        top.mainloop()
    def clearBig(self):
        self.t1.delete('1.0','end')
    def clearANIS(self):
        self.t2.delete('1.0','end')
    def clearKEYWORD(self):
        self.t3.delete('1.0', 'end')
    def start(self):
        try:
            current =self.dr.current_url
        except:
            self.dr = webdriver.Chrome()
        ANIS = self.t2.get('0.0',END)
        KEYWORD = self.t3.get('0.0',END)
        self.input(ANIS,KEYWORD)
    def input(self, ANIS, KEYWORD):
        ANIS= ANIS.strip()
        if (ANIS == ""):
            self.t1.insert('insert','ANIS不能为空！\n')
            print('ANIS不能为空！')
            return
        KEYWORD = KEYWORD.strip()
        if (KEYWORD == ""):
            self.t1.insert('insert','KEYWORD不能为空！\n')
            print('KEYWORD不能为空！')
            return
        print(ANIS,KEYWORD)
        self.t1.insert('insert','%s %s\n'%(ANIS,KEYWORD))
        self.query(ANIS, KEYWORD)
    def query(self, ANIS, KEYWORD):
        print("开始查询...")
        self.t1.insert('insert','开始查询...\n')
        # js = "window.open('https://www.amazon.com/s?k=' + KEYWORD + '&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&ref=nb_sb_noss');"
        # self.dr.execute_script(js)
        self.dr.get(
            "https://www.amazon.com/s?k=" + KEYWORD + "&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&ref=nb_sb_noss")
        self.dr.implicitly_wait(4)  ##设置超时时间
        self.dr.set_page_load_timeout(4)  ##设置超时时间
        self.catch(ANIS, KEYWORD)
    def catch(self, ANIS, KEYWORD):
        count = 1
        while True:
            try:
                # el = self.dr.find_element_by_css_selector("body>div#a-page>div#search>div.sg-row"
                #     + ">div"
                #     + ">div.sg-col-inner>span[data-component-type='s-search-results']>"
                #     + "div>div[data-asin=" + ANIS + "]")
                el = self.dr.find_element_by_css_selector("div[data-asin=" + ANIS + "]")
                break
            except:
                # self.t1.insert('insert',"第%d页没有此商品,开始下一页->\n" % (count))
                print("第%d页没有此商品,开始下一页->" % (count))
                count += 1
                try:
                    nextPage = self.dr.find_element_by_partial_link_text("下一页").click()
                except:
                    self.t1.insert('insert','没有此商品！')
                    self.t1.insert('insert','-----------\n')
                    print('没有此商品！')
                    print('-----------\n')
                    return
        self.t1.insert('insert',"查询结果：\n")
        self.t1.insert('insert',"查询到商品%s第%d页排名:%d\n" % (ANIS, count, int(el.get_attribute("data-index"))+1))
        self.t1.insert('insert',"-----------\n")
        print("查询结果：\n")
        print("查询到商品%s第%d页排名:%d\n" % (ANIS, count, int(el.get_attribute("data-index"))+1))
        print("-----------\n")
    def __del__(self):
        print("退出")
        self.dr.quit()
if __name__ == '__main__':
    Amazon = AmazonQuery()

