import os
from time import sleep
from selenium import webdriver
from flask_bcrypt import Bcrypt
from user import username, password
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC





class Setup:
    def __init__(self):
        self.username = username
        self.password = password
        if self.username == None:
            self.username = input("Please Enter Your Username/Email. You will only be asked for your login info once: ")
            with open('user.py', 'w') as file:
                file.write(f'username = "{self.username}"\n')
                file.write(f'password = {self.password}\n')
        if self.password == None or self.password == "None":
            self.password = self.cipher_suite.encrypt(bytes(input("Please Enter Your Password: ").encode()))
            with open('user.py', 'w') as file:
                file.write(f'username = "{self.username}"\n')
                file.write(f'password = "{self.password}"\n')
        # set webdriver to chrome. Try for mac, except for PC
        self.key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
        self.cipher_suite = Fernet(self.key)
        try:
            self.browser = webdriver.Chrome(executable_path=r"{}/chromedrivers/chromedriver".format(os.path.dirname(__file__)))
        except:
            self.browser = webdriver.Chrome(executable_path=r"{}/chromedrivers/chromedriver.exe".format(os.path.dirname(__file__)))

class BootCampLoginPage:
    def __init__(self, setup):
        self.browser = setup.browser
        # use the browser object to get the website
        self.browser.get('https://bootcampspot.com/login')
        # username element
        self.userbox = self.browser.find_element_by_xpath('//*[@id="emailAddress"]')
        # Password element
        self.pwbox = self.browser.find_element_by_xpath('//*[@id="password"]')
        # sign in button
        self.sign_in_button = self.browser.find_element_by_xpath('//*[@id="root"]/div/section/div/div[2]/button')
        setup.password = setup.cipher_suite.decrypt(setup.password).decode("utf-8")

    def login(self, username, password):
        # Action chain
        # Enter user_name/email
        actions = ActionChains(self.browser)
        actions.move_to_element(self.userbox)
        actions.click(self.userbox)
        actions.send_keys(setup.username)

        # Enter password
        actions.move_to_element(self.pwbox)
        actions.click(self.pwbox)
        actions.send_keys(setup.password)
        
        # Click sign-in
        actions.move_to_element(self.sign_in_button)
        actions.click(self.sign_in_button)
        actions.perform()
        return BootCampCheckinPage(self.browser)

class BootCampCheckinPage:
    def __init__(self, browser):
        self.browser = browser
        sleep(2)
        # if asked to do a survey, auto-fill it
        if self.check_exists_by_xpath('//*[@id="main-content"]/div[2]/section/div/div/div/button') == True:  
            try:
                # wait 10 seconds for the check-in button xpath element to load
                element = WebDriverWait(self.browser, 1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div/div/button'))
                )
                # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
                element.click()
                for i in range(15, 23):
                    element = WebDriverWait(self.browser, 1).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="{i}-4"]')))
                    element.click()
                # 10 hours outside of class studying
                actions = ActionChains(self.browser)
                self.additionalHours = self.browser.find_element_by_xpath('//*[@id="23"]')
                actions.move_to_element(self.additionalHours)
                actions.click(self.additionalHours)
                actions.send_keys('10')
                # add additional learning
                self.additionalLearning = self.browser.find_element_by_xpath('//*[@id="24"]')
                actions.move_to_element(self.additionalLearning)
                actions.click(self.additionalLearning)
                actions.send_keys('Additional learning')
                # click submit                
                self.submit = self.browser.find_element_by_xpath('//*[@id="main-content"]/div[2]/section/div/div/form/div/div/button')
                actions.move_to_element(self.submit)
                actions.click(self.submit)
                # Click Thank you!
                self.thanks = self.browser.find_element_by_xpath('//*[@id="main-content"]/div[2]/section/div/div/div/div/button')
                actions.move_to_element(self.thanks)
                actions.click(self.thanks)
                actions.perform()

            except Exception:
                # If the button is not found print a message to the user
                print('''WARNING: Could not complete survey''')
            ##### check the sessions page for a checkin button before printing the exception
        try:
            # wait 5 seconds for the check-in button xpath element to load
            element = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div[4]/div/div/div/div[3]/ul/li[3]/a'))
            )
            # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
            element.click()
        except Exception:
            # If the button is not found print a message to the user
            print('''WARNING: Did not find Check-in button! 
If you have not already checked-in, please re-run program or check-in manually''')

    def check_exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

        

  
if __name__ == '__main__':
    setup = Setup()
    loginpage = BootCampLoginPage(setup)
    checkinpage = loginpage.login(username,password)
    checkinpage.browser.close()

