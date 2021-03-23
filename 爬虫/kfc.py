import requests
import json

def getMenu():
    res = requests.post(url, data = data, headers=header, cookies=cookie)
    print(res.json())
    with open('kfc.json', 'w') as f:
        f.write(json.dumps(res.json(), ensure_ascii=False))

if __name__ == '__main__':
    header = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'referer':'https://order.kfc.com.cn/mwos/menu'
    }
    data = {
        'quickOrder':'',
        'storeCode':'',
        'portalType':'WAP',
        'deviceId':'a9b6aca7-799e-423a-978e-5a8c938a96e5',
        'borwer_id':'unique-test-4a4d32c6-ccc9-41c0-9130-deee4854ee67'
    }
    url = 'https://order.kfc.com.cn/mwos/rest/core/menu/getMenuByStore'
    cookie = {
        'JSESSIONID':'hE0zm9YawKJX8wBJEq3iUja2GSGezNIK0WgWlkH2',
        'SERVERID':'c16792f0f158ac16a3433048f7e4eb8b|1616405439|1616405402',
        'ga_uuid':'unique-test-4a4d32c6-ccc9-41c0-9130-deee4854ee67',
        
    }
    getMenu()