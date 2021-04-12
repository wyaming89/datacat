import requests 

url = 'https://qianfan.analysys.cn/sail/ranklist/listTopRank'
params = {
    "page": 1,
    "pageSize": 10,
    "sort": '',
    "sortFiled":'',
    "cateList": {},
    "rankType":1
}
headers = {
    "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    "referer":"https://qianfan.analysys.cn/sail/view/exquisite/index.html"
}

def getRank():
    resp = requests.get(url, headers=headers, params=params)
    print(resp.json())

if __name__ == '__main__':
    getRank()