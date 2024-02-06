# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 09:31:25 2023

@author: rnjsd
"""


import pandas as pd
import time
import random
#please pip install selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_popup(browser, by, value):
    try:
        browser.find_element(by, value)
        return True
    except:
        return False
    
def is_tel(browser, by, value):
    try:
        browser.find_element(by, value)
        return True
    except:
        return False
    
def get_information(name, url, browser=None):
    if not browser:
        browser = Chrome()
    browser.get(url)
    browser.maximize_window()
    time.sleep(random.uniform(3, 4.5))
    df = pd.DataFrame()

    #팝업
    if is_popup(browser, By.XPATH, '//*[@id="detailinfoview"]/div[2]/div/button'):
        browser.execute_script("floating_close();")
        tag_num = 11
    else:
        tag_num = 9
            
    #태그
    if browser.find_element(By.XPATH, f'//*[@id="detailGo"]/div[{tag_num}]/button').is_displayed():
        browser.find_element(By.XPATH, f'//*[@id="detailGo"]/div[{tag_num}]/button').click()
    WebDriverWait(browser, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.tag_cont div.inr ul.clfix'))
    )
    tag = browser.find_element(By.CSS_SELECTOR, 'div.tag_cont div.inr ul.clfix').text.replace('#', '').replace('\n', ', ')
    
    #장소 설명
    place_info = browser.find_element(By.CSS_SELECTOR, 'div.area_txtView.top div.inr_wrap div.inr').text
    #번호
    if is_tel(browser, By.CSS_SELECTOR, 'div.wrap_contView div.area_txtView.bottom div.inr_wrap span.pc'):
        tel = browser.find_element(By.CSS_SELECTOR, 'div.wrap_contView div.area_txtView.bottom div.inr_wrap span.pc').text
    else:
        tel = ''
    
    #주소
    for i in browser.find_elements(By.CSS_SELECTOR, 'div.wrap_contView div.area_txtView.bottom div.inr_wrap li'):
        if i.text.strip().startswith('주소'):
            address = ' '.join(i.text.split(' ')[1:])
    #장소 부연 설명
    sub_head = browser.find_element(By.CSS_SELECTOR, 'div.titleType1 h3').text
    #조회수
    view_count = browser.find_element(By.CSS_SELECTOR, 'div.post_area span.num_view span').text
    #조회수가 ...K일때, K = 1000
    if view_count.endswith('K'):
        view_count = int(float(view_count[:-1]) * 1000)
    else:
        view_count = int(view_count)

    df['name'] = [name]
    df['sub_head'] = [sub_head]
    df['view_count'] = [view_count]
    df['tel'] = [tel]
    df['tag'] = [tag]
    df['info'] = [place_info]
    df['address'] = [address]
    return df

def get_name_link(url):
    browser = Chrome()
    browser.get(url)
    browser.maximize_window()
    time.sleep(5)
    
    name_link_dict = {}
    while True:
        names = browser.find_elements(By.CSS_SELECTOR, 'div.tit a')
        links = browser.find_elements(By.CSS_SELECTOR, 'div.tit a')
        for name, link in zip(names, links):
            click_ = link.get_attribute('onclick').split("'")
            add_adr = click_[1]
            new_url = 'https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=' + add_adr + '&big_category=A02&mid_category=A0203&big_area=1'
            name_link_dict[name.text] = new_url
        print('url')
        if '다음' in browser.find_element(By.CSS_SELECTOR, 'div.page_box').text:
            now_page = int(browser.find_element(By.CSS_SELECTOR, 'div.page_box a.on').text)
            next_page = str(now_page+1)
            xpath_ = f'//div[@class="page_box"]/a[@id={next_page}]'
            browser.find_element(By.XPATH, xpath_).click()
            time.sleep(random.uniform(3, 4.5))
        else:
            print('페이지 끝!')
            break
    return name_link_dict          