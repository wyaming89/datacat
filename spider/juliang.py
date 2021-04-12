import hashlib, urllib.parse as parse

"""
1.作者最新15条作品数据API
https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6692552362847895564&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems&sign=547043cc0904784066615da65d2fedee
参数：
o_author_id 作者id
platform_source 1
platform_channel 1
limit 15
service_name 服务名
service_method 函数
sign 以上参数md5

2.作者ID来源，达人列表API
https://star.toutiao.com/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&task_category=1&order_by=score&disable_replace_keyword=false&is_filter=false&use_recommend=1
参数：
limit 项目数
need_detail
page 页数
paltform_soucre 1
task_category 1
order_by score 排序

3.sign参数是将url所有params字典排序后再MD5散列

"""

def md5Param(url):
    """
    传入带必要参数但没有sign的url，返回带sign的url
    params:
        url  带参数url
    return:
        url
    >>> url = https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6692552362847895564&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems
    >>> md5Param(url)
    out: https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6692552362847895564&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems&sign=547043cc0904784066615da65d2fedee
    """
    query = parse.urlparse(url).query
    if query:
        paramdict = {}
        content = ''
        for q in query.split('&'):
            res = q.split('=')
            paramdict[res[0]] = res[1]

        #字典排序
        for k in sorted(paramdict):
            content += k
            content += str(paramdict[k])
        #带固定字符串
        content += "e39539b8836fb99e1538974d3ac1fe98"
        sign = hashlib.md5(content.encode()).hexdigest()
        return url+f'&sign={sign}'
    else:
        print('url没有带参数')

def main():
    url = 'https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6692552362847895564&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems'
    testurl = 'https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6692552362847895564&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems&sign=547043cc0904784066615da65d2fedee'
    res = md5Param(url)
    assert res==testurl 
    print('测试通过')

if __name__ == '__main__':
    main()

    
