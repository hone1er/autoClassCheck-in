from time import sleep
from selenium import webdriver
from user import username, password
from selenium.webdriver.common.action_chains import ActionChains

# set webdriver to chrome
browser = webdriver.Chrome()
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
        self.checkin_button = browser.find_element_by_xpath('//*[@id="main-content"]/div[2]/section/div/div[4]/div/div/div/div[3]/ul/li[3]')

    def checkin(self):
        actions = ActionChains(self.browser)
        actions.click(self.checkin_button)


if __name__ == '__main__':
    loginpage = BootCampLoginPage(browser)
    checkinpage = loginpage.login(username,password).checkin()

