# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep



# Widnows version
# s = Service("./chromedriver.exe")

# Mac version
s = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=s)
driver.get("https://sdms.dysh.tyc.edu.tw/school/roll_call_landing")



""" # ------ Only development ------ !!!!!!!!!!!!!!!!!!!!!
sleep(2)
driver.find_element(by=By.XPATH, value='/html/body/div[2]/form/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/p/input').send_keys("username")
driver.find_element(by=By.XPATH, value='/html/body/div[2]/form/div[3]/div[2]/div/div[2]/div/div[1]/div[2]/p/input').send_keys("passwd")
input("Did you enter capcha? yes :")
driver.find_element(by=By.XPATH, value='/html/body/div[2]/form/div[3]/div[2]/div/div[2]/div/div[1]/input[2]').click()
sleep(3)
# ------ Only development ------!!!!!!!!!!!!!!!!!!!!!!!!
 """



input("Did you login? yes :")
sleep(1)
driver.get("https://sdms.dysh.tyc.edu.tw/school/Roll_Call/Admin/RC/RC_card?title=%u5237%u5361%u9ede%u540dz")





# ------ Start go to data ------

input("Start scraping :")


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
    # print(late_stdNum)

    # Test -------------
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

geting_arrivalStd = input("Do you want to start to get arrival time?   Y / y  :")

if geting_arrivalStd == "Y" or geting_arrivalStd == "y":
    driver.get("https://sdms.dysh.tyc.edu.tw/school/Roll_Call/admin/RC/Roll_Call2?title=%u9ede%u540d%u7ba1%u7406")
    sleep(1)


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
    #print(df_arrivalStd)    
    #print("-- -- --- --- - - - --")


    #print("This is late_stdNum ")
    #print(late_stdNum)



    fillter_data = df_arrivalStd[df_arrivalStd['Number'].isin(late_stdNum)]
    fillter_data = fillter_data.reset_index(drop=True)
    
    #print("")
    #print("---- This is arrival time ----")
    #print(fillter_data)

    return fillter_data



while geting_arrivalStd == "y" or geting_arrivalStd == "Y":
    sleep(1)
    get_arrivalTime()
    geting_arrivalStd = input("Do you want to continue to get arrival time?  Y / y :")





testB = convert_ArrivalCsv()
ansB = testB



print("----- This is result -----")
result_data = pd.merge(ansA, ansB, on='Number')
print(result_data)



sleep(3)
print("")
print("done......")
