#!/usr/bin/env python

import sys
import getopt
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
    print('START')
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
            time.sleep(60)
            check += 1
            if check == 10:
                phones[phones_list[i]] = 'zły numer/brak operatora'
                i+=1
                check = 0

    # print(phones)
    create_report_txt(report_name, phones)

def help():
    text = "Skrypt phone_operator.py v1.0\n" \
           "Opcje:\n" \
           "-h : Pomoc\n" \
           "-f : Nazwa pliku z numerami\n" \
           "-r : Nazwa pliku raportu z numerami i ich operatorami\n" \
           "Przyklad uzycia:\n" \
           "python3 checkip.py -f 'numbers.txt' -r 'report.txt'"
    return text

def main():

    report_file = 'report.txt'

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hf:r:")
        if not opts:
            print('Wymagane podanie pliku z adresami')
            print(help())
            sys.exit(2)
    except getopt.GetoptError as err:
        print(err)
        opts = []

    for opt, arg in opts:
        if opt in ['-h']:
            print(help())
            sys.exit(2)
        elif opt in ['-f']:
            numbers_file = arg
        elif opt in ['-r']:
            report_file = arg
        else:
            print('Nie rozpoznano komendy\n', help())

    phone_list = open_file_txt(numbers_file)
    run_scope(phone_list, report_file)
    print('Done!')

if __name__ == "__main__":
    main()
