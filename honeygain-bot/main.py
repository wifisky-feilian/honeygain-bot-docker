# Required libraries 
import sys
import os
import time
from time import sleep
import random
import pickle
import requests
import stdiomask
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi  
from PyQt5.QtCore import pyqtRemoveInputHook
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException

# Define user agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'

# Define function to check if config.pickle is empty or not
def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

# Define delay function
def delay ():
    time.sleep(random.randint(2,4))

# Define waitfor Function
def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

# Define browser setup function
def browserSetup(user_agent: str = PC_USER_AGENT) -> WebDriver:
    # Create Chrome browser with added arguements
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument('log-level=3')
    options.add_argument("start-maximized")
    chrome_browser_obj = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    return chrome_browser_obj

# Define function to input email and password onto config.pickle using pickle lib
def inputCredentials():
	email = input('[INPUT] Enter Honeygain email: ')
	password = stdiomask.getpass('[INPUT] Enter Honeygain password: ')
	delay()

	configuration = {1: email, 2: password}
	with open('config.pickle','wb') as account_dict:
		pickle.dump(configuration, account_dict)
	
	displayCredentials()
	
# Define display credentials
def displayCredentials():
	# Open config.pickle to unpickle email and password and send to login function
	with open('config.pickle','rb') as account_dict:
		accountinfo = pickle.load(account_dict)
	
	email = accountinfo[1]		
	password = accountinfo[2]
	print('[LOGIN] Email: '+str.upper(email))
	delay()
	# Set up browser and call login function
	browser = browserSetup()
	login(browser, email, password)

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access Honeygain
	browser.get('https://dashboard.honeygain.com/')
    # Wait complete loading
	waitUntilVisible(browser, By.CSS_SELECTOR, '#root > div.sc-fAjcbJ.hETDZK > \
		div.sc-bwzfXH.iGhfYS.sc-dVhcbM.isUSGo > div.sc-brqgnP.sc-eqIVtm.eUFEVX >\
		 div > div.sc-bwzfXH.iGhfYS > svg > path:nth-child(20)', 10)
	try:
		acceptCookie = browser.find_element_by_css_selector('#root > div.sc-brqgnP.sc-csuQGl.ljIjdp > div > div.sc-bwzfXH.sc-gipzik.fLSFAs > div.sc-bZQynM.sc-jlyJG.eBdWuh > button.ButtonView-sc-1h6bhnl.iTkAsq')
		acceptCookie.click()
	except:
		pass

	# Type email
	print('[LOGIN]', 'Writing email...')
	browser.find_element_by_css_selector('#root > div.sc-fAjcbJ.hETDZK > div.sc-bwzfXH.iGhfYS.sc-dVhcbM.isUSGo > div.sc-brqgnP.sc-eqIVtm.eUFEVX > div > form > div:nth-child(1) > div > input').send_keys(email)
	delay()
	# Type  password
	print('[LOGIN]', 'Writing password...')
	browser.find_element_by_css_selector('#root > div.sc-fAjcbJ.hETDZK > div.sc-bwzfXH.iGhfYS.sc-dVhcbM.isUSGo > div.sc-brqgnP.sc-eqIVtm.eUFEVX > div > form > div:nth-child(2) > div > input').send_keys(pwd)
	# Click login
	browser.find_element_by_css_selector('#root > div.sc-fAjcbJ.hETDZK > div.sc-bwzfXH.iGhfYS.sc-dVhcbM.isUSGo > div.sc-brqgnP.sc-eqIVtm.eUFEVX > div > form > div.sc-bwzfXH.iMOrHM > button').click()
	delay()
	# Check Login
	print('[LOGIN] Retrieving Honeygain...')
	checkhoneygainLogin(browser)
	   		

# Def function to get account variables
def checkhoneygainLogin(browser: WebDriver):
    global ACCOUNT_NAME, TOTAL_EARNINGS, DAILY_EARNINGS, PAYOUT_COUNTER, DAILY_COUNTER, HONEY_JAR_FRAME
    # Access Honeygain
    browser.get('https://dashboard.honeygain.com/')
    # Wait a few seconds
    time.sleep(2)
    # Update account name
    TOTAL_EARNINGS = str(browser.find_element_by_css_selector('#root > div.sc-bwzfXH.icDwvc > div.sc-gxMtzJ.ddabaQ > div > div > div.row > div:nth-child(1) > div > div > div\
    > div > div.sc-bZQynM.bhSRNy > div > div:nth-child(1) > div.sc-bwzfXH.sc-esOvli.hliBMD > div.sc-bwzfXH.sc-iQNlJl.khWADx > div\
    > div.sc-dnqmqq.efAFyk').get_attribute('innerHTML'))
    DAILY_EARNINGS = str(browser.find_element_by_css_selector('#root > div.sc-bwzfXH.icDwvc > div.sc-gxMtzJ.ddabaQ > div > div > div.row > div:nth-child(1) > div > div > div\
    > div > div.sc-bZQynM.bhSRNy > div > div.sc-bwzfXH.fQoEQz > div.sc-bwzfXH.sc-iQNlJl.khWADx > div > div.sc-dnqmqq.efAFyk').get_attribute('innerText'))
    PAYOUT_COUNTER = str(browser.find_element_by_css_selector('#root > div.sc-bwzfXH.icDwvc > div.sc-gxMtzJ.ddabaQ > div > div > div.row > div:nth-child(1) > div > div > div\
    > div > div.sc-bZQynM.bhSRNy > div > div:nth-child(1) > div.sc-bwzfXH.sc-hXRMBi.eQRgIN > div.sc-gwVKww.hDldUr > div > span').get_attribute('innerText'))
    avatar = (browser.find_element_by_css_selector('#root > div.sc-bwzfXH.icDwvc > div.sc-bwzfXH.sc-kIPQKe.inrxjT > div.sc-bZQynM.kXSrGb > div > div.sc-kPVwWT.fBnOdz > div > svg').click())
    delay()
    ACCOUNT_NAME = (browser.find_element_by_css_selector('#root > div.sc-bwzfXH.icDwvc > div.sc-bwzfXH.sc-kIPQKe.inrxjT > div.sc-bZQynM.kXSrGb > div > div.sc-kPVwWT.fBnOdz > div.sc-esjQYD.euQfrT > div > div.sc-dfVpRl.sc-gzOgki.dtXkyG').get_attribute('innerText'))
    print('[ACCOUNT] You are currently logged into Honeygain as: ' + str(ACCOUNT_NAME) +'' )
    print('[ACCOUNT] Total Earnings: ' + str(TOTAL_EARNINGS) +'')
    print('[ACCOUNT] Daily Earnings: ' + str(DAILY_EARNINGS) +'')
    print('[ACCOUNT] Payout Counter: ' + str(PAYOUT_COUNTER) +'')
    getHoneyJar(browser)
		
