import re
import sys
import time

import requests
from googleapiclient.discovery import build
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

api_key = "AIzaSyCbxA2wgD7xRjZ6zlc8K0RSZFXb-6iBH6c"
cse_id = "009601857586525310085:zmpvuts9nra"

def google_search(quest, ans):
    quest = re.sub('[^A-Za-zа-яА-Я0-9\s]+', "", quest)
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=quest + ' intext:"' + ans + '"', cx=cse_id).execute()
    return int(res["searchInformation"]["totalResults"])

def word2vec(query, ans):
    query = re.sub('[^A-Za-zа-яА-Я0-9\-\s]+', "", query)


driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get("https://myquiz.ru")
lst_q = ""
predvars = []
while True:
    if "/p/" in driver.current_url:
        try:
            quest_text = driver.find_element_by_id("questionDetails__Text").get_attribute("innerHTML") #questionDetails__Text
            if quest_text != lst_q:
                lst_q = quest_text
                #print(quest_text)

                ans_block = driver.find_element_by_id("questionDetails__Answers")
                answers = driver.find_elements_by_class_name("answerButton__TextSpan")
                vars = []
                for answer in answers:
                    vars.append(answer.get_attribute("innerHTML"))
                if vars != predvars:
                    print(vars)
                    predvars = vars
                    mxv = vars[0]
                    mxi = 0
                    mxa = -1
                    i = 0
                    for var in vars:
                        res = google_search(quest_text, var)
                        if res > mxa:
                            mxa = res
                            mxi = i
                            mxv = var
                        print(var, res)
                        i += 1
                    print("# QUESTION: ", quest_text)
                    answers[mxi].click()
                    print("Ответ: ", mxv)

        except:
            pass

#AIzaSyAXX7DMcU_LF6jRTzU00TcHHjFecBX7psc
#009601857586525310085:asinawfu-bo