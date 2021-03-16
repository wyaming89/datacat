import json
from urllib import parse

import requests

with open('./config.json', 'r') as f:
    config = json.loads(f.read())


header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
}



def getValidePage():
    url = config['tg_url']
    res = requests.get(url, headers=header, allow_redirects=False)
    cookie = res.cookies.get_dict()
    tg_url = parse.urlparse(res.headers['Location'])
    params = parse.parse_qs(tg_url.query)
    jsname = params['name'][0]
    seed = params['seed'][0]
    ts = params['ts'][0]
    print(jsname, seed, ts)
    return cookie, jsname, seed, ts

def getJsFile(fname, cookies):
    baseUrl = 'https://www.lagou.com/common-sec/dist/'
    url = parse.urljoin(baseUrl, fname+'.js')
    res = requests.get(url, headers=header, cookies=cookies)
    with open(fname+'.js', 'w') as f:
        f.write(res.text)

def getToken(url, params):
    res = requests.get(url, params)
    return res.text

def getPositionList(cookies):
    header['referer'] = config['tg_url']
    baseUrl = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
    data = {'first':'true','pn':1,'kd':'数据分析'}
    res = requests.post(baseUrl, data=data, headers=header, cookies=cookies)
    print(res.json())


def main():
    apiUrl = config['jsUrl']+'/lagou'
    cookie, jsname, seed, ts = getValidePage()
    getJsFile(jsname, cookie)
    params = {'name':jsname,'seed':seed, 'ts':ts}
    token = getToken(apiUrl, params)
    print(token)
    cookie['__lg_stoken__'] = token
    getPositionList(cookie)

if __name__ == '__main__':
    main()