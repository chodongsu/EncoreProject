import os
import collections
import email
import csv

path = 'C:/Users/USER/Desktop/k-시큐리티(비정상 이메일)/eml/'
# path = 'contest_sample/sampledata/'


# listing = ['0000bfff-4a6e-4e40-9a36-3a4b9d1f5a67.eml']

listing = os.listdir(path)
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
    header_count = collections.Counter(header_dict[key])
    header_dict[key] = (len(set(header_dict[key])) , len(header_dict[key]), [(i ,header_count[i]) for i in header_count if header_count[i] > 10 ] )

print(header_dict)
    # header_dict[key] = header_dict[key].most_common(3) # top3 출력

output_file_name = "heaer_count_3.csv"

with open(output_file_name,'w',newline='', encoding='utf8') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(('header_name', 'count_unique', 'count_entire', 'freq_appear'))
    for key , (value1, value2, value3)in header_dict.items():
        csvwriter.writerow((key,value1, value2, value3))