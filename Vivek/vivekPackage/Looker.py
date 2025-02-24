import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# User inputs the dashboard name
Looker_Dashboard_Name = input("Enter the Dashboard name in Looker:")
print(Looker_Dashboard_Name)

dashboard_urls = {
    "Student_Details": "https://squareshift.cloud.looker.com/dashboards/321",
}

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://squareshift.cloud.looker.com/login")

try:
    email_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
    )
    email_element.send_keys("vivek@squareshift.co")
    print("✅ Email was entered.")
except:
    print("❌ Email was not entered.")

time.sleep(1)

try:
    password_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
    )
    password_element.send_keys("Qwerty@12345")
    print("✅ Password was entered.")
except:
    print("❌ Password was not entered.")

time.sleep(1)

try:
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
    )
    login_button.click()
    print("✅ Login button clicked.")
except:
    print("❌ Login button was not clicked.")

time.sleep(2)

try:
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@data-pendo-id='ExplorePanel']"))
    )
    print("✅ Home page loaded.")
except:
    print("❌ Home page did not load.")

if Looker_Dashboard_Name in dashboard_urls:
    driver.get(dashboard_urls[Looker_Dashboard_Name])
else:
    print("❌ Invalid Dashboard Name.")
    driver.quit()
    exit()

time.sleep(2)

try:
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, f"(//*[contains(text(),'{Looker_Dashboard_Name}')])[2]"))
    )
    print("✅ Dashboard loaded.")
except:
    print("❌ Dashboard did not load.")

time.sleep(2)

try:
    element_title = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[@data-testid='dashboard-tile-title']"))
    )
    element_title.click()
    print("✅ Element title clicked.")
except:
    print("❌ Element title was not clicked.")

time.sleep(2)

try:
    three_dots_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'ElementOverlay__VerticalIconContainer-sc')]"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(three_dots_menu).perform()
    three_dots_menu.click()
    print("✅ Hovered and clicked three dots menu.")
except:
    print("❌ Three dots menu was not clicked.")

time.sleep(2)

try:
    download_data_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Download data')]"))
    )
    download_data_button.click()
    print("✅ 'Download Data' button clicked.")
except:
    print("❌ 'Download Data' button was not clicked.")

time.sleep(2)

try:
    format_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='formatOption']"))
    )
    format_dropdown.click()
    time.sleep(1)
    format_dropdown.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    format_dropdown.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    format_dropdown.send_keys(Keys.ENTER)
    time.sleep(1)
    print("✅ Format set to CSV.")
except:
    print("❌ Failed to set format to CSV.")

time.sleep(1)

try:
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='qr-export-modal-download']"))
    )
    download_button.click()
    print("✅ Download button clicked.")
except:
    print("❌ Download button was not clicked.")

time.sleep(2)

download_path = f"C:\\Users\\User\\Downloads\\{Looker_Dashboard_Name}.csv"
timeout = 60
start_time = time.time()

while not os.path.exists(download_path):
    time.sleep(1)
    if time.time() - start_time > timeout:
        print("❌ Download failed: File not found.")
        driver.quit()
        exit()

print("✅ Success: CSV file downloaded!")
driver.quit()