def getHoneyJar(browser: WebDriver):
	time.sleep(2)
	try:
		tryYourLuckButton = browser.find_element_by_css_selector('#root > div.sc-itybZL.hIvvFD > div > div > div > div.sc-bwzfXH.sc-bHwgHz.fNQyBu > button')
		tryYourLuckButton.click()
		delay()
		openButton = browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > button')
		openButton.click()
		delay()
		dailyFree = (browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > div.sc-bwzfXH.sc-dEoRIm.jvRTRB > div.sc-dnqmqq.sc-ebFjAB.jZdCHe').get_attribute('innerText'))
		addToAccountButton = browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > button')
		addToAccountButton.click()
		time.sleep(10)
		print('[HONEY JAR] Successfully claimed ' + str(dailyFree) + ' credits!')
		browser.close()
		print('POWERED BY PASSIVEBOT.COM')
		quit()
	except:
		try:
			time.sleep(5)
			tryYourLuckButton = browser.find_element_by_css_selector('#root > div.sc-itybZL.hIvvFD > div > div > div > div.sc-bwzfXH.sc-bHwgHz.fNQyBu > button')
			tryYourLuckButton.click()
			delay()
			openButton = browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > button')
			openButton.click()
			delay()
			dailyFree = (browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > div.sc-bwzfXH.sc-dEoRIm.jvRTRB > div.sc-dnqmqq.sc-ebFjAB.jZdCHe').get_attribute('innerText'))
			addToAccountButton = browser.find_element_by_css_selector('#root > div.sc-kaNhvL.cbfFyG > button')
			addToAccountButton.click()
			print('[HONEY JAR] Successfully claimed ' + str(dailyFree) + ' credits!')
			browser.close()
			print('POWERED BY PASSIVEBOT.COM')
			quit()
		except:
			print("[HONEY JAR] Not available, please check later.")
			browser.close()
			print('POWERED BY PASSIVEBOT.COM')
			quit()

	app.quit()
	os._exit(1)

# Define Login
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("input.ui",self)
         # string value
        title = "Honeygain bot"
        self.setWindowTitle(title)
        label = QLabel(self)
        pixmap = QPixmap('logo.png')
        label.setPixmap(pixmap)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputButton.clicked.connect(self.inputCredentials)

    # Define function to input email and password onto config.pickle using pickle lib
    def inputCredentials(self):
    	email=self.email.text()
    	password=self.password.text()
    	delay()

    	configuration = {1: email, 2: password}
    	with open('config.pickle','wb') as account_dict:
    		pickle.dump(configuration, account_dict)

    	displayCredentials()


   



class Start(QDialog):
    def __init__(self):
        super(Start,self).__init__()
        loadUi("start.ui",self)
        label = QLabel(self)
        pixmap = QPixmap('logo.png')
        label.setPixmap(pixmap)
        # resizing the widget
        #self.label.resize(200, 20)
        self.startButton.clicked.connect(self.clicked_close)
        self.startButton.clicked.connect(displayCredentials)

    def clicked_close(self):
        self.close()



ticker = is_non_zero_file('config.pickle')
pyqtRemoveInputHook()
if ticker ==1:
	app=QApplication(sys.argv)
	mainwindow=Start()
	mainwindow.setStyleSheet("background-color: white;")
	widget=QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.setWindowTitle("Honeygain bot")
	widget.setFixedWidth(326)
	widget.setFixedHeight(200)
	widget.show()
else:
	app=QApplication(sys.argv)
	mainwindow=Login()
	mainwindow.setStyleSheet("background-color: white;")
	widget=QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.setWindowTitle("Honeygain bot")
	widget.setFixedWidth(326)
	widget.setFixedHeight(235)
	widget.show()


app.exec_()
app.quit()
os._exit(1)
