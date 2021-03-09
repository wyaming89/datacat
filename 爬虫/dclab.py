 # -*- coding:utf-8 -*-
import requests
from requests.packages import urllib3
import os, re, sys
from Crypto.Cipher import AES
import hashlib
from bs4 import BeautifulSoup

urllib3.disable_warnings()

# 全局变量，requests库请求使用headers参数
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Referer': 'https://ke.dclab.run/'
}

# 用于保持会话
s = requests.Session()


# 下载视频
# m3u8_url为视频的m3u8地址,filename为视频保存的文件名
def download_video(m3u8_url, filename):

    print('----------download_video-------------->>>')
    global headers, s
    # res = s.get(m3u8_url, headers=headers, verify=False)
    res = requests.get(m3u8_url, headers=headers)
    print(res,res.status_code )

    if res.status_code == 200:
        print('----------------')
        print('-------200---------')

        with open(filename, mode='wb') as file_object:
            for chunk in res.iter_content(1024):
                file_object.write(chunk)


        # data = res.content
        # print(data)
        # # 使用正则表达式提取出AES加密方法，密钥的url和iv
        # aes_method, key_url, iv_str = re.findall(r'#EXT-X-KEY:METHOD=(.*?),URI="(.*?)",IV=0x(.*?)\n', data)[0]
        # # 提取所有的ts文件的uri
        # ts_uri_list = re.findall(r'(.*?.ts)\n', data)
        # # 获取密钥
        # key_str = get_key(key_url)
        # print(key_str)
        # print(iv_str)
        # # print(ts_uri_list)
        #
        # # 下载视频内容
        # content = b''
        # for ts_url in ts_uri_list:
        #     url_base = m3u8_url[:m3u8_url.rfind('/') + 1]
        #     res1 = s.get(url_base + ts_url, headers=headers, verify=False)
        #     if res1.status_code == 200:
        #         # 对ts片断进行解密，拼接
        #         content += decrypt_single_ts(res1.content, iv_str, key_str)
        # # 保存为文件
        # open('%s' % filename, 'wb').write(content)
        # print(filename, '下载完毕')


# 根据key和iv对ts进行解密
# key_str为AES密钥，为十六进制字符串
# iv_str为AES的初始向量，为十六进制字符串
def decrypt_single_ts(ts, iv_str, key_str):
    # 将key和iv转化成bytes类型
    iv = bytes.fromhex(iv_str)
    key = bytes.fromhex(key_str)

    # 填充最后一个块
    pad_len = AES.block_size - len(ts) % AES.block_size
    if pad_len != AES.block_size:
        ts = ts[:-pad_len] + bytes([0] * pad_len)
    # 解密
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    out_data = cipher.decrypt(ts)
    # 提出解密后的真实数据
    if pad_len != AES.block_size:
        out_data = out_data[:-pad_len]
    return out_data


# 根据密钥的url获取密钥
def get_key(key_url):
    res = s.get(key_url, headers=headers, verify=False)
    if res.status_code == 200:
        return res.content.hex()
    return ''


# 计算x的md5值
def md5(x):
    m = hashlib.md5()
    m.update(x.encode('utf-8'))
    return m.hexdigest()


# 下载课程资料
# url为课程资料的url，filename为文件名
def download_info(url, filename):
    # 其文件为pdf
    if filename.endswith('.pdf'):
        res = s.get(
            url,
            headers=headers,
            verify=False
        )
        if res.status_code == 200:
            open(filename, 'wb').write(res.content)
            print(filename, '下载完毕')
    # 若文件为html
    if filename.endswith('.html'):
        res = s.get(
            url,
            headers=headers,
            verify=False
        )
        if res.status_code == 200:
            content = res.text
            # 爬取页面中的css
            for x in BeautifulSoup(res.text, 'lxml').find_all('link'):
                url = x['href']
                target_filename = 'data\\static\\%s' % md5(url)

                open(target_filename, 'w', encoding='utf-8').write(s.get(url, headers=headers, verify=False).text)
                content = content.replace(url, '../../static/%s' % md5(url))
            print(res.encoding)
            open(filename, 'w', encoding=res.encoding).write(content)
            print(filename, '下载完毕')


def main():
    # 登陆
    res = s.post(
        'https://ke.dclab.run/api/user/common/login.json',
        headers=headers,
        verify=False,
        data={
            'username': '15563930332',  # 用户名
            'password': '15563930332'  # 密码
        }
    )

    if res.status_code == 200:
        if res.json()['login']:
            print('登陆成功')
            userid = res.json()['data']['loginUserIds']['id']
            print('userid', userid)
            # 请求该用户购买的所有课程
            res = s.get(
                'https://ke.dclab.run/api/common/center/courseCertificateList.json',
                headers=headers,
                verify=False,
                params={"pageNo": "1", "pageSize": "100", "userId": userid}
            )
            if res.status_code == 200:
                print(res.json())
                for x in res.json()['data']['certificateList']:
                    # 课程名称
                    course_name = x['name']
                    # 课程id
                    course_id = x['course_id']
                    print(course_name)
                    res = s.get(
                        'https://ke.dclab.run/api/common/course/getCourseCatalogue.json',
                        headers=headers,
                        verify=False,
                        params={"courseId": course_id}
                    )
                    if res.status_code == 200:
                        for i, x in enumerate(res.json()['data']['courseCatalogue']):
                            # 章的名字
                            catalogue = x['name']
                            catalogue = '第%d章 %s' % (i + 1, catalogue)
                            print(catalogue)
                            for j, y in enumerate(x['trainClassMapList']):
                                # 节的名称
                                class_name = y['name']
                                # 课时id
                                class_id = y['id']

                                # 请求课程的下载连接
                                res = s.get(
                                    'https://ke.dclab.run/api/user/getVideoUrl.json',
                                    headers=headers,
                                    verify=False,
                                    params={"classId": class_id, "pixel": "1080P", "videoFrom": "2"}
                                )
                                if res.status_code == 200:
                                    # print(res.json())
                                    # print(res.json()['data']['class']['name'])
                                    # 构造课时的完整名称
                                    class_name = '%d-%d %s' % (i, j + 1, class_name)
                                    print(class_name)
                                    # 课时的视频m3u8地址
                                    m3u8_url = res.json()['data']['url']
                                    print(m3u8_url)


                                    # 存储的路径
                                    path = 'data\\%s\\%s' % (course_name, catalogue)
                                    # 若不存在该路径，创建这个路径
                                    if not os.path.isdir(path):
                                        os.makedirs(path)
                                    # 视频文件名
                                    filename = '%s\\%s.mp4' % (path, class_name)
                                    # 若该视频文件不存在，下载它
                                    if not os.path.isfile(filename):
                                        download_video(m3u8_url, filename)
                                    # 请求课程资料的url
                                    res = s.get(
                                        'https://ke.dclab.run/api/user/course/downDataOuter.json',
                                        headers=headers,
                                        verify=False,
                                        params={"dataId": class_id}
                                    )
                                    if res.status_code == 200:
                                        # print(res.json())
                                        # 课程资料的title
                                        if 'data' not in res.json():
                                            break
                                        x = res.json()['data'].get('file', '')
                                        if x:
                                            # 课程资料的文件名
                                            filename = '%s\\%s' % (path, x['name'])
                                            try:
                                                # 下载课程资料
                                                download_info(x['path'], filename)
                                            except Exception as e:
                                                # 报错的话不处理
                                                print(e)
                                                pass
main()