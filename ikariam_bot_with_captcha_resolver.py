"""Module providingFunction printing python version."""
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import urllib
import os
from python_anticaptcha import NoCaptchaTaskProxylessTask
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains


email = 'XXX'
password = 'YYY'
api_key = 'ZZZ'
url = 'https://lobby.ikariam.gameforge.com/pl_PL/'


captcha_exist = False
pirate_house_exist = False
abord_btn_exist = False
abord_captcha_btn_exist = False
wait_time = 150


def log_in(login, password):

    # Write login
    search_input_login = driver.find_element(
        "xpath", '//*[@id="registerForm"]/div[2]/div/input')
    # time.sleep(1)
    search_input_login.send_keys(login)

    # Write password
    search_input_pass = driver.find_element(
        "xpath", '//*[@id="registerForm"]/div[3]/div/input')
    # time.sleep(1)
    search_input_pass.send_keys(password)

    # Change tab from registration to login
    login_tab = driver.find_element(
        "xpath", '//*[@id="loginRegisterTabs"]/ul/li[1]')
    # time.sleep(1)
    login_tab.click()

    # Click login
    login_btn = driver.find_element(
        "xpath", '//*[@id="loginForm"]/p/button[1]')
    # time.sleep(1)
    login_btn.click()
    time.sleep(5)


def close_cookie():
    try:
        cookie_btn = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/span[2]/button[2]')
    except NoSuchElementException:
        print('Cookie button has not been found\n')
    else:
        cookie_btn.click()
        time.sleep(1)


def close_promo():
    # Check if promotion windows exist and close it
    try:
        temp_btn = driver.find_element(
            "xpath", '//*[@id="multiPopup"]/div[2]/div[2]/a')
    except NoSuchElementException:
        time.sleep(1)
    else:
        temp_btn.click()
        print('Promo window has been found and closed\n')
        time.sleep(1)


def click_play_btn():

    play_btn = driver.find_element("xpath", '//*[@id="joinGame"]/button')
    play_btn.click()


def search_pirate_house():
    global pirate_house_exist
    global pirate_house
    try:
        prt_hs = driver.find_element(
            "xpath", '//*[@id="js_CityPosition17Link"]')
    except NoSuchElementException:
        pirate_house_exist = False
        print('Pirate house has not been found.\n')
        driver.refresh()
        time.sleep(2)
        pirate_house = search_pirate_house()
    else:
        pirate_house_exist = True
        time.sleep(1)
        print('Pirate house has been found. Going in!\n')
        return prt_hs


def search_abord_btn():
    global abord_btn_exist
    global wait_time
    try:
        abord_btn = driver.find_element(By.CLASS_NAME, 'button.capture')
    except NoSuchElementException:
        abord_btn_exist = False
        wait_time = wait_time + 5
        print(
            '"Abort" button has not been found!(Current waiting time='+str(wait_time-6)+')\n')
        driver.refresh()
        time.sleep(6)
    else:
        abord_btn_exist = True
        wait_time = wait_time - 6

        if (wait_time < 155):
            wait_time = 155

        print('Start boarding! Arghhh!!!\n')
        abord_btn.click()
        time.sleep(2)


def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']  # + 100
    top = location['y']  # + 100
    right = location['x'] + size['width']  # + 290
    bottom = location['y'] + size['height']  # + 150

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image
    return image


def check_for_captcha():
    global captcha_exist
    try:
        captcha_answer = driver.find_element(By.NAME, 'captcha')
    except:
        print('Captcha not found\n')
        captcha_exist = False
    else:
        print('Captcha has been found!\n')
        captcha_exist = True


def resolve_captcha():
    global captcha_exist
    captcha_answer = driver.find_element(By.NAME, 'captcha')

    try:
        abord_after_captcha = driver.find_element(
            "xpath", '//*[@id="pirateCaptureBox"]/div[1]/form/div[2]/input')
    except NoSuchElementException:
        slider = driver.find_element(
            By.XPATH, '//*[@id="pirateFortress"]/div[2]/div[1]/div[2]')
        action = ActionChains(driver)
        action.drag_and_drop_by_offset(slider, 0, 90).perform()
        abord_after_captcha = driver.find_element(
            "xpath", '//*[@id="pirateCaptureBox"]/div[1]/form/div[2]/input')

    try:
        img = driver.find_element(
            By.XPATH, '//*[@id="pirateCaptureBox"]/div[1]/form/img')
    except NoSuchElementException:
        captcha_exist = False
    else:
        image = get_captcha(driver, img, "captcha.png")
        DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE = "{}/captcha.png".format(DIR)
        captcha_fp = open(IMAGE, "rb")

        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        global job
        job = client.createTask(task)
        job.join()

        result = job.get_captcha_text()

        captcha_answer = driver.find_element(By.NAME, 'captcha')
        captcha_answer.send_keys(result)

        time.sleep(2)

        abord_after_captcha = driver.find_element(
            "xpath", '//*[@id="pirateCaptureBox"]/div[1]/form/div[2]/input')
        abord_after_captcha.click()

    # check_for_captcha()
    # if (captcha_exist is True):
    #    resolve_captcha()
    time.sleep(2)
    driver.refresh()
    time.sleep(2)


def wait(tim):
    for x in range(tim):
        time.sleep(1)
        print(str(tim-x))


def goto_main_city():

    check_var = False

    while check_var == False:
        try:
            goto_city = driver.find_element(
                By.XPATH, '//*[@id="js_cityLink"]/a')
        except NoSuchElementException:
            driver.refresh()
            time.sleep(1)
        else:
            goto_city.click()
            time.sleep(1)

            try:
                list = driver.find_element(
                    By.XPATH, '//*[@id="js_citySelectContainer"]/span')
            except NoSuchElementException:
                driver.refresh()
                time.sleep(1)
            else:
                list.click()
                time.sleep(1)

                try:
                    first_city = driver.find_element(
                        By.CSS_SELECTOR, '#dropDown_js_citySelectContainer > div.bg > ul > li.ownCity.coords.first-child')
                except NoSuchElementException:
                    driver.refresh()
                    time.sleep(1)
                else:
                    try:
                        first_city.click()
                        time.sleep(1)
                    except ElementNotInteractableException:
                        continue
                    else:
                        check_var = True

    time.sleep(1)


############# MAIN PROGRAM#############
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

time.sleep(2)

log_in(email, password)
close_cookie()
click_play_btn()

time.sleep(5)
driver.switch_to.window(driver.window_handles[1])

close_promo()

for i in range(5000):

    pirate_house = search_pirate_house()
    if (pirate_house_exist == True):
        pirate_house.click()
        time.sleep(2)
    else:
        print(pirate_house_exist)

    search_abord_btn()

    if (abord_btn_exist == True):

        check_for_captcha()
        if (captcha_exist is True):

            resolve_captcha()
            check_for_captcha()
            while captcha_exist == True:
                job.report_incorrect_recaptcha
                resolve_captcha()
                check_for_captcha()

            print('Captcha has been resolved\n')
            print('Waiting '+str(wait_time)+'s\n')
            wait(wait_time)
            print('Waiting is over\n')

            time.sleep(2)
            goto_main_city()

        elif (captcha_exist is False):
            print('Waiting '+str(wait_time)+'s\n')
            wait(wait_time)
            print('Waiting is over\n')

            time.sleep(2)
            goto_main_city()


