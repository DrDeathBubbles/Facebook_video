def search_key_2( stages, key):
    out = []
    for i in stages:
        if key == i['id']:
            out.append(i)
#        if key in i.values():
#            out.append(i)
    return out            


def test():
    return None 