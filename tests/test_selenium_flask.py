# tests/test_selenium_flask.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.app import app as flask_app
from threading import Thread
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import app as flask_app

BASE_URL = "http://127.0.0.1:5000/login"

@pytest.fixture(scope="module")
def driver():
    """Initialise Chrome headless pour Selenium Remote WebDriver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    capabilities = options.to_capabilities()

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=capabilities
    )

    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def live_server():
    """Démarre le serveur Flask pour les tests"""
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": False
    })

    server = Thread(target=lambda: flask_app.run(port=5000))
    server.daemon = True
    server.start()
    time.sleep(1)  # Attendre que le serveur démarre
    yield
    # Pas besoin de join, le thread est daemon


def test_login_invalid(driver, live_server):
    driver.get(BASE_URL)

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password = driver.find_element(By.NAME, "password")

    username.send_keys("wrong")
    password.send_keys("wrong")
    driver.find_element(By.TAG_NAME, "button").click()

    error_msg = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Identifiants invalides')]"))
    )
    assert error_msg.is_displayed()
    print("✅ Message d’erreur affiché pour mauvais identifiants.")


def test_login_valid(driver, live_server):
    driver.get(BASE_URL)

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password = driver.find_element(By.NAME, "password")

    username.clear()
    password.clear()
    username.send_keys("admin")       # Identifiant correct
    password.send_keys("passer123")   # Mot de passe correct
    driver.find_element(By.TAG_NAME, "button").click()

    dashboard_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Bienvenue" in dashboard_text.text
    print("✅ Login valide fonctionne et dashboard accessible.")






