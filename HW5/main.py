from selenium import webdriver
from selenium.common.exceptions import ElementNotSelectableException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
#options.add_argument('--window-size=1900,1000')
options.binary_location=r'C:\Users\aiz\AppData\Local\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(executable_path='./drivers/geckodriver.exe', options=options)
driver.implicitly_wait(10)
driver.get('https://account.mail.ru/login')

def document_initialised(driver):
    return driver.execute_script("return initialised")

emailInput = driver.find_element(By.NAME, 'username')

emailInput.click()
emailInput.send_keys("study.ai_172")
next_button = driver.find_element(By.XPATH,f'//button[@data-test-id="next-button"]')
next_button.click()


wait = WebDriverWait(driver, 10, poll_frequency=1,
                     ignored_exceptions=[ElementNotVisibleException,
                                         ElementNotSelectableException])

passwordInput = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
passwordInput.click()

passwordInput.send_keys("NextPassword172#")

login_button = driver.find_element(By.XPATH,f'//button[@data-test-id="submit-button"]')
login_button.click()







