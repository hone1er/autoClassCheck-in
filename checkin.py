#! python3

import os
import tkinter as tk
from tkinter import *
from time import sleep
from tkinter import ttk
from selenium import webdriver
import tkinter.messagebox as tm
from user import username, pw
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
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

                # Click Thank you!
                self.thanks = self.browser.find_element_by_xpath(
                    '//*[@id="main-content"]/div[2]/div/button')
                actions.move_to_element(self.thanks)
                actions.click(self.thanks)
                actions.perform()

            except Exception:
                # If the survey is not completed print a message to the user
                msg = Popup(
                    "WARNING: Could not complete survey! \nIf you have not already checked-in, \nplease re-run program or check-in manually")

    # check the sessions page for a checkin button before printing the exception
    def present(self):
        try:
            # wait 2 seconds for the check-in button xpath element to load
            element = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div[4]/div/div/div/div[3]/ul/li[3]/a'))
            )
            # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
            element.click()
            msg = Popup("Check-in COMPLETE!!")
        except Exception:
            # If the button is not found print a message to the user
            msg = Popup(
                "WARNING: Did not find Check-in button! \nIf you have not already checked-in, \nplease re-run program or check-in manually")

    def remoteAttendance(self):
        try:
            # wait 2 seconds for the check-in button xpath element to load
            remote = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main-content"]/div[2]/section/div/div[4]/div/div/div/div[3]/ul/li[2]/a'))
            )
            # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
            remote.click()

 # check if anything else needs to be clicked after remote attendance
            checkbox = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="agree"]'))
            )
            # the browser finds the element for checkin, set it to the variable checkin_button and run the checkin method
            checkbox.click()

            confirm = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main-content"]/div[2]/section/div[2]/div[3]/div/button[1]'))
            )
            confirm.click()

            msg = Popup("Remote Request COMPLETE!!")

        except Exception:
            # If the button is not found print a message to the user
            msg = Popup(
                "WARNING: Did not find Check-in button! \nIf you have not already checked-in, \nplease re-run program or check-in manually")

    def check_exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


class Setup:
    ''' setup for user and web driver '''

    def __init__(self):
        # Pop up and buttons asking if student is in class, not in class, or attending remotely
        self.popup = tk.Tk()
        self.popup.wm_title("Are you in class??")
        label = ttk.Label(
            self.popup, text="Are you currently in class & connected to wifi?", font=("Verdana", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self.popup, text="Yes", command=self.yes)
        B2 = ttk.Button(self.popup, text="No", command=self.no)
        B3 = ttk.Button(
            self.popup, text="Request Remote attendance", command=self.remote)
        B1.pack()
        B2.pack()
        B3.pack()
        self.popup.mainloop()

        self.username = username
        self.pw = pw
        self.driver = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
        self.driver_suite = Fernet(self.driver)

        # if there is no username or password open a dialog box that request username and password
        if self.username == None or self.pw == None:
            root = Tk()
            lf = LoginFrame(root, self)
            root.mainloop()

    def remote(self):
        self.popup.destroy()
        self.attendance = 'remote'

    def no(self):
        self.popup.destroy()
        quit()

    def yes(self):
        self.attendance = 'present'
        self.popup.destroy()

# Login popup if username or pw needs to be input.


class LoginFrame(Frame):
    ''' popup that request username and password if there is none available or it is incorrect '''

    def __init__(self, master, setup):
        super().__init__(master)
        self.master = master
        self.setup = setup
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login",
                             command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        self.setup.username = self.entry_username.get()
        self.setup.pw = self.setup.driver_suite.encrypt(
            bytes(self.entry_password.get().encode('utf-8')))
        with open('user.py', 'w') as file:
            file.write(f'username = "{self.setup.username}"\n')
            file.write(f'pw = {self.setup.pw}\n')
        self.master.destroy()


class Popup:
    ''' popup for warnings and success messages '''

    def __init__(self, msg):
        self.popup = tk.Tk()
        self.popup.wm_title("Check-in Status")
        label = ttk.Label(self.popup, text=msg, font=("Verdana", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self.popup, text="Okay", command=self.buttoncmd)
        B1.pack()
        self.popup.mainloop()

    def buttoncmd(self):
        self.popup.destroy()


if __name__ == '__main__':
    setup = Setup()
    if hasattr(setup, 'attendance'):
        loginpage = BootCampLoginPage(setup)
        checkinpage = loginpage.login(username, pw)
        if setup.attendance == 'present':
            checkinpage.present()
            loginpage.browser.close()
        elif setup.attendance == 'remote':
            checkinpage.remoteAttendance()
            loginpage.browser.close()
    quit()
