import email
import os
from email.header import decode_header
import quopri
import time
from datetime import datetime 
from difflib import SequenceMatcher
import base64
import re
from bs4 import BeautifulSoup
import csv
import create_header as create_head
import warnings


# Beautifulsoup warning 무시
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


# encode 정보 예시 (encode 정보가 잘못 기재된 파일의 encode 정보를 불러오기 위함)
encode_ex = ['euc-kr', 'shift-jis', 'uft-8', 'iso-8859-1', 'us-ascii']

# output 파일인 csv 형식을 준비함
output_file_name = 'contest/n_eml_parse_final.csv'
output_file = open(output_file_name, 'w', encoding='utf8', newline='')

# header를 dictionary로 변환했을때 key 값들을 미리 리스트로 지정해둠.
header_col_names= create_head.run()

# csv의 column 값들을 지정하고 입력
main_col_names=['text_without_tag','include_url','num_of_imgs']
csv_col_names = ['file_name'] + header_col_names + main_col_names
csvwriter = csv.writer(output_file)
csvwriter.writerow(csv_col_names)

# data를 불러올 경로 설정
path = 'contest/data/eml/'
listing = os.listdir(path)
count = 0

# eml 파일을 불러읽음
def open_file(f_encode, s_encode, th_encode):
    f = open(path+fle ,encoding=f_encode,errors= 'ignore')
    msg=email.message_from_file(f)
    f.close()
    #main_text 정보를 불러옴
    if type(msg._payload) is list:
        msg_body = str(msg.get_payload()[0])
    else:
        msg_body = str(msg.get_payload())
    try :
        a = bytes(msg_body, s_encode)
    except :
        a = bytes(msg_body, 'utf-8')
    msg_body = quopri.decodestring(a, header=False)
    return msg_body.decode(th_encode, errors='ignore')

# eml 파일의 encode 정보를 가져옴
def find_encode(anchor_index):
    encode_index = anchor_index+9
    encode_i=''
    run = True

    while run:
        encode_i += msg_header[encode_index]
        encode_index +=1
        if encode_index == len(msg_header)-1:
            encode_i = 'utf8'
            break
        if msg_header[encode_index] == '"':
            run = False
       
    return encode_i

# 미확인 encode의 경우, 기존에 저장해둔 encode 예시에서 제일 비슷한 encode로 바꿔줌
def change_unknown_encode(encode_i):
    encode = encode_i.lower()
    temp = [ SequenceMatcher(a=encode, b=k).ratio() for k in encode_ex ]
    temp_idx = temp.index(max(temp))
    return encode_ex[temp_idx]

# # base64에서 오류가 생길 경우, 정규식 처리 후 다시 인코딩 진행 
def padding(data):
    data += '=' * (len(data) % 4)
    return data
    

print(datetime.now())
# main_code
for fle in listing:
    csv_list = []
    if str.lower(fle[-3:])=="eml":
        csv_list.append(fle)
        count +=1
        unknown_encode = []
        if count %1000 ==0:
            print(count)
            print('to_csv:', datetime.now())
        # print(fle)

        ## encode 정보를 확인하기 위해 eml파일을 utf8 형식으로 불러옴
        encode = 'utf8'
        f = open(path+fle ,encoding='utf8',errors= 'ignore')
        msg=email.message_from_file(f)
        f.close()
        
        ## header의 정보들을 csv_list에 넣어줌
        msg_header = dict(msg._headers)
        for i in header_col_names:
            try:
                csv_list.append(msg_header[i])
            except:
                csv_list.append('')
        
        ## message의 maintext 부분을 message 형식으로 가져옴
        if type(msg._payload) is list:
            msg_body = str(msg.get_payload()[0])
        else:
            msg_body = str(msg.get_payload())

        # encoding 정보를 찾아줌
        anchor_index = msg.get_charsets()
        for charset_index in anchor_index :
            if charset_index != None :
                anchor_index = charset_index
                break
            else : 
                anchor_index = -1 

        # encode 정보를 포함하고 있으면 해당 encode를 가져옴. 그렇지 않을경우 euc-kr 형식으로 지정
        if anchor_index == -1:
            encode_i = 'euc-kr'
        else:
            encode_i = anchor_index

        # base64 형식으로 encoding 된 문서인지 확인
        msg_4_base64 = str(msg)
        base64_index = msg_4_base64.find('base64')

        # main_text에 접근하는 경우를 base64일때와 아닐때로 나눔
        if base64_index >-1 :
            start = base64_index + 6
            txt = msg_4_base64[start:]
            try:
                d = base64.urlsafe_b64decode(txt + '=' * (4 - len(txt) % 4))
                main_text = d.decode(encode_i, errors='ignore')
            except:
                try:
                    d = base64.b64decode(txt, ' /')
                    main_text = d.decode(encode_i, errors='ignore')
                except:
                    try:
                        pad = padding(txt)
                        b1 = pad.encode(encode_i)
                        b2 = base64.b64decode(b1, ' /')
                        main_text = b2.decode(encode_i, errors='ignore')
                    except:
                        try:
                            main_text = msg_body
                        except:
                            not_open_file.append(fle)
                    continue
               
        else:
            # 받아온 encode를 기존에 모아둔 encode_ex 중에서 제일 비슷한 놈으로 바꿔줌
            unknown_encode.append(encode_i)
            encode_i = change_unknown_encode(encode_i)

            # 바꾼 encode를 넣고 다시 파일 열기 시도
            try:
                main_text = open_file(encode_i, encode_i, encode_i)
                # print(unknown_encode)
            except :
                main_text =  open_file('utf8','euc-kr' ,'euc-kr')


        # main_text에서 html tag를 뺀 text 파일과 img 파일을 분리함.

        # 이미지 주소 출력
        soup = BeautifulSoup(main_text, 'html.parser')

        imgs = soup.findAll( 'img')
        num_imgs = len(imgs)

        # html tag를 뺀 text만 지정
        main_text_no_tag = soup.text.strip()

        # 본문에 url을 포함하고 있는지 여부 확인
        if main_text_no_tag.find('http') >= 0:
            include_url = 1
        else:
            include_url = 0

        # 제목과 header 정보를 포함하고 있는 csv_list에 본문 정보를 추가해줌
        csv_list += [main_text_no_tag, include_url ,num_imgs]

        # 합쳐진 csv_list를 csv에 입력
        csvwriter.writerow(csv_list)

