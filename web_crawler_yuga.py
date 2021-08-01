# -*-coding: utf-8 -*-
import os
import re
import sys
import json
import requests
import argparse
import time
import codecs
from io import open
from bs4 import BeautifulSoup
from six import u


#清空原本json檔案
f = open('output.json','r+')
f.truncate()


#登入已滿18頁面
payload = {'from':'/bbs/Gossiping/index.html','yes':'yes'}
url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',data=payload)

count = 0
page = 0
push_content = []




#擷取40筆PO文
while count < 40:
    res = rs.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    articles = soup.find_all('div', 'r-ent')#搜尋<div class='r-ent'>的資料(list)

    nextpageurl = 'https://www.ptt.cc'+soup.find_all(attrs = {'class':'btn wide'})[1]['href']#下一頁以及上一頁url
    
    for article in articles:#從搜尋到的文章資料一筆一筆處理
        count += 1#已處理PO文數
        if count > 40:
            break

        #基本資料蒐集: 標題、作者、內文連結
        meta = article.find('div', 'title')
        title = meta.getText().strip()
        if('(本文已被刪除)' in title):
            break
        link = meta.find('a')['href']
        date = article.find('div', 'date').getText()
        author = article.find('div', 'author').getText()
        article_id = link.replace('/bbs/Gossiping/','').replace('.html','')
       
        #蒐集內文資料
        contenturl = "https://www.ptt.cc" + link
        res = rs.get(contenturl)
        soup = BeautifulSoup(res.text, 'lxml')

        main_content = soup.find(id="main-content")
        metas = main_content.select('div.article-metaline')
        
        #去除main_content中非內文部分
        for meta in metas:
            meta.extract()
        for meta in main_content.select('div.article-metaline-right'):
            meta.extract()
        pushes = main_content.find_all('div', class_='push')
        for push in pushes:
            push.extract()
        try:
            ip = main_content.find(text=re.compile(u'※ 發信站:'))
            ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ip).group()
        except:
            ip = "None"
        filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
        expr = re.compile(u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, '', filtered[i])

        filtered = [_f for _f in filtered if _f]  # remove empty strings
        filtered = [x for x in filtered if article_id not in x]  # remove last line containing the url of the article

        #蒐集留言(存入list)    
        for push in pushes:
            push_content.append(push.find('span','push-content').get_text().encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
        
        
        #蒐集內文
        content = ' '.join(filtered)
        content = re.sub(r'(\s)+', ' ', content)
       

        

        #將蒐集到的資料儲存成json格式
        data = {'number':count,
                'author':author,
                'title':title,
                'content':content,
                'comment':push_content
                }

        #印出資料、儲存至json
        with open('output.json', 'a',encoding = 'utf8')as f:
            json.dump(data,f, ensure_ascii=False,indent = 4, separators=(',', ': '))
        f.close()
        print("count:",count,":",title, date, author)  # result of setp-3
        print(content)
        
       
        push_content = []
    url = nextpageurl
    page+=1
    print("================page ",page,' ===================')
        

   
        

