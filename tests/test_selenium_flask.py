from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


# Lancement de Chrome
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# URL de l'app Flask
url = "http://127.0.0.1:5000/login"
driver.get(url)
time.sleep(1)

try:
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    submit_button = driver.find_element(By.TAG_NAME, "button")
    print("✅ Champs détectés.")
except NoSuchElementException as e:
    print("❌ Champ manquant :", e)


# attendre que le champ soit présent
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
username.clear()
username.send_keys("admin")

# Soumettre le formulaire avec de mauvais identifiants
driver.find_element(By.NAME, "username").send_keys("wrong")
driver.find_element(By.NAME, "password").send_keys("wrong")
driver.find_element(By.TAG_NAME, "button").click()

# Attendre que le message d'erreur apparaisse
error_msg = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "li"))
)
print("✅ Message d’erreur affiché pour mauvais identifiants.")

# Rechercher à nouveau les champs pour le test suivant
username = driver.find_element(By.NAME, "username")
password = driver.find_element(By.NAME, "password")
username.clear()
password.clear()
username.send_keys("admin")
password.send_keys("admin")


# Test mauvais identifiants
username.send_keys("admin")
password.send_keys("123")
submit_button.click()
time.sleep(1)

try:
    error_msg = driver.find_element(By.XPATH, "//p[contains(text(),'Identifiants invalides')]")
    if error_msg.is_displayed():
        print("✅ Message d’erreur affiché pour mauvais identifiants.")
except NoSuchElementException:
    print("❌ Message d’erreur introuvable")



# Test bons identifiants
username.clear()
password.clear()
username.send_keys("admin")
password.send_keys("passer123")
submit_button.click()
time.sleep(1)

if "dashboard" in driver.current_url:
    print("✅ Redirection vers le dashboard réussie")
else:
    print("❌ Redirection échouée")

driver.quit()
