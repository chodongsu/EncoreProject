import email
import os
from difflib import SequenceMatcher
from datetime import datetime 
import csv

encode_ex = ['euc-kr', 'shift-jis', 'uft-8', 'iso-8859-1', 'us-ascii']


def how_similar(ele, benchmark):
    if ele[0] == 'x':
        return 1+SequenceMatcher(a=ele, b=benchmark).ratio()
    else:
        return SequenceMatcher(a=ele, b=benchmark).ratio() 


def run():
    path = 'contest/data/eml/'
    listing = os.listdir(path)
    count = 0
    print(datetime.now())
    header_info = []
    for fle in listing:
        #time.sleep(1)
        if str.lower(fle[-3:])=="eml":
            count +=1

            encode = 'utf8'
            file = open(path+fle ,encoding='utf8',errors= 'ignore')
            msg=email.message_from_file(file)
            header=dict(msg._headers)

            temp_list = list(header.keys())

            for i in header.keys():
                if i not in header_info:
                    header_info.append(i)
            
            if count % 1000 == 0:
                print(count)
                print(datetime.now())
            file.close()
    standard = 'abcdefghijklmnopqrstuvwxyz'
    header_all = sorted(header_info, key= lambda x:how_similar(x.lower(),standard))
    return header_all
