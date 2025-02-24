import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Enter the Dashboard name in Tableau
Tableau_Dashboard_Name = input("Enter the Dashboard name in Tableau:")
print(Tableau_Dashboard_Name)

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep browser open after execution

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Open the given URL
url = "https://sso.online.tableau.com/public/login"
driver.get(url)

# **1️⃣ Enter Email**
try:
    email_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='email']"))
    )
    email_element.send_keys("vishnuprakash@squareshift.co")
    print("✅ Email entered successfully!")
except:
    print("❌ Email input element did not appear within the timeout.")

# **2️⃣ Click the Sign In button**
try:
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='login-submit']"))
    )
    login_button.click()
    print("✅ Login button clicked!")
except:
    print("❌ Login button did not appear within the timeout.")

# **3️⃣ Enter URI**
try:
    uri_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='site-uri']"))
    )
    uri_element.send_keys("vishnuprakash-ce8986c494")
    print("✅ URI entered successfully!")
except:
    print("❌ URI input element did not appear within the timeout.")

# **4️⃣ Click the Continue button**
try:
    verify_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='verify-button']"))
    )
    verify_button.click()
    print("✅ Continue button clicked!")
except:
    print("❌ Continue button did not appear within the timeout.")

# **5️⃣ Wait for the promo content**
try:
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='login-promo__content']"))
    )
    print("✅ Promo content is visible!")
except:
    print("❌ Promo content did not appear within the timeout.")

# **6️⃣ Enter Password**
try:
    password_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    password_field.send_keys("Vishnu@2001")
    print("✅ Password entered successfully!")
except:
    print("❌ Password input element did not appear within the timeout.")

# **7️⃣ Click the final Sign In button**
try:
    final_login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    final_login_button.click()
    print("✅ Signed in successfully!")
except:
    print("❌ Final login button did not appear within the timeout.")

# **8️⃣ Wait & Navigate to the Tableau Dashboard**
time.sleep(7)
dashboard_url = f"https://prod-apnortheast-a.online.tableau.com/#/site/vishnuprakash-ce8986c494/views/Student_Details/Sheet1?:iid=3"
driver.get(dashboard_url)
time.sleep(2)

driver.refresh()

time.sleep(10)

# # **9️⃣ Wait for the iframe & Switch to it**

try:
    # Wait for the toolbar to load
    toolbar = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "viz-viewer-toolbar-items-container"))
    )

    # Hover over the toolbar to make buttons appear
    actions = ActionChains(driver)
    actions.move_to_element(toolbar).perform()

    # Wait for the download button to appear
    download_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "download"))
    )

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)

    # Try a normal click
    try:
        download_button.click()
        print("✅ Download button clicked successfully!")
    except:
        # If normal click fails, use JavaScript click
        driver.execute_script("arguments[0].click();", download_button)
        print("✅ Clicked using JavaScript!")

except Exception as e:
    print(f"❌ Failed to click download button: {e}")

time.sleep(3)
# **1️⃣1️⃣ Wait for Crosstab Option & Click**
try:
    crosstab_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='frvoegc'][contains(.,'Crosstab')]"))
    )
    crosstab_option.click()
    print("✅ Crosstab option clicked!")
except:
    print("❌ Crosstab option did not appear within the timeout.")

# **1️⃣2️⃣ Wait for CSV Option & Click**
try:
    csv_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='f1u2kjnq'][contains(.,'CSV')]"))
    )
    csv_option.click()
    print("✅ CSV format selected!")
except:
    print("❌ CSV format option did not appear within the timeout.")

# **1️⃣3️⃣ Wait for 1 second & Click the Final Download Button**
time.sleep(1)
try:
    final_download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-tb-test-id='export-crosstab-export-Button']"))
    )
    final_download_button.click()
    print("✅ Download started!")
except:
    print("❌ Final download button did not appear within the timeout.")

# **1️⃣4️⃣ Wait for the CSV File to Download**
download_path = f"C:\\Users\\User\\Downloads\\{Tableau_Dashboard_Name}.csv"
timeout = 60  # Wait up to 60 seconds for download
start_time = time.time()

while not os.path.exists(download_path):
    time.sleep(1)
    if time.time() - start_time > timeout:
        print("❌ Download failed: File not found")
        driver.quit()
        exit()

print("✅ Success: CSV file downloaded!")

# **🎯 Close the browser**
driver.quit()
