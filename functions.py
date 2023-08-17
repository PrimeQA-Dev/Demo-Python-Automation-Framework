from selenium import webdriver


def Start_Driver(driver_name):
    if driver_name == "Chrome":
        return webdriver.Chrome()


def LOGIN(driver):
    # Login
    driver.get("https://www.flipkart.com")
    driver.maximize_window()

