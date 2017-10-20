#! encoding=utf-8

# Creation Date: 2017-10-20 16:44:23
# Created By: Heyi Tang

import json
def f2json(f):
    with open(f) as fin:
        data = json.load(fin)
    return data
def json2f(data, f):
    with open(f, "w") as fout:
        json.dump(data, fout, indent = 1)

from collections import defaultdict
def load_locs(enf, zhf):
    en_data = f2json(enf)
    zh_data = f2json(zhf)
    result = {}
    names = {}
    roles = defaultdict(list)
    key2loc = {}
    for key,val in sorted(en_data.items()):
        keys = key.split(".")
        if keys[0] != "location":
            continue
        if len(keys) == 2:
            loc_key = val
            key2loc[keys[1]] = val
            loc_zh = zh_data[key]
            names[loc_key] = loc_zh
        elif len(keys) == 3:
            role = "%s:%s" % (val, zh_data[key])
            roles[key2loc[keys[1]]].append(role)
    result = {"names":names, "roles":roles}
    for k,v in roles.items():
        print ""
        print k, names[k]
        for role in v:
            print role
    return result

if __name__ == "__main__":
    data = load_locs("en-US.json", "zh-TW.json")
    print len(data["names"])
    json2f(data, "zh-tw-52.json")
