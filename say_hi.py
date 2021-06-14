#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

login_url = "https://login.zhipin.com/?ka=header-login"
recommend_url = "https://www.zhipin.com/web/boss/recommend"

# By default, boss will recommend 15 persons in a page, if we need say
# more hi, we need to scroll page down
MAX_RECOMMEND = 15

jobs = {
    "Python开发工程师 _ 北京  15-25K": {
        "filters": [
            "1-3年", "3-5年",
            "本科", "硕士",
            "10-20K",
            "离职-随时到岗", "在职-月内到岗"],
        "max_say_hi": 35

    },
    "云迁移灾备产品Python研发工程师 _ 北京  20-35K": {
        "filters": [
            "3-5年", "5-10年",
            "本科", "硕士",
            "10-20K", "20-50K",
            "离职-随时到岗", "在职-月内到岗"],
        "max_say_hi": 35
    },
    "云迁移灾备产品实施工程师 _ 北京  12-18K": {
        "filters": [
            "1-3年", "3-5年",
            "大专", "本科",
            "10-20K",
            "离职-随时到岗", "在职-月内到岗"],
        "max_say_hi": 30
    }
}

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=options)

# Wait after each find
browser.implicitly_wait(10)

# Switch to QRCode and wait for login
browser.get(login_url)
browser.find_element_by_css_selector("div.btn-switch").click()

WebDriverWait(browser, 100).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".chat-weclcome-warp"))
)

# Switch to recommend page
browser.get(recommend_url)

for job, conditions in jobs.items():
    print("Begin to filter job %s..." % job)

    filters = conditions["filters"]
    print("Filter Conditions is %s" % filters)

    max_say_hi = conditions["max_say_hi"]

    # For each job, switch to main body and filter job by name first
    print("Switing main page to query job %s" % job)
    browser.switch_to.default_content()
    time.sleep(5)

    # Click dropdown filter first
    browser.find_element_by_css_selector(".chat-select-job").click()

    # Select job
    job_xpath = "//span[contains(text(), '%s')]" % job
    browser.find_element_by_xpath(job_xpath).click()

    # Click to close dropdown filter
    #browser.find_element_by_css_selector(".ui-icon-arrow-down").click()

    WebDriverWait(browser, 100).until(
        # Use wait for frame 
        EC.frame_to_be_available_and_switch_to_it((By.NAME, "recommendFrame"))
        #EC.visibility_of_element_located((By.CSS_SELECTOR, ".dropdown-recommend"))
        #browser.switch_to_frame("recommendFrame")
    )

    # Filter by filters
    browser.find_element_by_css_selector(".recommend-filter").click()

    for f in filters:
        xpath = "//dd/a/span[contains(text(), '%s')]" % f
        print("Clicking contition xpath %s" % xpath)
        browser.find_element_by_xpath(xpath).click()
        time.sleep(2)
    browser.find_element_by_css_selector(".btn-sure").click()
    time.sleep(2)

    scroll_down_times = max_say_hi // MAX_RECOMMEND
    print("Need to scroll %s time(s) to "
          "get more records." % scroll_down_times)

    if scroll_down_times > 0:
        for i in range(0, scroll_down_times):
            print("Trying %s time(s) to scroll down to "
                  "get more records..." % i)
            # Move to loadmore area and trigger load more records
            load_more_element = browser.find_element_by_css_selector(
                ".loadmore")
            action = ActionChains(browser)
            action.move_to_element(load_more_element).perform()
            time.sleep(2)


    # Say Hi to all recommenders
    more = True

    # how many counts say hi
    say_hi_count = 0

    hi_button_xpath="//div[@id='recommend-list']//button[contains(text(), '打招呼')]"
    while(more):
        hi_buttons = browser.find_elements_by_xpath(hi_button_xpath)
        find_count = len(hi_buttons)
        print("Find %s persons to say hi" % find_count)

        # Page move back to button postiion
        if say_hi_count == 0:
            action = ActionChains(browser)
            action.move_to_element(hi_buttons[0]).perform()
            time.sleep(2)

        if find_count > 0:
            hi_buttons[0].click()
            say_hi_count = say_hi_count + 1
            print("Say hi to %s and total count %s" % (
                hi_buttons[0], say_hi_count))

        # if say_hi_count equals find total count or say_hi_count
        # equals max_say_hi count, then exit
        if find_count == say_hi_count or say_hi_count == max_say_hi:
            more = False

        time.sleep(3)

    # Wait after each job finish
    time.sleep(5)
