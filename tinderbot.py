#!/python3
########################################################

from selenium import webdriver
from time import sleep
from time import time as timer
import numpy as np

# -- extract credentials from ./secrets.py
from secrets import username, password 

########################################################

class TinderBot():
    """My awesome Tinder swipe bot"""

    # -- conditions for match:
    conditions = {
        "age": {
            "min": 23,
            "max": 39,
        },
        "distance": {
            "min": 0,
            "max": 8,
        },
    }

    # -- counters
    nlikes = 0
    ndislikes = 0
    nmatches = 0
    total_time = 0

    # -- base window
    base_window = None

    def __init__(self):
        chromedriver_loc = "./chromedriver.exe" # -- assuming chromedriver is in this directory
        
        options = webdriver.ChromeOptions()
        #options.add_argument("--disable-dev-shm-usage")
    	
        self.driver = webdriver.Chrome(chromedriver_loc, chrome_options=options)
        self.driver.get('https://tinder.com')
        print("loaded tinder.")

    def login(self):
        print("logging in...")
        fb_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        fb_button.click()

        # save base-window 
        self.base_window = self.driver.window_handles[0]
        try:
            # switch to pop-up window
            print("switch to pop-up login window.")
            self.driver.switch_to.window(self.driver.window_handles[1])

            # input credentials
            email_field = self.driver.find_element_by_xpath('//*[@id="email"]')
            password_field = self.driver.find_element_by_xpath('//*[@id="pass"]')

            # insert login credentials
            print("entering credentials.")
            email_field.send_keys(username)
            password_field.send_keys(password)

            # enter login
            login_button = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
            login_button.click()
            print("logged in.")

            # switch back to base window
            print("switching back to base window")
            self.driver.switch_to.window(self.base_window)
        except Exception as e:
            print(e)
            pass

    def like(self):
        print("like")
        btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        btn.click()
        self.nlikes += 1
        sleep(0.5)
    
    def dislike(self):
        print("dislike")
        btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        btn.click()
        self.ndislikes += 1
        sleep(0.5)

    def say_something_nice(self, input_text: str = "Hei :)"):
        """It's a match! Say something nice!"""
        textarea = self.driver.find_element_by_xpath('//*[@id="chat-text-area"]')
        textarea.send_keys(input_text)
        send_form_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button')
        send_form_btn.click()
        print("Match: just said somethig nice: {}".format(input_text))
        self.nmatches += 1
        sleep(0.5)

    def print_stats(self):
        tt = np.modf(self.total_time/60)
        minutes = int(tt[1])
        seconds = int(tt[0] * 60)
        time = "{:02d}:{:02d}".format(minutes, seconds)
        print("""
=================================
    matches  : {}
    likes    : {}
    dislikes : {}
    time     : {}
=================================
        """.format(self.nmatches, self.nlikes, self.ndislikes, time))

    def auto_swipe(self):
        t0 = timer()
        while True:
            try:
                profile_info = self.get_profile_info()
                test_conditions_have_been_met = self.run_tests(profile_info)
            except:
                    # 1) it's a match -> Say something nice!
                    self.say_something_nice()
                    self.total_time = timer() - t0
                    self.print_stats()
                    continue

            sleep(0.5)
            if test_conditions_have_been_met:
                self.like()
            else:
                self.dislike()

    def run_tests(self, profile_info: dict) -> bool:
        """Test if profile_info contitions are met"""
        
        print("running tests...")
        all_conditions_met = True

        for key in self.conditions.keys():
            try:
                entry = profile_info[key]
                if type(self.conditions[key]) == type(dict()):
                    # -- check if entry is between conditional boundaries
                    condition_met = (self.conditions[key]["min"] <= entry <= self.conditions[key]["max"])
                    if not condition_met:
                        all_conditions_met = False
                        break
                else:
                    # -- condition should be a True/False statement
                    if self.conditions[key]:
                        if profile_info[key] is None:
                            # profile_info is not existing
                            all_conditions_met = False
                            break
            except:
                pass

        print("done.")
        return all_conditions_met

    def get_profile_info(self) -> dict:
        """get profile info"""
        print("get profile info...")

        data = {
            "name": None,
            "age": None,
            "description": None,
            "distance": None,
            "education": None,
            "info": [],
        }

        try:
            name = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span')
            data["name"] = name.text
        except:
            pass

        try:            
            age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span')
            data["age"] = int(age.text)
        except:
            pass

        sleep(0.2)
        ibtn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')
        ibtn.click()

        base = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/'
        for i in range(1,6):
            try:
                row = self.driver.find_element_by_xpath(base + 'div[{}]/div[2]'.format(i))
                data["info"].append(row.text)
            except:
                print(i)
                break

        try:
            desc = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/span')
            data["description"] = desc.text
        except:
            pass

        sleep(0.1)
        back_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[1]')
        back_btn.click()

        ##############################
        # extract data from info list

        school_name_list = ['høyskole', 'høyskolen', 'universitet', 'university', 'college', 'school', 'institute']
        if len(data["info"]) > 0:
            for i in data["info"]:
                v = i.split()
                if ('kilometers' in v and 'away' in v):
                    data["distance"] = int(v[0])
                else:
                    education = False
                    for element in v:
                        if (element.lower() in school_name_list): 
                            education = True
                    if education:
                        data["education"] = i

        print("done.")
        return data
