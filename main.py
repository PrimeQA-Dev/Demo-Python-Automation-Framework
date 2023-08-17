from contextlib import contextmanager
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import sys
import datetime
import functions
import os
import logging
import time
import pandas as pd
from pretty_html_table import build_table
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


Today_date = datetime.date.today()
One_Day = datetime.timedelta(days=1)
Yesterday = Today_date - One_Day
YESTERDAY_DATE = Yesterday.strftime('%Y-%m-%d_%H-%M-%S')

# Make new directory
TODAYS_FOLDER = (datetime.datetime.now()).strftime('%Y-%m-%d_%H-%M-%S')
YESTERDAY_F0LDER = YESTERDAY_DATE
try:
    for directory in os.listdir():
        if os.path.exists(YESTERDAY_F0LDER):
            os.mkdir(TODAYS_FOLDER)
            Screenshot_path = os.path.join(os.getcwd(), TODAYS_FOLDER)
        else:
            Screenshot_path = os.path.join(os.getcwd(), YESTERDAY_F0LDER)

except Exception as e:
    logging.error(e)
    Screenshot_path = os.path.join(os.getcwd(), TODAYS_FOLDER)

LOGGER_FILENAME = os.path.join(os.getcwd(), str(Today_date) + "-Demo.txt")
logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d][%(levelname)s]:[%(lineno)s] - %(message)s",
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(LOGGER_FILENAME, 'a'),
        logging.StreamHandler()
    ])

SENDER_MAIL = 'TestMailPrimeQA@gmail.com'
SENDER_PWD = 'pzvjbtwvwcodzphu'
Tester = 'vikas@primeqasolutions.com'
cc = 'devanshi@primeqasolutions.com'
Recipents = cc.split(",") + [Tester]


# -----------------
SuccessCount = 0
FailureCount = 0
SkippedCount = 0
Success_List = []
Failure_Cause = []
Execution_time = []

# ---------- XPATH'S --------------
LOGIN_BUTTON = '//a[text()="Login"]'
SEARCH_BAR = '//input[@name="q"]'
CROSS_ICON = '//button[text()="✕"]'


def test_case_01():
    with services_context_wrapper("test_case_1.png", "Start Test Case 1", "End for Test Case 1",
                                  "TC_01", "Open Flipkart and search product") as driver:
        driver.maximize_window()
        functions.LOGIN(driver)
        driver.implicitly_wait(10)
        act_title = driver.find_element(
            By.XPATH, LOGIN_BUTTON
        ).text
        assert act_title == "Login"
        logging.info("Login is successful.")
        rt_value = driver.find_element(
            By.XPATH, LOGIN_BUTTON      
        ).is_displayed()
        assert rt_value
        # click at crossbar
        (WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, CROSS_ICON))).click())
        # Search the product in search bar and click the Enter
        (WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, SEARCH_BAR))).send_keys("iphone",
                                                                                                           Keys.ENTER))
        # Result
        result = driver.find_elements(By.XPATH, '//div[@class="_4rR01T"]')
        logging.info(len(result))
        assert len(result) >= 1
        logging.info("We have got the more then one results")
        Success_List_Append("TC_01", "Open flipkart and search the product", "Pass")


def test_case_02():
    with services_context_wrapper("test_case_2.png", "Start Test Case 2", "End for Test Case 2", "TC_02",
                                  "Open Flipkart and search product") as driver:
        driver.maximize_window()
        functions.LOGIN(driver)
        driver.implicitly_wait(10)
        act_title = driver.find_element(
            By.XPATH, LOGIN_BUTTON
        ).text
        assert act_title == "gin"
        logging.info("Login is successful.")
        rt_value = driver.find_element(
            By.XPATH, LOGIN_BUTTON
        ).is_displayed()
        assert rt_value
        # click at crossbar
        (WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[tex()="X"]'))).click())
        # Search the product in search bar and click the Enter
        (WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, SEARCH_BAR))).send_keys("iphone",
                                                                                                           Keys.ENTER))
        # Result
        result = driver.find_elements(By.XPATH, '//div[@class="_4rR01T"]')
        logging.info(len(result))
        assert len(result) >= 1
        logging.info("We have got the more then one results")
        Success_List_Append("TC_02", "Open flipkart and search the product", "Pass")


