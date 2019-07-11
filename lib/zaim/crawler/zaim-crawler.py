# coding: utf-8


import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException

from time import sleep
import json
import re
from zaimpass import zaimId, zaimPass


def printList(data):
    print(json.dumps(data, ensure_ascii=False))


options = Options()
# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

# options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)


# login
driver.get('https://auth.zaim.net/')
driver.find_element_by_name('data[User][email]').send_keys(zaimId)
driver.find_element_by_name('data[User][password]').send_keys(zaimPass)
driver.find_element_by_xpath('//*[@id="UserLoginForm"]/div[4]/input').click()


# getData
driver.get('https://zaim.net/money')
sleep(1)
tr = driver.find_elements_by_css_selector(
    '#main > div.main-content > div > div:nth-child(7) > table > tbody > tr')


data = []

year = int(driver.find_element_by_class_name('btn-jump-to-month').text[0:4])
for i in tr:
    buff = {
        'category': i.find_element_by_class_name('category').find_element_by_tag_name('span').get_attribute('alt'),
        'price': int(i.find_element_by_class_name('price').text[1:].replace(',', '')),
        'store': i.find_element_by_class_name('place').find_element_by_tag_name('span').get_attribute('data-original-title'),
        'product': i.find_element_by_class_name('name').find_element_by_tag_name('span').get_attribute('data-original-title'),
        'memo': i.find_element_by_class_name('comment').text
    }

    # 4月16日（火）
    dateRawText = i.find_element_by_class_name('date').text
    reDate = re.search(u'(\d*)月(\d*)日', dateRawText)
    buff['date'] = {
        'year': year,
        'month': reDate.group(1),
        'day': reDate.group(2)
    }

    try:
        buff['from_account'] = i.find_element_by_class_name(
            'from_account').find_element_by_tag_name('img').get_attribute('alt')
    except NoSuchElementException as e:
        print(e)

    try:
        buff['to_account'] = i.find_element_by_class_name(
            'to_account').find_element_by_tag_name('img').get_attribute('alt')
    except NoSuchElementException as e:
        print(e)

    data.append(buff)

printList(data)
