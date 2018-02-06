data=[];
school=[];
from bs4 import BeautifulSoup;
from urllib import request
import time;
import datetime;
import random;
import urllib.parse;
now=datetime.datetime.now();
#生成关键词
for s in school:
    for i in range(1985,2018):
        curkey='SQRQ:('+str(i)+')('+s+')AND SQR:('+s+') AND LeiXing:( FMSQ)';
        data.append(curkey);
filename=str(now.microsecond)+'.txt';#
file1=open(filename,'w');
file2=open('history.txt');
a=file2.read();
history=a.split('\n');
#history里面是已经爬过的所有信息
file3=open('history.txt','w');
file4=open('max.txt','w');
file3.write(a);
file3.write('\n');
condition1='权利转移';
condition2='许可备案';
need=['合同备案号','让与人','变更前权利人','变更后权利人','授权公告日','许可种类','备案日期','受让人'];
storename=['htbah','ryr','bgqqlr','bghqlr','sqggr','rkzl','barq','srr'];
pat="";

def getNum(gen):
    i=0;
    for a in gen:
        if i==0:
            ccc=a;
            i=i+1;
        else:
            return ccc+a;
    return;
def get(dom,tt):
    time.sleep(1.2+random.uniform(0,1));
    global pat;
    par=dom.parent.parent;
    patNum=getNum(par.select('td')[2].strings);
    pos=patNum.find('.');
    patNum=patNum[0:pos];
    print(patNum);
    if pat==patNum:
        return;
    pat=patNum;
    result={};
    result['zlh']=pat;
    result['type']=tt;
    result['fmmc']=par.select('td a')[0].string;
    result['fmr']=par.select('td')[5].string;
    result['sqr']=par.select('td a font')[0].string;
    result['sqrq']=par.select('td font')[1].string;
    curUrl='http://www.soopat.com/Home/SipoLegal/'+pat;
    print(curUrl);
    curresponse=request.urlopen(curUrl);
    curpage=curresponse.read();
    curpage=curpage.decode('utf-8');
    cursoup=BeautifulSoup(curpage,'html.parser');
    message=cursoup.select('tr td[colspan=3]');
    whole_message=[];
    for m in message:
        for mm in m.stripped_strings:
            whole_message.append(mm);
            if mm=='授权':
                flag=False;
                for cursqrq in m.parent.parent.stripped_strings:
                    if flag:
                        result['sqrq']=cursqrq;
                        break;
                    if cursqrq=='法律状态公告日':
                        flag=True;
            if mm=='公开':
                flag=False;
                for curgkrq in m.parent.parent.stripped_strings:
                    if flag:
                        result['gkrq']=curgkrq;
                        break;
                    if curgkrq=='法律状态公告日':
                        flag=True;
            if mm=='专利申请权、专利权的转移':
                flag=False;
                for zyrq in m.parent.parent.stripped_strings:
                    if flag:
                        result['zyrq']=zyrq;
                        break;
                    if zyrq=='法律状态公告日':
                        flag=True;
    ff=False;
    for m in whole_message:
        pm=m.find(':');
        if pm!=-1:
            for i in range(0,len(need)):
                if need[i]==m[0:pm] and not storename[i] in result:
                    ff=True;
                    result[storename[i]]=m[pm+1:];
    if ff==False:
        for m in whole_message:
            pm=m.find(':');
            if pm!=-1:
                result['whole']=m;
                break;
    
    print(str(result));
    file1.write(str(result));
    file1.write('\n');
    return;

for curdata in data:
    if curdata in history:
        continue;
    print(curdata);
    first='http://www.soopat.com/Home/Result?SearchWord='+urllib.parse.quote(curdata)+'&PatentIndex=0&View=7';
    response=request.urlopen(first);
    page=response.read();
    page=page.decode('utf-8');
    soup=BeautifulSoup(page,'html.parser');
    if len(soup.select('p.right b'))==0:
        print('请打开链接',first);
        print('然后输入验证码');
        print('然后在终端中输入 \'python3.6 index.py\'即可');
        break;
    pagenum=int(int(soup.select('p.right b')[0].string)/30);
    file3.write(curdata);
    file3.write('\n');
    if pagenum>32:
        pagenum=32;
        file4.write(curdata);
        file4.write('\n');
    print(pagenum);
    time.sleep(3);
    for i in range(0,pagenum):
        time.sleep(2+random.uniform(0,2));
        first='http://www.soopat.com/Home/Result?SearchWord='+urllib.parse.quote(curdata)+'&PatentIndex='+str(i*30)+'&View=7';
        print(first);
        response=request.urlopen(first);
        page=response.read();
        page=page.decode('utf-8');
        soup=BeautifulSoup(page,'html.parser');
        item=soup.select('tbody tr.td_left');
        for k in item:
            check=k.select('td div');
            for j in check:
                if(j.string==condition1):
                    get(j,0);
                    break;
                if(j.string==condition2):
                    get(j,1);
                    break;

