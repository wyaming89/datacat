from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageChops
from base64 import b64decode
from io import BytesIO
import numpy as np
import time
from selenium.webdriver.common.action_chains import ActionChains 



chrome_opts = Options()
#chrome_opts.add_argument('--headless')
chrome_opts.add_argument('--no_sandbox')
chrome_opts.add_argument('--disable-gpu')
chrome_opts.add_argument('--window_size=1920,1080')

url = 'https://captcha1.scrape.center/'

def get_driver(url):
    brower = webdriver.Chrome(chrome_options=chrome_opts)
    brower.get(url)
    time.sleep(2)
    u_input = brower.find_element_by_xpath('//input[@type="text"]')
    u_input.clear()
    u_input.send_keys('admin')
    p_input = brower.find_element_by_xpath('//input[@type="password"]')
    p_input.send_keys('admin')
    btn = brower.find_element_by_xpath('//button')
    btn.click()
    time.sleep(2)
    return brower


def get_image(driver, class_name):
    exec_js = 'return document.getElementsByClassName("'+class_name+'")[0].toDataURL("image/png");'
    try:
        imgstr = driver.execute_script(exec_js)
    except:
        print('出错')
    else:
        if imgstr:
            pic = b64decode(imgstr.split(',')[1])
            p = Image.open(BytesIO(pic))
            return BytesIO(pic)

def diff_offset(driver):
    pic1 = get_image(driver,'geetest_canvas_bg geetest_absolute')
    pic2 = get_image(driver,'geetest_canvas_fullbg geetest_fade geetest_absolute')
    captcha_bg = Image.open(pic1)
    captcha = Image.open(pic2)
    diff = ImageChops.difference(captcha, captcha_bg)
    im = np.array(diff)
    width, height = diff.size
    diff = []
    for i in range(height):
        for j in range(width):
            # black is not only (0,0,0)
            if im[i, j, 0] > 15 or im[i, j, 1] > 15 or im[i, j, 1] > 15:
                diff.append(j)
                break
    return min(diff)

def get_slice_offset(img):
    slice_img = Image.open(img)
    w,h = slice_img.size
    im = np.array(slice_img)
    diff=[]
    for i in range(h):
        for j in range(w):
            # black is not only (0,0,0)
            if im[i, j, 0] > 15 or im[i, j, 1] > 15 or im[i, j, 1] > 15:
                diff.append(j)
                break
    return min(diff)



def drag(driver,offset):
    handler = driver.find_element_by_class_name('geetest_slider_button')
    ActionChains(driver).click_and_hold(handler).perform()
    for x in draw_track(offset,1):
        ActionChains(driver).move_by_offset(x,0).perform()
    ActionChains(driver).pause(0.5).release().perform()

def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)

def draw_track(distance, seconds):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        offset = round(ease_out_expo(t/seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return tracks

def main():
    brower = get_driver(url)
    d = diff_offset(brower)
    img = get_image(brower, 'geetest_canvas_slice geetest_absolute')
    d_slice = get_slice_offset(img)
    drag(brower, d-d_slice)
    time.sleep(2)
    res = brower.find_element_by_xpath('//h2[@class="text-center"]')
    print(res.text)

if __name__ == '__main__':
    main()
