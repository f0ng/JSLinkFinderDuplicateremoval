# -*- coding:utf-8 -*-
# author:f0ngf0ng

from concurrent.futures import ThreadPoolExecutor
import urllib3
import ssl

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
import requests

fuzz = []

def push_fuzz(url):
    uu_rl = url.split("/")
    print(uu_rl[2])
    with open("fuzz.txt", "r+") as file:
        for file_1 in file:
            file_1 = file_1.strip()
            file_1 = file_1.replace("www.google.com","asd" +uu_rl[2]).replace("google.com","asd" +uu_rl[2])
            file_1 = file_1.replace("www.whitelisteddomain.tld", uu_rl[2])
            fuzz.append(file_1)

    return fuzz

def fuzz_url(url):
    url = url.strip()
    fuzz_url_uri = []
    url_list_0 = url.split("?")
    url_list_1 = url_list_0[1].split("&")
    url_index = url_list_0[0]
    url_list_0[0] = url_list_0[0] + "?"

    for ii in url_list_1:
        url_list_3 = ii.split("=")
        ii = url_list_3[0] + "="
        url_list_0[0] = url_list_0[0] + ii + "&"

    url_list_0[0] = url_list_0[0].strip("&")

    url_0 = url_list_0[0]

    url_1 = url_0.split("?")
    a = url_1[1] + "&"
    aa = a.split("=&")
    aa.pop()

    for i in aa:
        if len(aa) == 1:
            fuzz_url_uri.append(url_index + "?" + i + "=")
        else:
            url_total = ""
            for iii in url_list_1:
                if i in iii:
                    a = i
                    continue
                else:
                    url_total = url_total + "&" + iii
                    url_total = url_total.strip("&")

            url_total = url_total + "&" + a + "="
            fuzz_url_uri.append(url_index + "?" + url_total)

    return fuzz_url_uri


def fuzz_url_test(list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    is_vul = 0
    for list_single in list:
        for fuzz_single in fuzz:
            url_final = list_single + fuzz_single

            try:
                a = requests.get(url_final, headers=headers, verify=False)

                if "Location:" in a.headers and "f0ng" in a.headers:
                    print("url跳转" + url_final)
                    is_vul = 1

                if "text/html" in a.headers and "alert(1)" in a.content:
                    print("存在xss" + url_final)
                    is_vul = 1

                if "f0ng=f0ng" in a.headers:
                    print("存在CRLF" + url_final)
                    is_vul = 1

            except requests.exceptions.ProxyError as e :
                print(e)

    if is_vul == 1:
        print("**********************\n"
              "**********************\n"
              "**********************")


if __name__ == '__main__':

    while True:

        url = input("f0ng专用fuzz\n"
                    "请输入fuzz的url：")


        b = push_fuzz(url)

        if "http://" in url:
            a = fuzz_url(url)

        elif "https://" not in url:
            a = fuzz_url("https://" + url)

        else:
            a = fuzz_url(url)

        print(a)

        with ThreadPoolExecutor(50) as pool:

            pool.submit(fuzz_url_test, a)

