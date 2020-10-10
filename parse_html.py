from abc import ABC
from html.parser import HTMLParser
import os
import urllib3
import time
from utils import dir_name
from os import path
http = urllib3.PoolManager()
etfs_number = 0
etfs_processed = 0
etfs_paths = dict()

def save_to_file(url, file_path):
    os.system('wget --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" ' + url + ' -O ' + file_path)
    # os.system('curl -H "Accept: application/xml" -H "Content-Type: application/xml" -X GET http://hostname/resource')

class MyHTMLParser(HTMLParser, ABC):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    if "bloomberg" in attr[1]:
                        url = attr[1].replace('http', 'https')
                        name = url.split('/')[-1]
                        global etfs_number
                        global etfs_paths
                        file_path = dir_name + '/' + name + '.html'

                        if file_path in etfs_paths:
                            continue
                        else:
                            etfs_paths[file_path] = True
                            etfs_number += 1

                        if path.isfile(file_path):
                            continue

                        time.sleep(10)
                        save_to_file(url, file_path)
                        global etfs_processed
                        etfs_processed += 1

    def handle_endtag(self, tag):
        pass
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass
        # print("Encountered some data  :", data)


if not os.path.isdir(dir_name):
    os.mkdir(dir_name)


with open("lista-funduszy-etfs.html", "r", encoding='utf-8') as f:
    text = f.read()
    parser = MyHTMLParser()
    parser.feed(text)

print('Processed ' + str(etfs_processed) + '/' + str(etfs_number) + ' etfs.')
