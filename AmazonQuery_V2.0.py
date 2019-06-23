import requests
from lxml import html
import time
page = 1
KEYWORD="page"
ANIS="B005R9U1NK"
class AmazonQuery():
    def query(self,KEYWORD,ANIS):
        while True:
            global page
            if page > 4:    #大于4页不再查询
                print("p.4+")
                return
            payload = {'k': KEYWORD, '__mk_zh_CN': '亚马逊网站', 'ref': 'nb_sb_noss', 'page': page}
            r = requests.get("https://www.amazon.com/s", params=payload, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'      #伪装浏览器获取页面
                            '75.0.3770.100 Safari/537.36'})
            tree1 = html.etree
            tree = tree1.HTML(r.text)    #将获取的页面数据封装
            ranking = tree.xpath("//div[@data-asin=\'" + ANIS + "\']/@data-index")
            if ranking == []:   #没有数据就下一页
                page += 1
            else:
                for i in ranking:
                    print("P.%d"%(page))
                    return

if __name__ == '__main__':
    Amazon = AmazonQuery()
    Amazon.query("pagetage","B0059U1NK")