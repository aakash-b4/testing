def StringToMap(s):
    ls = s.split("&")
    dic = {}
    for i in ls:
        temp = i.split("=")
        # print(temp)
        dic[temp[0]] = temp[1]
    return dic
