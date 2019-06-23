import requests
import xlwt
from lxml import html
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time
from fake_useragent import UserAgent
# KEYWORD=""""
# page
# grip tape
# grip tape cleaner
# ""
# ANIS="B01LY7572N"
DATASAVE = []

ThreadNum = 0
id = 1
#头文件数据
ua = UserAgent() #自动生成头文件方法
'''
    亚马逊查询类
'''
class AmazonQuery():
    def TempListSort(self,tempList):
        global DATASAVE
        #排序取排名最前的存入数组
        tempList.sort(key=(lambda x:x[3]))
        DATASAVE.append([tempList[0][0],tempList[0][1],tempList[0][2],
                         "P.%d N.%s"%(tempList[0][3],tempList[0][4])])
        #在文本框里显示
        UI.t1.insert(1.0, '%d %s   %s   P.%d N.%s\n' %
                     (tempList[0][0],tempList[0][1],tempList[0][2],tempList[0][3],tempList[0][4]))
        #打印在控制台
        print('%d %s   %s   P.%d N.%s\n' %
                     (tempList[0][0],tempList[0][1],tempList[0][2],tempList[0][3],tempList[0][4]))
    def createThead(self,ID,KEYWORD,ANIS):
        global DATASAVE
        print(ANIS,KEYWORD)
        TheadPool = []
        self.tempList = []  #临时列表
        self.page = 1
        self.count= 0
        AliveNum = 0    #已结束的线程个数
        try:
            while self.page <= 4:  # 查询四页
                time.sleep(0.3)
                th = threading.Thread(target=self.AmazonPageQuery, args=(ID,KEYWORD, ANIS, self.page,))
                self.page += 1
                TheadPool.append(th)
                # _thread.start_new_thread(self.AmazonPageQuery,(KEYWORD,ANIS,page))
            for th in TheadPool:
                th.start()  #开启线程

            while True:
                time.sleep(1)
                for i in TheadPool:
                    if i.is_alive() == False:
                        AliveNum +=1
                if AliveNum >= 4 :
                    break
                else:
                    AliveNum = 0
                    # threading.Thread.join(th)
            if self.tempList !=[] :
                self.TempListSort(self.tempList)
                return
                # th.join()
            # time.sleep(6)
            if self.count == 0:
                print("p.4+")
                DATASAVE.append([ID, ANIS,KEYWORD, "p.4+"])
                UI.t1.insert(1.0, '%d  %s  %s  p.4+\n' %(ID,ANIS, KEYWORD))
                # return
            # return
        except:
            print("线程启动错误")
            UI.t1.insert(1.0, '线程启动错误\n')
        finally:
            pass
    def AmazonPageQuery(self,ID,KEYWORD,ANIS,page): #爬取
        global ua,DATASAVE
        proxy ='163.204.241.6:9999'
        proxies ={                      #代理
            'http':'http://'+proxy,
            'https':'https://'+proxy,}
        payload = {'k': KEYWORD, '__mk_zh_CN': '亚马逊网站', 'ref': 'nb_sb_noss', 'page': page}  # 向服务器传参
        while True:
            # if self.count == 1:
            #     print("结束")
            #     return
            try:
                r = requests.get("https://www.amazon.com/s", headers={
                    'user-agent':ua.random},params=payload)
            except:
                print("网络被断开..重新请求")
                time.sleep(0.3)
                continue
            l = len(r.text)
            print(l)
            if l < 9999:
                print("网络地址不正确..重新请求")
                time.sleep(0.1)
                continue
            tree1 = html.etree
            tree = tree1.HTML(r.text)  # 将获取的页面数据封装
            ranking = tree.xpath("//div[@data-asin=\'" + ANIS + "\']/@data-index")
            if ranking != []:  #
                self.count = 1
                self.tempList.append([ID,ANIS,KEYWORD,page,ranking[0]])
                return
            else:
                return


'''
    UI界面类
'''
def set1_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4

    font.height = height
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    style.font = font
    # style.borders = borders
    return style
