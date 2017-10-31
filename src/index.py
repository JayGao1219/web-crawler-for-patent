data=[];
school=['北京大学', '北京工业大学', '北京科技大学', '北京理工大学', '北京师范大学', '北京邮电大学', '东北农业大学', '哈尔滨工业大学', '合肥工业大学', '华南师范大学', '暨南大学', '辽宁大学', '南京大学', '南京理工大学', '宁夏大学', '清华大学', '上海交通大学', '石河子大学', '四川大学', '太原理工大学', '天津医科大学', '同济大学', '西北大学', '西北工业大学', '西北农林科技大学', '西藏大学', '中国地质大学', '中国矿业大学 （徐州）', '中国政法大学', '安徽大学', '北京航空航天大学', '北京化工大学', '北京交通大学', '北京林业大学', '北京中医药大学', '大连海事大学', '大连理工大学', '电子科技大学', '东北大学', '东北林业大学', '东北师范大学', '东华大学', '东南大学', '福州大学', '复旦大学', '广西大学', '哈尔滨工程大学', '海南大学', '河北工业大学', '河海大学', '湖南大学', '湖南师范大学', '华北电力大学', '华东理工大学', '华东师范大学', '华南理工大学', '华中科技大学', '华中农业大学', '华中师范大学', '吉林大学', '江南大学', '兰州大学', '南昌大学', '南京航空航天大学', '南京农业大学', '南京师范大学', '南开大学', '内蒙古大学', '青海大学', '厦门大学', '山东大学', '陕西师范大学', '上海大学', '四川农业大学', '苏州大学', '天津大学', '武汉大学', '武汉理工大学', '西安电子科技大学', '西安交通大学', '西南大学', '西南大学', '西南交通大学', '新疆大学', '延边大学', '云南大学', '长安大学', '浙江大学', '郑州大学', '中国海洋大学', '中国科学技术大学', '中国矿业大学（北京）', '中国农业大学', '中国人民大学', '中国石油大学（北京）', '中国石油大学（华东）', '中国药科大学', '中南大学', '中山大学', '重庆大学', '贵州大学'];
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

