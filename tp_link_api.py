import time
import os
from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ENABLE_HEADLESS = True

load_dotenv()

ROUTER_IP = os.environ.get("ROUTER_IP")
ROUTER_PASSWORD = os.environ.get("ROUTER_PASSWORD")

opts = Options()
opts.headless = ENABLE_HEADLESS
opts.add_argument("--window-size=1920,1080")

browser = Firefox(options=opts)
browser.get(ROUTER_IP)


def login():
    # get input with id = "pc-login-password"
    password_input = browser.find_element(By.ID, "pc-login-password")

    # input password
    password_input.send_keys(ROUTER_PASSWORD)

    # get button with id = "pc-login-btn"
    login_button = browser.find_element(By.ID, "pc-login-btn")

    # click login button
    login_button.click()

    # get button with id = "confirm-yes"
    confirm_button = browser.find_element(By.ID, "confirm-yes")

    if confirm_button:
        # click confirm button
        confirm_button.click()

    # wait for page to load
    while True:

        try:
            browser.find_element(By.ID, "advanced")
            break
        except NoSuchElementException:
            time.sleep(0.5)

    time.sleep(3)


def activate_advanced():
    # get button with id = "advanced"
    advanced_button = browser.find_element(By.ID, "advanced")

    # click advanced button
    advanced_button.click()
    advanced_button.click()

    time.sleep(3)


def click_sms_tab():
    # get button with id = "sms"
    sms_button = browser.find_element(By.ID, "sms")

    # click sms button
    sms_button.click()


def click_new_sms_tab():
    # get button with id = "new-sms"
    new_sms_button = browser.find_element(By.LINK_TEXT, "New Message")

    # # click new sms button
    new_sms_button.click()


def input_number(number):
    # get input with id = "toNumber"
    number_input = browser.find_element(By.ID, "toNumber")

    # input number
    number_input.send_keys(number)


def input_message(message):
    # get input with id = "inputContent"
    message_input = browser.find_element(By.ID, "inputContent")

    # input message
    message_input.send_keys(message)


def send():
    # get button with id = "send"
    send_button = browser.find_element(By.ID, "send")

    # click send button
    send_button.click()

    while True:
        try:
            sms_sent_tooltip = browser.find_element(By.ID, "lteSmsTips-container")

            # get display stype of lteSmsTips-container
            style = sms_sent_tooltip.get_attribute("style")

            # if display is block, sms was sent
            if "display: block;" in style:
                return True
        except NoSuchElementException:
            pass

        try:
            # if login button is visible, login again
            browser.find_element(By.ID, "pc-login-btn")

            logger.info("Re-login required...")

            login()
            activate_advanced()
            click_sms_tab()
            click_new_sms_tab()

            logger.info("Logged in")
            return False

        except NoSuchElementException:
            pass
        time.sleep(0.1)


def init_sms():
    # this should only need to be done once

    logger.info("Starting tp-link router SMS service")

    login()
    activate_advanced()
    click_sms_tab()
    click_new_sms_tab()

    logger.info("tp-link router SMS service started")


def send_sms(number, message):
    sent = False
    while not sent:
        logger.info("Sending SMS to %s", number)

        input_number(number)
        input_message(message)

        sent = send()

    logger.info("SMS sent to %s", number)

# if __name__ == '__main__':
#     login()
#     activate_advanced()
#     click_sms_tab()
#     click_new_sms_tab()
#
#     input_number("0049123456789")
#     input_message("Hello World!")
#     send()
