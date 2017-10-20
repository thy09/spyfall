#! encoding=utf-8

# Creation Date: 2017-10-20 00:38:37
# Created By: Heyi Tang

import xlrd
from translation import baidu, google, youdao, iciba, bing

def load_initial():
    f = "roles.xlsx"
    wb = xlrd.open_workbook(f)
    fout = open("output2.txt","w")
    table = wb.sheets()[0]
    for i in range(table.nrows):
        row = table.row(i)
        for col in row:
            if  len(col.value)<2:
                continue
            print col.value
            col.value = col.value.replace("/",";")
            result = bing(col.value, dst = "zh-CHS")
            print result
            fout.write((col.value + ":" + result + "\n").encode("utf-8"))
    fout.close()

from collections import defaultdict
def words2dict(f):
    total = 30
    lines = 8
    result  = defaultdict(list)
    key2name = {}
    for line in open(f):
        en, zh = line.rstrip().split(":")
        if en == "Spy":
            key = None
            continue
        loc, name = en.split(";")
        loc = loc.strip()
        name = name.strip()
        zhs = zh.split(";")
        namezh = zhs[-1]
        if len(zhs)>0:
            key2name[loc] = zhs[0]
        result[loc].append("%s:%s" % (name, namezh))
        print loc, key2name[loc], name, namezh
    for k,v in sorted(key2name.items()):
        print k,v
    print len(key2name)
    return {"names": key2name, "roles": result}

import json

if __name__ == "__main__":
    f = "output2.txt"
    data = words2dict(f)
    json.dump(data, open("words.json","w"), indent = 1)