@contextmanager
def services_context_wrapper(screenshot, TESTCASE_START, TESTCASE_END, testID, description):
    global driver
    try:
        st = time.time()
        logging.info(TESTCASE_START)
        # c = Options()
        # c.add_argument("--headless")
        driver = webdriver.Chrome()
        yield driver
    except Exception as e:
        logging.info("-- Entered into the failure part--")
        logging.error(f"Error: {e}")
        Failure_Cause_Append(driver, testID, description, e, screenshot)
        Success_List_Append(testID, description, "Fail")
        logging.info(testID)
    finally:
        driver.quit()
        et = time.time()
        elapsed_time = round((et - st), 2)
        logging.info('Execution time:' + str(elapsed_time))
        Execution_time.append([str(elapsed_time)])
        logging.info(TESTCASE_END)


def Success_List_Append(testID, description, results):
    global SuccessCount, FailureCount, driver
    Success_List.append([testID, description, results])
    if results == "Pass":
        SuccessCount += 1
        logging.info(testID)
        logging.info("Success Count = " + str(SuccessCount))


def Failure_Cause_Append(driver, testID, description, failureCause, screenshot=None):
    global SuccessCount, FailureCount
    Failure_Cause.append([testID, description, failureCause])
    FailureCount += 1
    logging.info(testID)
    if screenshot:
        driver.save_screenshot(Screenshot_path + "\\" + screenshot + ".png")
    logging.info("Failure Count = " + str(FailureCount))


def TestReport_Generation():
    global Test_Report_Table
    driver = webdriver.Chrome()
    logging.info("Entered into TestReport_Generation()")
    Test_Report = [["Project Name", "Demo"], ["Test Type", "Automation"], ["Browser Used", "Chrome"],
                   ["Browser Version", driver.capabilities['browserVersion']],
                   ["Test Execution Start Time", Execution_StartTime],
                   ["Test Execution End Time", Execution_EndTime], ["Test Pass", SuccessCount],
                   ["Test Fail", FailureCount],
                   ["Total Test Cases", int(SuccessCount + FailureCount)]]
    Test_Report_DF = pd.DataFrame(Test_Report, columns=("Summary", "Details"))
    Test_Report_Table = build_table(Test_Report_DF, "blue_dark", text_align='justify')
    driver.quit()
    logging.info("Exiting from TestReport_Generation()")


def Summary_Table_Formation():
    global Summary_Table
    global Failure_Cause_Table
    global SocialWall_table_DF
    SocialWall_table_DF = pd.DataFrame(Success_List, columns=["Test Case No.", "Test Cases Summary", "Results"])
    Execution_table_DF = pd.DataFrame(Execution_time, columns=["Execution Time(sec)"])
    Summary_table_DF = pd.concat([SocialWall_table_DF, Execution_table_DF], axis=1, join='inner')
    Summary_Table = build_table(Summary_table_DF, "green_dark", text_align='justify')
    if Failure_Cause != "[]":
        Failure_Cause_Table_DF = pd.DataFrame(Failure_Cause,
                                              columns=["TestCasez No.", "TestCases Summary", "Failure Cause"])
        Failure_Cause_Table = build_table(Failure_Cause_Table_DF, "red_dark", text_align='center')


def Send_Mail():
    logging.info("Sending Mail...........")
    message = MIMEMultipart()
    message['Subject'] = 'Demo Results'
    message['From'] = SENDER_MAIL
    message['To'] = Tester
    message['Cc'] = cc
    if FailureCount != 0:
        empanelled = "<p>Failure Cause Table</p><div style='height: 700px; overflow: auto; width: fit-content'>" + Failure_Cause_Table + "</div>"
    else:
        empanelled = "<p>No Failure Observed.</p>"
    html = """\
        <html>
          <head></head>
          <body>
            <p>Hi,<br>
                Please find below Test Report for Automation Testing
            </p>
            <p>Test Report/Details
            </p>
            <div>""" + Test_Report_Table + """
            </div>
            <p>Summary Table
            </p>
            <div style='height: 700px; overflow: auto; width: fit-content'>""" + Summary_Table + """
            </div>
            <p>""" + empanelled + """</p>
            <p>THIS IS SYSTEM GENERATED MAIL.</p>
            <p></p>
          </body>
        </html>
        """

    part2 = MIMEText(html, 'html')
    message.attach(part2)
    msg_body = message.as_string()
    try:
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], SENDER_PWD)
        server.sendmail(message['From'], Recipents, msg_body)
        server.quit()
        logging.info("Mail Sent successfully")
    except Exception as e_mail:
        logging.error("Mail sending Failed")
        logging.error(e_mail)


def main():
    global Execution_StartTime
    global Execution_EndTime
    global Screenshot_Folder

    Execution_StartTime = datetime.datetime.now()

    test_case_01()
    test_case_02()

    Execution_EndTime = datetime.datetime.now()
    TestReport_Generation()
    Summary_Table_Formation()
    Send_Mail()


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(1)