class UI():
    #初始化窗口
    def __init__(self):
        self.top = Tk()
        sw = self.top.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.top.winfo_screenheight()
        # 得到屏幕高度

        ww = 770
        wh = 310
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.top.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        self.top.title("亚马逊商品查询")
        self.top.protocol("WM_DELETE_WINDOW", self.callback)
        labelframe = LabelFrame(self.top, width=240, height=200)
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
        button3_text = Button(labelframe2, command=self.clearData, text='清除', width=4, font=('宋体', '12'))
        button3_text.grid(column=2, row=0)

        button5_text = Button(labelframe2, text='导出', width=4, font=('宋体', '12'),command=self.CreateExcel)
        button5_text.grid(column=2, row=5)
        self.top.mainloop()  #  #
    # 点击关闭按钮调用
    def callback(self):
        if messagebox.askokcancel("提示", "数据将不会保存，确定退出?"):
            self.top.destroy()
            exit("退出程序")
    #暂且无效
    def modified(self, event):
        UI.t1.see(END)
    # 清除文本框
    def clearBig(self):
        UI.t1.delete('1.0','end')
    def clearANIS(self):
        self.t2.delete('1.0','end')
    def clearKEYWORD(self):
        self.t3.delete('1.0', 'end')
    #查询
    def start(self):
        ANIS = self.t2.get('0.0',END)
        KEYWORD = self.t3.get('0.0',END)

        self.input(ANIS,KEYWORD)
    def input(self, ANIS, KEYWORD):
        global ThreadNum
        global id
        ANIS= ANIS.strip()
        if (ANIS == ""):
            UI.t1.insert(1.0,'ANIS不能为空！\n')
            print('ANIS不能为空！')
            return
        KEYWORD = KEYWORD.strip()
        if (KEYWORD == ""):
            UI.t1.insert(1.0,'KEYWORD不能为空！\n')
            print('KEYWORD不能为空！')
            return

        '''
            线程测试
        '''
        KeyList = KEYWORD.split("\n")
        # threading.Thread(target=self.Listening, args=(KeyList)).start()
        for Key in KeyList:
            Amazon = AmazonQuery()
            th =threading.Thread(target=Amazon.createThead, args=(id,Key.strip(), ANIS))
            th.setDaemon(True)
            th.start()
            time.sleep(0.5)
            ThreadNum+=1
            id+=1
            if ThreadNum >= 20 :
                time.sleep(20)
                ThreadNum = 0
        # l = len(KeyList)
        # while True:
        #     time.sleep(10)
        #     print(AmazonQuery.id)
        #     print(l)
        #     if AmazonQuery.id>= l:
        #
        #         messagebox.INFO('提示','查询完成！')
        #         break
        '''
            阻塞测试
        '''
        # KeyList = KEYWORD.split("\n")
        # if len(KeyList) > 20:
        #     for Key in KeyList:
        #         Amazon = AmazonQuery()
        #         th = threading.Thread(target=Amazon.createThead, args=(Key.strip(), ANIS))
        #         threadPool.append(th)
        #         ThreadNum+=1
        #         if ThreadNum >=20:
        #             for i in threadPool:
        #                 i.start()
        #             time.sleep(5)
        #             for i in threadPool:
        #                 i.join()            #等待线程完成
        #             ThreadNum = 0
        #         threadPool = []
        # else:
        #     for Key in KeyList:
        #         Amazon = AmazonQuery()
        #         th = threading.Thread(target=Amazon.createThead, args=(Key.strip(), ANIS))
        #         threadPool.append(th)
        #         for i in threadPool:
        #             th.start()
        #         for i in threadPool:
        #             th.join()


        print("\n加载完毕\n")
        UI.t1.insert(1.0,'加载完毕\n')
        # UI.t1.insert('insert', '查询结束')
    # def Listening(self,KeyList):
    #     global id
    #     l = len(KeyList)
    #     while True:
    #         time.sleep(10)
    #         if id >= l:
    #             UI.t1.insert(1.0,'查询完成\n')
    #             id = 1
    #             return
    #文本格式
    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        # borders= xlwt.Borders()
        # borders.left= 6
        # borders.right= 6
        # borders.top= 6
        # borders.bottom= 6
        style.font = font
        # style.borders = borders
        return style
    #清除所有数据
    def clearData(self):
        global DATASAVE,id
        if messagebox.askokcancel("提示", "清空数据？"):
            DATASAVE = []
            id = 1
            self.clearBig()
    #创建xls文件
    def CreateExcel(self):
        global DATASAVE
        try:
            self.DATASAVESort()
            print(DATASAVE)
            fname = filedialog.asksaveasfilename(
                title=u'导出表格', filetypes=[('Xls', '.xls')],initialdir='./',initialfile=DATASAVE[0][1]+'商品分析表')
        except:
            messagebox.showwarning("提示","没有数据可导出！")
            return
        f = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
        '''
        创建第一个sheet:
            sheet1
        '''
        timeM =time.strftime("%Y/%m/%d", time.localtime())
        sheet1 = f.add_sheet('sheet1')  # 创建sheet
        row0 = ['ID', 'ASIN', 'KEYWORD', '排名']
        #设置第一行每个格宽度
        # 生成第一行
        for i in range(0, len(row0)):
            col = sheet1.col(i)
            col.width = 256 * 20
            sheet1.write(0, i, row0[i],set1_style('宋体', 220,True))#第一行
        sheet1.col(2).width = 256*33

        for i in range(0, len(DATASAVE)):   #后面数据
            for j in range(0,len(DATASAVE[i])):
                sheet1.write(i+1, j, DATASAVE[i][j],set1_style('Times New Roman', 220,True))
        # f.save(DATASAVE[0][1]+'商品分析表.xls')
        f.save(str(fname)+'.xls')

        messagebox.showinfo("提示","导出成功！")
    def DATASAVESort(self):
        global DATASAVE
        DATASAVE.sort(key=(lambda x:x[0]))

if __name__ == '__main__':
    ui = UI()

