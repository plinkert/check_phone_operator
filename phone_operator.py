#!/usr/bin/env python

# import os
import time
import requests
import re
import xlrd
import json
from bs4 import BeautifulSoup
# import urllib3



def is_phone_num(p: str) -> str:
    rePhone = re.compile(r'((48)\d{9})|\d{9}')
    try:
        phone = rePhone.search(p).group()
    except:
        phone = ''
    return phone

def mgsm(phone: str) -> str:
    try:
        url = 'https://www.mgsm.pl/pl/wjakiejsieci/'
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url, data = {'sCheckNumber': phone}, verify = False)
        soup = BeautifulSoup(r.text, 'html.parser')
        tab = soup('table', {'cellpadding':'2'})
        resoult = tab[0].find_all('tr')[2].find_all('td')[1].find_all('b')[0].text
    except:
        resoult = ''
    return resoult

def open_file_txt(file: str) -> list:

    file = open(file)
    phones_list = []
    for phone in file.readlines():
        phone = phone.replace(" ", "").strip()
        if is_phone_num(phone) != '':
            phones_list.append(phone)
    file.close()
    return phones_list

def create_report_txt(file: str, data: dict):
    with open(file, 'w') as report:
        for key, val in data.items():
            report.write(str(key)+ '\t' + str(val) + '\n')

def run_scope(phones_list: list, report_name: str):
    phones = {}
    i = 0
    check = 0
    while(i < len(phones_list)):
        operator = mgsm(phones_list[i]).strip()
        # print(str(i) + ' ' + operator)
        if operator != '':
            phones[phones_list[i]] = operator
            i+=1
        else:
            time.sleep(10)
            check += 1
            if check == 2:
                phones[phones_list[i]] = 'zły numer/brak operatora'
                i+=1
                check = 0

    # print(phones)
    create_report_txt(report_name, phones)

if __name__ == "__main__":
    #TEST
    print('START')
    phone_list = open_file_txt('phones.txt')
    print('LISTA GOTOWA')
    run_scope(phone_list, 'raport.txt')
    print('STOP')
    # print(phones_list)
