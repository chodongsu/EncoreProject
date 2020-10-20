import os
import collections
import email
import csv

path = 'C:/Users/USER/Desktop/k-시큐리티(비정상 이메일)/eml/'

# listing = ['0000bfff-4a6e-4e40-9a36-3a4b9d1f5a67.eml']

listing = os.listdir(path)[:1000]
count = 0

header_dict = dict()

for fle in listing:
    count += 1  
    with open(path+fle,'r',encoding='utf-8',errors='ignore') as f:
        msg=email.message_from_file(f)
        msg_header = dict(msg._headers) # 헤더 딕셔너리화
        
        print(fle)
        print(count)

        for key,value in msg_header.items(): # 헤더이름 별로 값을 리스트 묶어서 만들어줌 
            
            try:
                header_dict[key].append(value)
                
            except:  # 새로운 헤더이름이 나왔을 때 실행
                header_dict[key] = [value]

# print(header_dict)

for key in header_dict: # counter 함수 활용
    header_dict[key] = collections.Counter(header_dict[key])
    header_dict[key] = header_dict[key].most_common(3) # top3 출력

output_file_name = "eml_head_count.csv"

with open('head_count_2.csv','w',encoding='utf8',newline='') as f:
    csvwriter = csv.writer(f)
    for key , value in header_dict.items():
        csvwriter.writerow((key,value))
