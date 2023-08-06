#!/usr/bin/python
# -*- coding:utf-8 -*-

from deepl import deepl
import pyperclip
import time
import sys
import os

replace_list = [
    ["-\r\n-", ""],
    ["-\r\n", ""],
    ["\r\n-", ""],
    ["\r\n", " "],
    ["-\n-", ""],
    ["-\n", ""],
    ["\n-", ""],
    ["\n", " "]
]

def translate(sentences):

    t = deepl.DeepLCLI("en", "zh")
    print("\033[1;34m"+sentences+"\n\033[0m")

    result = t.translate(sentences)

    print("\033[1;32m"+result+"\n\033[0m")
    print("#################")

    del t

def main():
    prv = ''
    pyperclip.copy('')
    sys.stderr = open(os.devnull, 'w')
    print('大帅比！Deepl 翻译引擎已开启，你来复制，我来翻译！' + '\n')
    print("#################")
    try:
        while(True):
            time.sleep(1)
            new = pyperclip.paste()
            for r in replace_list:
                new = new.replace(r[0], r[1])
            pyperclip.copy(new)
            if len(new) > 0 and new != prv:
                translate(new)
                prv = new
    except:
        pass            

if __name__ == '__main__':
    main()
