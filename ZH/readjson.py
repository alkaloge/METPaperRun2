import json


def check_json(jsondict, l1val, l2val):
    def parse_key(keystr):
        level, lrange = keystr.split(':')
        return level, eval(lrange)

    for l1key, l2dict in jsondict.items():
        if 'field' in l1key:
            l1, l1range = parse_key(l1key)
            if l1val >= l1range[0] and l1val <= l1range[1]:
                for l2key, vals in l2dict.items():
                    l2, l2range = parse_key(l2key)
                    if l2val >= l2range[0] and l2val <= l2range[1]:
                        return vals['value']
    return None


if __name__ == '__main__':
    with open('test.json', 'r') as f:
        myjson = json.load(f)
    print(check_json(myjson, 0.5, 20))
