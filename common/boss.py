#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

LOGIN_URL = "https://login.zhipin.com/?ka=header-login"
RECOMMEND_URL = "https://www.zhipin.com/web/boss/recommend"

# By default, boss will recommend 15 persons in a page, if we need say
# more hi, we need to scroll page down
MAX_RECOMMEND = 15


class Boss(object):

    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)

        # Wait after each find
        self.browser.implicitly_wait(10)

    def wait_scan_login(self):
        """Switch to scan QRCode page and wait to login"""
        # Switch to QRCode and wait for login
        self._goto_page(LOGIN_URL)
        self.browser.find_element_by_css_selector("div.btn-switch").click()

        WebDriverWait(self.browser, 100).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".chat-weclcome-warp"))
        )

    def goto_recommend_page(self):
        self._goto_page(RECOMMEND_URL)

    def filter_job_name(self, job):
        """Switch to recommend page first"""
        self._switch_to_body()
        # Click dropdown filter first
        self.browser.find_element_by_css_selector(
            ".chat-select-job").click()

        job_xpath = "//span[contains(text(), '%s')]" % job
        self.browser.find_element_by_xpath(job_xpath).click()

        # Select job
        job_xpath = "//span[contains(text(), '%s')]" % job
        self.browser.find_element_by_xpath(job_xpath).click()

        self._switch_to_frame("recommendFrame")

        # Filter by filters
        self.browser.find_element_by_css_selector(
            ".recommend-filter").click()

    def filter_persons(self, filters):
        """Switch to recommend page first"""
        for f in filters:
            xpath = "//dd/a/span[contains(text(), '%s')]" % f
            logging.info("Clicking contition xpath %s" % xpath)
            self.browser.find_element_by_xpath(xpath).click()
            time.sleep(2)

        self.browser.find_element_by_css_selector(".btn-sure").click()
        time.sleep(2)

    def say_hi(self, max_say_hi):
        scroll_down_times = max_say_hi // MAX_RECOMMEND
        logging.info("Need to scroll %s time(s) to "
              "get more records." % scroll_down_times)

        if scroll_down_times > 0:
            for i in range(0, scroll_down_times):
                logging.info("Trying %s time(s) to scroll down to "
                      "get more records..." % i)
                # Move to loadmore area and trigger load more records
                #load_more_element = browser.find_element_by_css_selector(
                #    ".loadmore")
                #action = ActionChains(browser)
                #action.move_to_element(load_more_element).perform()
                self._scroll_page_by_css(".loadmore")
                time.sleep(2)

        # Say Hi to all recommenders
        more = True

        # how many counts say hi
        say_hi_count = 0

        hi_button_xpath="//div[@id='recommend-list']//button[contains(text(), '打招呼')]"
        while(more):
            hi_buttons = self.browser.find_elements_by_xpath(
                hi_button_xpath)

            # Page move back to button postiion
            if say_hi_count == 0:
                action = ActionChains(self.browser)
                action.move_to_element(hi_buttons[0]).perform()
                time.sleep(2)
                find_count = len(hi_buttons)
                logging.info("Find %s persons to say hi" % find_count)

            if find_count > 0:
                hi_buttons[0].click()
                say_hi_count = say_hi_count + 1
                logging.info("Say hi to %s and total count %s" % (
                    hi_buttons[0], say_hi_count))

            # if say_hi_count equals find total count or say_hi_count
            # equals max_say_hi count, then exit
            if find_count == say_hi_count or say_hi_count == max_say_hi:
                more = False

            time.sleep(3)

    def _goto_page(self, page_url):
        logging.info("Goto page %s" % page_url)
        self.browser.get(page_url)

    def _switch_to_body(self):
        """Switch to body page, if you are in a frame"""
        self.browser.switch_to.default_content()
        time.sleep(5)

    def _switch_to_frame(self, frame_name):
        WebDriverWait(self.browser, 100).until(
            # Use wait for frame 
            EC.frame_to_be_available_and_switch_to_it((By.NAME, frame_name))
        )

    def _scroll_page_by_css(self, css_selector):
        scroll_element = self.browser.find_element_by_css_selector(
            css_selector)
        action = ActionChains(self.browser)
        action.move_to_element(scroll_element).perform()
