from flask import Flask, request, jsonify
import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
import os
import logging
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
app = Flask(__name__)

def run_selenium_test(tableau_dashboard_name, looker_dashboard_name):
    # Capture print() output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        print(f"✅ Validating Tableau dashboard: {tableau_dashboard_name}")
        print(f"✅ Validating Looker dashboard: {looker_dashboard_name}")
        print("🚀 Starting Validation...")

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)  # Keep browser open after execution

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)

        # Open the given URL
        print("✅ NoW opening the Tableau Site to download the CSV file")

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

        time.sleep(12)

        # # **9️⃣ Wait for the iframe & Switch to it**

        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))  # Check if any iframe is present
        )
        driver.switch_to.frame(iframe)
        print("✅ Switched to the detected iframe!")

        time.sleep(6)

        # **🔟 Wait for Download Button & Click**
        max_attempts = 3  # Number of retry attempts
        attempt = 0  # Initialize attempt counter

        while attempt < max_attempts:
            try:
                # Wait for the button to be present in the DOM
                download_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@id='download']"))
                )

                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                time.sleep(1)  # Allow time for any animations

                # Ensure the button is clickable
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='download']"))
                )

                # Remove any overlay issues
                driver.execute_script("arguments[0].style.pointerEvents = 'auto';", download_button)

                # Try clicking the button normally
                try:
                    download_button.click()
                except:
                    # Use JavaScript click if normal click fails
                    driver.execute_script("arguments[0].click();", download_button)

                print(f"✅ Download button clicked on attempt {attempt + 1}")
                break  # Exit loop on success

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        time.sleep(3)

        if attempt == max_attempts:
            print("❌ Failed to click the download button after multiple attempts.")

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
        download_path = f"C:\\Users\\User\\Downloads\\{tableau_dashboard_name}.csv"
        timeout = 60  # Wait up to 60 seconds for download
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                print("❌ Download failed: File not found")
                driver.quit()
                exit()

        print("✔️✔️✔️✔️✔️✔️ Tableau CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️")

        print("✅ NoW opening the Looker Site to download the CSV file")

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

        time.sleep(2)

        driver.get("https://squareshift.cloud.looker.com/dashboards/321")

        time.sleep(3)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"(//*[contains(text(),'{looker_dashboard_name}')])[2]"))
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

        time.sleep(3)

        max_attempts = 3  # Number of retry attempts
        attempt = 0  # Initialize attempt counter

        while attempt < max_attempts:
            try:
                # Wait for the three dots menu to be present in the DOM
                three_dots_menu = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(@class, 'ElementOverlay__VerticalIconContainer-sc')]"))
                )

                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", three_dots_menu)
                time.sleep(1)  # Give time for UI to settle

                # Hover over the menu
                actions = ActionChains(driver)
                actions.move_to_element(three_dots_menu).perform()
                time.sleep(1)  # Allow time for hover effects

                # Ensure the button is clickable
                three_dots_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class, 'ElementOverlay__VerticalIconContainer-sc')]"))
                )

                # Remove any overlay issues
                driver.execute_script("arguments[0].style.pointerEvents = 'auto';", three_dots_menu)

                # Click the menu
                try:
                    three_dots_menu.click()
                except:
                    # Use JavaScript click if normal click fails
                    driver.execute_script("arguments[0].click();", three_dots_menu)

                print(f"✅ Hovered and clicked three dots menu on attempt {attempt + 1}")
                break  # Exit loop on success

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        if attempt == max_attempts:
            print("❌ Failed to click the three dots menu after multiple attempts.")

        time.sleep(2)

        try:
            download_data_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Download data')]"))
            )
            download_data_button.click()
            print("✅ 'Download Data' button clicked.")
        except:
            print("❌ 'Download Data' button was not clicked.")

        time.sleep(3)

        try:
            format_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='formatOption']"))
            )
            time.sleep(2)
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

        download_path = f"C:\\Users\\User\\Downloads\\{looker_dashboard_name}.csv"
        timeout = 60
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                print("❌ Download failed: File not found.")
                driver.quit()
                exit()

        print("✔️✔️✔️✔️✔️✔️ Looker CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️")

        # Read CSV files with correct encoding and delimiter
        file_path = f"C:\\Users\\User\\Downloads\\{tableau_dashboard_name}.csv"
        file_path1 = f"C:\\Users\\User\\Downloads\\{looker_dashboard_name}.csv"

        # Try reading the Tableau CSV file
        try:
            if os.path.exists(file_path):
                df1 = pd.read_csv(file_path, encoding="utf-16", delimiter="\t")
                print("✅ Tableau CSV file read successfully!")
            else:
                print(f"❌ Error: The file '{file_path}' was not found.")
                df1 = None
        except Exception as e:
            print(f"❌ Error reading the Tableau file: {e}")
            df1 = None

        # Try reading the Looker CSV file
        try:
            if os.path.exists(file_path1):
                df2 = pd.read_csv(file_path1)  # Assuming it's a normal CSV
                print("✅ Looker CSV file read successfully!")
            else:
                print(f"❌ Error: The file '{file_path1}' was not found.")
                df2 = None
        except Exception as e:
            print(f"❌ Error reading the Looker file: {e}")
            df2 = None

        # Ensure both DataFrames are not None before proceeding
        if df1 is not None and df2 is not None:
            # Normalize column names: Remove extra spaces, lowercase all
            df1.columns = df1.columns.str.strip().str.lower()
            df2.columns = df2.columns.str.strip().str.lower()

            # Check for missing columns in df2
            missing_columns = [col for col in df1.columns if col not in df2.columns]

            if missing_columns:
                print(f"❌ Warning: The following columns are missing in Looker CSV: {', '.join(missing_columns)}")

                for col in missing_columns:
                    df2[col] = None  # Add missing columns with NaN values

            # Ensure columns are in the same order
            df2 = df2[df1.columns]

            # Get number of rows
            rows_original = len(df1)
            rows_changed = len(df2)

            # Find exact differences safely
            try:
                differences = df1.compare(df2)
            except ValueError as e:
                print(f"⚠️ Skipping comparison: {e}")
                differences = pd.DataFrame()

            # Find missing rows
            missing_rows = df1[~df1.isin(df2)].dropna(how="all")

            # Calculate accuracy percentage
            matching_rows = rows_original - len(differences)
            accuracy = (matching_rows / rows_original) * 100 if rows_original else 0

            # Print results
            print(f"🏆 Total Rows in Tableau File: {rows_original}")
            print(f"🏆 Total Rows in Looker File: {rows_changed}")
            print(f"🏆 Accuracy Percentage: {accuracy:.2f}%\n")

            if not differences.empty:
                print("🔹 Exact Differences Found:")
                print(differences)
            else:
                print("🏆 No differences found!")

            if not missing_rows.empty:
                print("\n🔸 Missing Rows in Changed CSV:")
                print(missing_rows)
            else:
                print("\n🏆 No missing rows found!")
        else:
            print("❌ Skipping comparison due to missing files.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    finally:
        sys.stdout = old_stdout  # Restore print output
        if 'driver' in locals():
            driver.quit()  # Ensure WebDriver quits

    return buffer.getvalue().split("\n")  # Return logs as list

@app.route('/run-selenium', methods=['POST'])
def run_selenium():
    data = request.json
    tableau_dashboard_name = data.get("tableau_dashboard_name")
    looker_dashboard_name = data.get("looker_dashboard_name")

    logs = run_selenium_test(tableau_dashboard_name, looker_dashboard_name)

    return jsonify({"status": "success", "logs": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Exposes API publicly
