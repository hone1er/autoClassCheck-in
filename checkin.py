import os
from time import sleep
from selenium import webdriver
from user import username, password
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# set webdriver to chrome
browser = webdriver.Chrome(executable_path=r"{}/chromedriver.exe".format(os.path.dirname(__file__)))
# use the browser object to get the website
browser.get('https://bootcampspot.com/login')


class BootCampLoginPage:
    def __init__(self, browser):
        self.browser = browser
        # username element
        self.userbox = browser.find_element_by_xpath('//*[@id="emailAddress"]')
        # Password element
        self.pwbox = browser.find_element_by_xpath('//*[@id="password"]')
        # sign in button
        self.sign_in_button = browser.find_element_by_xpath('//*[@id="root"]/div/section/div/div[2]/button')

    def login(self, username, password):
        # Action chain
        # Enter user_name/email
        actions = ActionChains(self.browser)
        actions.move_to_element(self.userbox)
        actions.click(self.userbox)
        actions.send_keys(username)

        # Enter password
        actions.move_to_element(self.pwbox)
        actions.click(self.pwbox)
        actions.send_keys(password)
        
        # Click sign-in
        actions.move_to_element(self.sign_in_button)
        actions.click(self.sign_in_button)
        actions.perform()
        return BootCampCheckinPage(self.browser)


class BootCampCheckinPage:
    def __init__(self, browser):
        self.browser = browser
        try:
            # wait 10 seconds for the check-in button xpath element to load
            element = WebDriverWait(self.browser, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div[4]/div/div/div/div[3]/ul/li[3]/a'))
            )
            # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
            element.click()
        except Exception:
            # If the button is not found print a message to the user
            print("Did not find Check-in button!")
  
if __name__ == '__main__':
    loginpage = BootCampLoginPage(browser)
    checkinpage = loginpage.login(username,password)
    checkinpage.browser.close()

