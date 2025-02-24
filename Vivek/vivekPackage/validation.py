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
import google.cloud.logging
# Initialize the Cloud Logging client
client = google.cloud.logging.Client()

# Set up the logger
logger = client.logger("my-log")



app = Flask(__name__)
# Initialize Cloud Logging client
client = google.cloud.logging.Client()

logger = client.logger("my-log")



def run_selenium_test(tableau_dashboard_name, looker_dashboard_name, log_context):
    process_id = log_context.get("process_id", "N/A")  # Extract process_id or use a default

    # Capture logger.log_text() output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        logger.log_text(f"✅ Validating Tableau dashboard: {tableau_dashboard_name} | {process_id}")
        logger.log_text(f"✅ Validating Looker dashboard: {looker_dashboard_name} | {process_id}")
        logger.log_text(f"Starting Validation... | {process_id}")

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        #options.add_argument("--headless")
        options.add_experimental_option("detach", True)  # Keep browser open after execution

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)

        # Open the given URL
        logger.log_text(f"✅ NoW opening the Tableau Site to download the CSV file | {process_id}")

        url = "https://sso.online.tableau.com/public/login"
        driver.get(url)

        # **1️⃣ Enter Email**
        try:
            email_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='email']"))
            )
            email_element.send_keys("vishnuprakash@squareshift.co")
            logger.log_text(f"✅ Email entered successfully! | {process_id}")
        except:
            logger.log_text(f"❌ Email input element did not appear within the timeout. | {process_id}")

        # **2️⃣ Click the Sign In button**
        try:
            login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='login-submit']"))
            )
            login_button.click()
            logger.log_text(f"✅ Login button clicked! | {process_id}")
        except:
            logger.log_text(f"❌ Login button did not appear within the timeout. | {process_id}")

        # **3️⃣ Enter URI**
        try:
            uri_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='site-uri']"))
            )
            uri_element.send_keys("vishnuprakash-ce8986c494")
            logger.log_text(f"✅ URI entered successfully! | {process_id}")
        except:
            logger.log_text(f"❌ URI input element did not appear within the timeout. | {process_id}")

        # **4️⃣ Click the Continue button**
        try:
            verify_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='verify-button']"))
            )
            verify_button.click()
            logger.log_text(f"✅ Continue button clicked! | {process_id}")
        except:
            logger.log_text(f"❌ Continue button did not appear within the timeout. | {process_id}")

        # **5️⃣ Wait for the promo content**
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='login-promo__content']"))
            )
            logger.log_text(f"✅ Promo content is visible! | {process_id}")
        except:
            logger.log_text(f"❌ Promo content did not appear within the timeout. | {process_id}")

        # **6️⃣ Enter Password**
        try:
            password_field = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.send_keys("Vishnu@2001")
            logger.log_text(f"✅ Password entered successfully! | {process_id}")
        except:
            logger.log_text(f"❌ Password input element did not appear within the timeout. | {process_id}")

        # **7️⃣ Click the final Sign In button**
        try:
            final_login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            final_login_button.click()
            logger.log_text(f"✅ Signed in successfully! | {process_id}")
        except:
            logger.log_text(f"❌ Final login button did not appear within the timeout. | {process_id}")

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
        logger.log_text(f"✅ Switched to the detected iframe! | {process_id}")

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

                logger.log_text(f"✅ Download button clicked on attempt {attempt + 1} | {process_id}")
                break  # Exit loop on success

            except Exception as e:
                logger.log_text(f"⚠️ Attempt {attempt + 1} failed: {e} | {process_id}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        time.sleep(3)

        if attempt == max_attempts:
            logger.log_text(f"❌ Failed to click the download button after multiple attempts. | {process_id}")

        # **1️⃣1️⃣ Wait for Crosstab Option & Click**
        try:
            crosstab_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='frvoegc'][contains(.,'Crosstab')]"))
            )
            crosstab_option.click()
            logger.log_text(f"✅ Crosstab option clicked! | {process_id}")
        except:
            logger.log_text(f"❌ Crosstab option did not appear within the timeout. | {process_id}")

        # **1️⃣2️⃣ Wait for CSV Option & Click**
        try:
            csv_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='f1u2kjnq'][contains(.,'CSV')]"))
            )
            csv_option.click()
            logger.log_text(f"✅ CSV format selected! | {process_id}")
        except:
            logger.log_text(f"❌ CSV format option did not appear within the timeout. | {process_id}")

        # **1️⃣3️⃣ Wait for 1 second & Click the Final Download Button**
        time.sleep(1)
        try:
            final_download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-tb-test-id='export-crosstab-export-Button']"))
            )
            final_download_button.click()
            logger.log_text(f"✅ Download started! | {process_id}")
        except:
            logger.log_text(f"❌ Final download button did not appear within the timeout. | {process_id}")

        # **1️⃣4️⃣ Wait for the CSV File to Download**
        download_path = f"{tableau_dashboard_name}.csv"
        timeout = 60  # Wait up to 60 seconds for download
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                logger.log_text(f"❌ Download failed: File not found | {process_id}")
                driver.quit()
                exit()

        logger.log_text(f"✔️✔️✔️✔️✔️✔️ Tableau CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️ | {process_id}")

        logger.log_text(f"✅ NoW opening the Looker Site to download the CSV file | {process_id}")

        driver.get("https://squareshift.cloud.looker.com/login")

        try:
            email_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
            )
            email_element.send_keys("vivek@squareshift.co")
            logger.log_text(f"✅ Email was entered. | {process_id}")
        except:
            logger.log_text(f"❌ Email was not entered. | {process_id}")

        time.sleep(1)

        try:
            password_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            password_element.send_keys("Qwerty@12345")
            logger.log_text(f"✅ Password was entered. | {process_id}")
        except:
            logger.log_text(f"❌ Password was not entered. | {process_id}")

        time.sleep(1)

        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
            )
            login_button.click()
            logger.log_text(f"✅ Login button clicked. | {process_id}")
        except:
            logger.log_text(f"❌ Login button was not clicked. | {process_id}")

        time.sleep(2)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-pendo-id='ExplorePanel']"))
            )
            logger.log_text(f"✅ Home page loaded. | {process_id}")
        except:
            logger.log_text(f"❌ Home page did not load. | {process_id}")

        time.sleep(2)

        driver.get("https://squareshift.cloud.looker.com/dashboards/321")

        time.sleep(3)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"(//*[contains(text(),'{looker_dashboard_name}')])[2]"))
            )
            logger.log_text(f"✅ Dashboard loaded. | {process_id}")
        except:
            logger.log_text(f"❌ Dashboard did not load. | {process_id}")

        time.sleep(2)

        try:
            element_title = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h2[@data-testid='dashboard-tile-title']"))
            )
            element_title.click()
            logger.log_text(f"✅ Element title clicked. | {process_id}")
        except:
            logger.log_text(f"❌ Element title was not clicked. | {process_id}")

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

                logger.log_text(f"✅ Hovered and clicked three dots menu on attempt {attempt + 1} | {process_id}")
                break  # Exit loop on success

            except Exception as e:
                logger.log_text(f"⚠️ Attempt {attempt + 1} failed: {e} | {process_id}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        if attempt == max_attempts:
            logger.log_text(f"❌ Failed to click the three dots menu after multiple attempts. | {process_id}")

        time.sleep(2)

        try:
            download_data_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Download data')]"))
            )
            download_data_button.click()
            logger.log_text(f"✅ 'Download Data' button clicked. | {process_id}")
        except:
            logger.log_text(f"❌ 'Download Data' button was not clicked. | {process_id}")

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
            logger.log_text(f"✅ Format set to CSV. | {process_id}")
        except:
            logger.log_text(f"❌ Failed to set format to CSV. | {process_id}")

        time.sleep(1)

        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='qr-export-modal-download']"))
            )
            download_button.click()
            logger.log_text(f"✅ Download button clicked. | {process_id}")
        except:
            logger.log_text(f"❌ Download button was not clicked. | {process_id}")

        time.sleep(2)

        download_path = f"{looker_dashboard_name}.csv"
        timeout = 60
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                logger.log_text(f"❌ Download failed: File not found. | {process_id}")
                driver.quit()
                exit()

        logger.log_text(f"✔️✔️✔️✔️✔️✔️ Looker CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️ | {process_id}")

        # Read CSV files with correct encoding and delimiter
        file_path = f"{tableau_dashboard_name}.csv"
        file_path1 = f"{looker_dashboard_name}.csv"

        # Try reading the Tableau CSV file
        try:
            if os.path.exists(file_path):
                df1 = pd.read_csv(file_path, encoding="utf-16", delimiter="\t")
                logger.log_text(f"✅ Tableau CSV file read successfully! | {process_id}")
            else:
                logger.log_text(f"❌ Error: The file '{file_path}' was not found. | {process_id}")
                df1 = None
        except Exception as e:
            logger.log_text(f"❌ Error reading the Tableau file: {e} | {process_id}")
            df1 = None

        # Try reading the Looker CSV file
        try:
            if os.path.exists(file_path1):
                df2 = pd.read_csv(file_path1)  # Assuming it's a normal CSV
                logger.log_text(f"✅ Looker CSV file read successfully! | {process_id}")
            else:
                logger.log_text(f"❌ Error: The file '{file_path1}' was not found. | {process_id}")
                df2 = None
        except Exception as e:
            logger.log_text(f"❌ Error reading the Looker file: {e} | {process_id}")
            df2 = None

        # Ensure both DataFrames are not None before proceeding
        if df1 is not None and df2 is not None:
            # Normalize column names: Remove extra spaces, lowercase all
            df1.columns = df1.columns.str.strip().str.lower()
            df2.columns = df2.columns.str.strip().str.lower()

            # Check for missing columns in df2
            missing_columns = [col for col in df1.columns if col not in df2.columns]

            if missing_columns:
                logger.log_text(f"❌ Warning: The following columns are missing in Looker CSV: {', '.join(missing_columns)} | {process_id}")

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
                logger.log_text(f"⚠️ Skipping comparison: {e} | {process_id}")
                differences = pd.DataFrame()

            # Find missing rows
            missing_rows = df1[~df1.isin(df2)].dropna(how="all")

            # Calculate accuracy percentage
            matching_rows = rows_original - len(differences)
            accuracy = (matching_rows / rows_original) * 100 if rows_original else 0

            # Print results
            logger.log_text(f"🏆 Total Rows in Tableau File: {rows_original} | {process_id}")
            logger.log_text(f"🏆 Total Rows in Looker File: {rows_changed} | {process_id}")
            logger.log_text(f"🏆 Accuracy Percentage: {accuracy:.2f}% | {process_id}\n")

            if not differences.empty:
                logger.log_text(f"🔹 Exact Differences Found: | {process_id}")
                logger.log_text(str(differences) + f" | {process_id}") # Convert to string to be safely logged
            else:
                logger.log_text(f"🏆 No differences found! | {process_id}")

            if not missing_rows.empty:
                logger.log_text(f"\n🔸 Missing Rows in Changed CSV: | {process_id}")
                logger.log_text(str(missing_rows) + f" | {process_id}")# Convert to string to be safely logged
            else:
                logger.log_text(f"\n🏆 No missing rows found! | {process_id}")
        else:
            logger.log_text(f"❌ Skipping comparison due to missing files. | {process_id}")

    except Exception as e:
        logger.log_text(f"❌ Error: {str(e)} | {process_id}")

    finally:
        sys.stdout = old_stdout  # Restore print output
        if 'driver' in locals():
            driver.quit()  # Ensure WebDriver quits

    return buffer.getvalue().split("\n")  # Return logs as list

@app.route('/run-selenium', methods=['POST'])
def run_selenium():
    try:
        data = request.json
        tableau_dashboard_name = data.get("tableau_dashboard_name")
        looker_dashboard_name = data.get("looker_dashboard_name")
        process_id = data.get("process_id")

        if not all([tableau_dashboard_name, looker_dashboard_name, process_id]):
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400

        log_context = {"process_id": process_id}  # Create log context

        logs = run_selenium_test(tableau_dashboard_name, looker_dashboard_name, log_context)

        return jsonify({"status": "success", "logs": logs})  # Return logs in the response

    except Exception as e:
        logger.log_text(f"Error in run_selenium: {e}") # Include context here too
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Exposes API publicly