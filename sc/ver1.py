# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from time import sleep



# Widnows version
# s = Service("./chromedriver.exe")

# Mac version
s = Service("/usr/local/bin/chromedriver")


driver = webdriver.Chrome(service=s)
driver.get("https://sdms.dysh.tyc.edu.tw/school/roll_call_landing")


# Ask yes or no using tk
ask_login_tk = messagebox.askyesno(
    title = "Ask yes or no",
    message = "你登入完了嗎?",
    detail = "Click NO to quit"
)
if not ask_login_tk:
    exit()



sleep(1)
driver.get("https://sdms.dysh.tyc.edu.tw/school/Roll_Call/Admin/RC/RC_card?title=%u5237%u5361%u9ede%u540dz")





# ------ Start go to data ------

start_scrape_ask = input("開始抓取自學刷卡點名 (Y/y):")
if start_scrape_ask == "y" or start_scrape_ask == "Y":
    author_website = "yeh-john.github.io"
else:
    quit()


std_class = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[2]')
std_seatNum = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[3]')
std_number = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[1]')
std_name = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[4]')
std_status = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[5]/select/option[1]')

# Other std_status option
std_statusA = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[6]/select/option[1]')


Class = []
SeatNum = []
Number = []
Name = []
Status = []
late_stdNum = []


def add_element():
    for add_class in std_class:
        Class.append(add_class.text)

    for add_seatNum in std_seatNum:
        SeatNum.append(add_seatNum.text)

    for add_number in std_number:
        Number.append(add_number.text)

    for add_name in std_name:
        Name.append(add_name.text)

    for add_status in std_status:
        Status.append(add_status.text)


def edit_list():
    if '' in Class:
        Class.remove('')
    if '' in SeatNum:
        SeatNum.remove('')
    if '' in Number:
        Number.remove('')
    if '' in Name:
        Name.remove('')
    if '' in Status:
        Status.remove('')



def check_data():
    # If Status's data is empty
    if len(Status) < 1:
        for add_statusA in std_statusA:
            Status.append(add_statusA.text)
        if '' in Status:
            Status.remove('')


def convert_csv():
    df = pd.DataFrame({'Class': Class, 'Seat': SeatNum, 'Number': Number, 'Name': Name, 'Status': Status})
    sleep(1)
    late_std = df[df['Status'] != '已刷卡']
    late_std = late_std.reset_index(drop=True)
    print(late_std)
    # print("________________")

    result_stdNum = late_std["Number"].to_list()

    for add_result_stdNum in result_stdNum:
        late_stdNum.append(add_result_stdNum)

    return late_std


# Use def script
add_element()
sleep(1)
edit_list()
sleep(1)
check_data()
sleep(1)
testA = convert_csv()
ansA = testA



# --------  Start get arrival time --------

sleep(3)
print("3秒後跳到抓到校時間頁面.....")
driver.get("https://sdms.dysh.tyc.edu.tw/school/Roll_Call/admin/RC/Roll_Call2?title=%u9ede%u540d%u7ba1%u7406")


arrivalTime = []
arrivalStdnum = []



def get_arrivalTime():
    std_arrivalTime = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[4]')
    std_arrivalStdnum = driver.find_elements(By.XPATH, '/html/body/div[2]/form/div[4]/table/tbody/tr/td[1]')

    for add_arrivalTime in std_arrivalTime:
        arrivalTime.append(add_arrivalTime.text)
    for add_arrivalStdnum in std_arrivalStdnum:
        arrivalStdnum.append(add_arrivalStdnum.text)

    if '' in arrivalTime:
        arrivalTime.remove('')
    if '' in arrivalStdnum:
        arrivalStdnum.remove('')
    


def convert_ArrivalCsv():
    df_arrivalStd = pd.DataFrame({'Number': arrivalStdnum, 'arrivalTime': arrivalTime})
    sleep(1)
    df_arrivalStd = df_arrivalStd.reset_index(drop=True)



    fillter_data = df_arrivalStd[df_arrivalStd['Number'].isin(late_stdNum)]
    fillter_data = fillter_data.reset_index(drop=True)
    

    return fillter_data


geting_arrivalStd = input("是否開始抓取到校時間?  Y / y :")
num = 1
while geting_arrivalStd == "y" or geting_arrivalStd == "Y":
    sleep(1)
    get_arrivalTime()
    print("已抓取完第"+str(num)+"個班級......")
    num = num + 1
    geting_arrivalStd = input("是否開始抓取到校時間?  Y / y :")





testB = convert_ArrivalCsv()
ansB = testB



print("----- This is result -----")
result_data = pd.merge(ansA, ansB, on='Number')
print(result_data)



sleep(3)
print("")
print("done......")
