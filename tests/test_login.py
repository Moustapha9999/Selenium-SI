import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

BASE_URL = "http://127.0.0.1:5000/login"

def test_login_page_loads(driver):
    driver.get(BASE_URL)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    submit_button = driver.find_element(By.TAG_NAME, "button")
    assert username and password and submit_button

def test_wrong_login_shows_error(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    error_msg = driver.find_element(By.XPATH, "//p[contains(text(),'Identifiants invalides')]")
    assert error_msg.is_displayed()

def test_correct_login_redirects(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("passer123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    assert "dashboard" in driver.current_url
