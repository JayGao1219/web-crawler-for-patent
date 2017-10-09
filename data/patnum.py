import json;
import re;
import urllib;
name=64;
file2=open('result.txt','w');
result=[];
for i in range(0,8):
    name=name+1;
    openfile=chr(name)+".txt";
    file1=open(openfile);
    while 1:
        line=file1.readline();
        if not line:
            break;
        m=re.match(r'[A-H]\d{2}[A-Z]',line);
        if m:
            cur=m.group();
            if cur not in result:
                result.append(cur);
            else:
                pass;
        else:
            pass;

file2.write('[');
for i in result:
    file2.write('\'');
    file2.write(i);
    file2.write('\',');

file2.write(']');

