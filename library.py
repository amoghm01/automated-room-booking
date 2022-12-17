import calendar
import json
import string
from datetime import datetime, time, date, timedelta
import time as t
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

df = open('../data.json',)
data = json.load(df)
df.close()

OPENLINK = data[0]['link']
ROOM = data[0]['room']
PASS = data[0]['pass']
USER = data[0]['user']
REFLINK = data[0]['refLink']
FINALLINK = data[0]['finalLink']

options = Options()
options.add_experimental_option("detach", True) #keeps browser open after completion

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                        options=options)

#for my own sanity
def caesar(text, step, alphabets):

    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]

    shifted_alphabets = tuple(map(shift, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)

alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation)

def lib(days):

    driver.get(OPENLINK)

    driver.maximize_window()

    link = driver.find_element("xpath", "//*[@aria-label='Go To Date']")

    # print(link)
    link.click()

    midnight = (int(t.time() // 86400)) * 86400

    midStr = str(midnight) + "000"

    # two weeks in advance: set shift = 13 * 86400000
    shift =  days * 86400000 
    targetUnixDate = int(midStr) + shift

    targetDateBtn = str(targetUnixDate)

    path = "//*[@data-date='" + targetDateBtn +  "']"

    link = driver.find_element("xpath", path)
    link.click()

    target = date.today()+timedelta(days)

    targetNormalDate = target.strftime("%A, %B %d, %Y")

    path1 = "//*[@title='4:00pm " + targetNormalDate + " " +  ROOM + "']"
    path2 = "//*[@title='5:00pm " + targetNormalDate + " " +  ROOM + "']"
    path3 = "//*[@title='6:00pm " + targetNormalDate + " " +  ROOM + "']"
    path4 = "//*[@title='7:00pm " + targetNormalDate + " " +  ROOM + "']"
    pathArray = [path1, path2, path3, path4]
    t.sleep(0.2)

    for i in range(0, len(pathArray)):
        link = driver.find_element("xpath", pathArray[i])
        link.click()
        t.sleep(0.2)

    path = "//button[@id='submit_times']"

    link = driver.find_element("xpath", path)
    # print(link.get_attribute("innerHTML"))
    link.click()

    t.sleep(0.2)
    driver.switch_to.window(driver.window_handles[0])
    # print(driver.current_url)

    userPath = "//input[@id='ssousername']"
    userForm = driver.find_element("xpath", userPath)
    userForm.send_keys(USER)

    enterPass = caesar(PASS, 7, alphabets)

    passPath = "//input[@id='ssopassword']"
    passForm = driver.find_element("xpath", passPath)
    passForm.send_keys(enterPass)

    submitPath = "//button[@type='submit']"
    submitBtn = driver.find_element("xpath", submitPath)
    submitBtn.click()

    driver.switch_to.window(driver.window_handles[0])

def continueOn():
    
    # print(driver.current_url)
    continuePath = "//button[@name='continue']"
    continueBtn = driver.find_element("xpath", continuePath)
    continueBtn.click()

    driver.switch_to.window(driver.window_handles[0])
    # print(driver.current_url)

def toSubmit():
    submitPath = "//button[@id='s-lc-eq-bform-submit']"
    submitBtn = driver.find_element("xpath", submitPath)
    submitBtn.click()

def main():
    # lib(14) for 2 weeks
    # lib(6) on Jan 3 for Jan 9 booking
    lib(1)
    
    t.sleep(4)
    
    refURL = driver.current_url
    print(refURL)
    
    print("HERE")
    if(refURL[0:62] == REFLINK):
        continueOn()
    refURL = driver.current_url
    if(refURL[0:56] == FINALLINK):
        toSubmit()
        
    
if __name__ == "__main__":
    main()