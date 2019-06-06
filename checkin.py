#! python3

import os
import tkinter as tk
from tkinter import ttk
from time import sleep
from user import username, pw
from selenium import webdriver
from popups import Popup, LoginFrame, Setup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class BootCampLoginPage:
    ''' initial bootcampspot.com page '''

    def __init__(self, setup):
        self.setup = setup
        # set webdriver to chrome. Try for mac, except for PC
        try:
            self.browser = webdriver.Chrome(
                executable_path=r"{}/chromedrivers/chromedriver".format(os.path.dirname(__file__)))
        except:
            self.browser = webdriver.Chrome(
                executable_path=r"{}/chromedrivers/chromedriver.exe".format(os.path.dirname(__file__)))
        # use the browser object to get the website
        self.browser.get('https://bootcampspot.com/login')

    def login(self, username, pw):
        # username element
        self.userbox = self.browser.find_element_by_xpath(
            '//*[@id="emailAddress"]')
        self.userbox.clear()
        # pw element
        self.pwbox = self.browser.find_element_by_xpath('//*[@id="password"]')
        self.pwbox.clear()
        # sign in button
        self.sign_in_button = self.browser.find_element_by_xpath(
            '//*[@id="root"]/div/section/div/div[2]/button')
        setup.pw = setup.driver_suite.decrypt(setup.pw).decode("utf-8")
        # Action chain
        # Enter user_name/email
        actions = ActionChains(self.browser)
        actions.move_to_element(self.userbox)
        actions.click(self.userbox)
        actions.send_keys(setup.username)

        # Enter pw
        actions.move_to_element(self.pwbox)
        actions.click(self.pwbox)
        actions.send_keys(setup.pw)

        # Click sign-in
        actions.move_to_element(self.sign_in_button)
        actions.click(self.sign_in_button)
        actions.perform()
        sleep(1)
        return self.verifyLogin()

    def verifyLogin(self):
        if self.browser.find_elements_by_xpath('//*[@id="root"]/div/section/div/div[2]/div/p'):
            msg = Popup(
                "Your email address or password is incorrect. Please try again.")
            root = Tk()
            lf = LoginFrame(root, self.setup)
            root.mainloop()
            return self.login(username, pw)
        return BootCampCheckinPage(self.browser)


class BootCampCheckinPage:
    ''' this webpage contains the check-in button '''

    def __init__(self, browser):
        self.browser = browser
        sleep(2)
        # if asked to do a survey, auto-fill it
        if self.check_exists_by_xpath('//*[@id="main-content"]/div[2]/section/div/div/div/button') == True:
            try:
                # wait 2 seconds for the take survey button xpath element to load then click it
                element = WebDriverWait(self.browser, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div/div/button'))
                )
                element.click()

                # for each survey question answer with 4 out of 5
                for i in range(15, 23):
                    element = WebDriverWait(self.browser, 1).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="{i}-4"]')))
                    element.click()

                # 10 hours outside of class studying
                actions = ActionChains(self.browser)
                self.additionalHours = self.browser.find_element_by_xpath(
                    '//*[@id="23"]')
                actions.move_to_element(self.additionalHours)
                actions.click(self.additionalHours)
                actions.send_keys('10')

                # add additional learning
                self.additionalLearning = self.browser.find_element_by_xpath(
                    '//*[@id="24"]')
                actions.move_to_element(self.additionalLearning)
                actions.click(self.additionalLearning)
                actions.send_keys('Additional learning')

                # click submit
                self.submit = self.browser.find_element_by_xpath(
                    '//*[@id="main-content"]/div[2]/section/div/div/form/div/div/button')
                actions.move_to_element(self.submit)
                actions.click(self.submit)
                actions.perform()
                sleep(1)
                # Click Thank you!
                element = WebDriverWait(self.browser, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/div/button')))
                element.click()

            except Exception:
                # If the survey is not completed print a message to the user
                msg = Popup(
                    "WARNING: Could not complete survey! \nIf you have not already checked-in, \nplease re-run program or check-in manually")

    # check the sessions page for a checkin button before printing the exception
    def login(self, attendance):
        if self.check_exists_by_xpath(f"//*[contains(text(), '{attendance}')]") == True:
            try:
                # Try to find the checkin button on the home page
                # wait 2 seconds for the check-in button xpath element to load
                element =self.browser.find_element_by_partial_link_text(f'{attendance}')
                # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
                element.click()
                msg = Popup("Check-in COMPLETE!!")
            except TimeoutException:
                msg = Popup(
                    "WARNING: Did not find Check-in button! \nIf you have not already checked-in, \nplease re-run program or check-in manually")
        else:
            try:
                # if the browser is full screen
                element = WebDriverWait(self.browser, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="root"]/div/nav/div[2]/nav/ul/li[2]/a'))
                )
                # the browser finds the element for the sessions, set it to the variable checkin_button and run the checkin method
                element.click()
                sleep(.5)
                # find check-in element
                checkInElement = self.browser.find_element_by_partial_link_text(f'{attendance}')
                checkInElement.click()
            except ElementNotVisibleException:
                try:
                    # if the browser is small
                    navelement = WebDriverWait(self.browser, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="root"]/div/div[1]'))
                    )
                    # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
                    navelement.click()
                    sleep(1)
                    sessions = self.browser.find_element_by_xpath(
                        '//*[@id="root"]/div/nav/div[2]/nav/ul/li[2]/a')
                    actions = ActionChains(self.browser)
                    actions.move_to_element(sessions)
                    actions.click(sessions)
                    actions.perform()

                    sleep(2)
                    checkInElement = self.browser.find_element_by_partial_link_text(f'{attendance}')
                    #checkInElement.click()
                    msg = Popup("Check-in COMPLETE!!")
                except Exception:
                    msg = Popup(
                        "WARNING: Did not find Check-in button! \nIf you have not already checked-in, \nplease re-run program or check-in manually")

    def check_exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

if __name__ == '__main__':
    setup = Setup()
    if hasattr(setup, 'attendance'):
        loginpage = BootCampLoginPage(setup)
        checkinpage = loginpage.login(username, pw)
        if setup.attendance == 'present':
            checkinpage.login('Check In To Class')
            loginpage.browser.close()
        elif setup.attendance == 'remote':
            checkinpage.login('Request Remote Attendance')
            loginpage.browser.close()
    quit()