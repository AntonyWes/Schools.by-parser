import datetime
import time

import pandas
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

username = 'alex.rozhkov'
password = 'schoolRozhkov-911'
chetvert = 4
MARKS = {}
week_date = datetime.date(2024, 4, 1)
driver = webdriver.Chrome()
driver.get("https://schools.by/login")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_username"]'))).send_keys(username)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_password"]'))).send_keys(password)
driver.find_element(By.XPATH, '//*[@id="page_layout"]/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/form/div[3]/div/div[2]/div/input[2]').click()

person_id = driver.find_element(By.XPATH, '//*[@id="page_layout"]/div[2]/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]/b').text
while week_date.month < 5 and week_date.day < 31:
    week_date += datetime.timedelta(days=7)
    url = f"https://gymn8vitebsk.schools.by/pupil/{person_id}/dnevnik/quarter/83/week/{week_date.strftime('%Y')}-{week_date.strftime('%m')}-{week_date.strftime('%d')}"#FSFSDFDSFDSFDS
    driver.get(url)
    print(url)
    week = pandas.read_html(driver.page_source)  # Returns list of all tables on page
    for day_id, day in enumerate(week):
        for lesson in day.iloc[:, 0]:
            lesson_str = "".join([character for character in str(lesson) if not character.isdigit()])
            lesson_str = lesson_str.replace(".", "")
            lesson_str = lesson_str.replace(" ", "")
            if lesson_str not in MARKS:
                MARKS[lesson_str] = []
        for ind, mark in enumerate(day.iloc[:, -1]):
            # if not "/" in mark:
            mark = ''.join(i for i in str(mark) if not i.isalpha())
            if type(mark) != float and mark != "" and day_id<5:
                lesson_str = "".join([character for character in str(day.iloc[:, 0][ind]) if not character.isdigit()])
                lesson_str = lesson_str.replace(".", "")
                lesson_str = lesson_str.replace(" ", "")
                MARKS[lesson_str].append(int(mark[0]) + 2)
print(MARKS)
for key, value in MARKS.items():
    print(f"{key}: {sum(value)/len(value)}") if value != [] else None
