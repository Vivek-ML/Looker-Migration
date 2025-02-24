from flask import Flask, request, jsonify
import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from flask import Flask, request, jsonify, send_from_directory
import os

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

# LOG_FILE = os.path.join(os.getenv("TEMP"), "demo.log")
LOG_FILE = "demo.log"

os.environ["DISPLAY"] = ":0"
os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"


def log_message(message, level="INFO"):
    """Append logs to demo.log with UTF-8 encoding in structured format."""
    log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {level} | {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")
    print(log_entry)


def run_selenium_test(tableau_dashboard_name, looker_dashboard_name):
    open(LOG_FILE, "w").close()

    try:
        log_message(f"✅ Validating Tableau dashboard: {tableau_dashboard_name}", "INFO")
        log_message(f"✅ Validating Looker dashboard: {looker_dashboard_name}", "INFO")
        log_message(" Starting Validation...", "INFO")

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        options.add_experimental_option("detach", True)  # Keep browser open after execution

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)

        # Open the given URL
        log_message("✅ NoW opening the Tableau Site to download the CSV file", "INFO")

        url = "https://sso.online.tableau.com/public/login"
        driver.get(url)

        # **1️⃣ Enter Email**
        try:
            email_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='email']"))
            )
            email_element.send_keys("vishnuprakash@squareshift.co")
            log_message("✅ Email entered successfully!", "INFO")
        except:
            log_message("❌ Email input element did not appear within the timeout.", "ERROR")

        # **2️⃣ Click the Sign In button**
        try:
            login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='login-submit']"))
            )
            login_button.click()
            log_message("✅ Login button clicked!", "INFO")
        except:
            log_message("❌ Login button did not appear within the timeout.", "ERROR")

        # **3️⃣ Enter URI**
        try:
            uri_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='site-uri']"))
            )
            uri_element.send_keys("vishnuprakash-ce8986c494")
            log_message("✅ URI entered successfully!", "INFO")
        except:
            log_message("❌ URI input element did not appear within the timeout.", "ERROR")

        # **4️⃣ Click the Continue button**
        try:
            verify_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='verify-button']"))
            )
            verify_button.click()
            log_message("✅ Continue button clicked!", "INFO")
        except:
            log_message("❌ Continue button did not appear within the timeout.", "ERROR")

        # **5️⃣ Wait for the promo content**
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='login-promo__content']"))
            )
            log_message("✅ Promo content is visible!", "INFO")
        except:
            log_message("❌ Promo content did not appear within the timeout.", "INFO")

        # **6️⃣ Enter Password**
        try:
            password_field = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.send_keys("Vishnu@2001")
            log_message("✅ Password entered successfully!", "INFO")
        except:
            log_message("❌ Password input element did not appear within the timeout.", "ERROR")

        # **7️⃣ Click the final Sign In button**
        try:
            final_login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            final_login_button.click()
            log_message("✅ Signed in successfully!", "INFO")
        except:
            log_message("❌ Final login button did not appear within the timeout.", "ERROR")

        # **8️⃣ Wait & Navigate to the Tableau Dashboard**
        time.sleep(7)
        dashboard_url = f"https://prod-apnortheast-a.online.tableau.com/#/site/vishnuprakash-ce8986c494/views/Tableau_Dashboard1/Tableau_Dashboard?:iid=1"
        driver.get(dashboard_url)
        time.sleep(2)

        driver.refresh()

        time.sleep(12)

        # # **9️⃣ Wait for the iframe & Switch to it**

        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))  # Check if any iframe is present
        )
        driver.switch_to.frame(iframe)
        log_message("✅ Switched to the detected iframe!", "INFO")

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

                log_message(f"✅ Download button clicked on attempt {attempt + 1}", "INFO")
                break  # Exit loop on success

            except Exception as e:
                log_message(f"⚠️ Attempt {attempt + 1} failed: {e}", "ERROR")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        time.sleep(3)

        if attempt == max_attempts:
            log_message("❌ Failed to click the download button after multiple attempts.", "ERROR")

        # **1️⃣1️⃣ Wait for Crosstab Option & Click**
        try:
            crosstab_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='frvoegc'][contains(.,'Crosstab')]"))
            )
            crosstab_option.click()
            log_message("✅ Crosstab option clicked!", "INFO")
        except:
            log_message("❌ Crosstab option did not appear within the timeout.", "ERROR")

        # **1️⃣2️⃣ Wait for CSV Option & Click**
        try:
            csv_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='f1u2kjnq'][contains(.,'CSV')]"))
            )
            csv_option.click()
            log_message("✅ CSV format selected!", "INFO")
        except:
            log_message("❌ CSV format option did not appear within the timeout.", "ERROR")

        # **1️⃣3️⃣ Wait for 1 second & Click the Final Download Button**
        time.sleep(1)
        try:
            final_download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-tb-test-id='export-crosstab-export-Button']"))
            )
            final_download_button.click()
            log_message("✅ Download started!", "INFO")
        except:
            log_message("❌ Final download button did not appear within the timeout.", "ERROR")

        # **1️⃣4️⃣ Wait for the CSV File to Download**
        download_path = f"C:\\Users\\vivek\\Downloads\\{tableau_dashboard_name}.csv"
        timeout = 60  # Wait up to 60 seconds for download
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                log_message("❌ Download failed: File not found", "ERROR")
                driver.quit()
                exit()

        log_message("✔️✔️✔️✔️✔️✔️ Tableau CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️", "INFO")

        log_message("✅ NoW opening the Looker Site to download the CSV file", "INFO")

        driver.get("https://squareshift.cloud.looker.com/login")

        try:
            email_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
            )
            email_element.send_keys("vivek@squareshift.co")
            log_message("✅ Email was entered.", "INFO")
        except:
            log_message("❌ Email was not entered.", "ERROR")

        time.sleep(1)

        try:
            password_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            password_element.send_keys("Qwerty@12345")
            log_message("✅ Password was entered.", "INFO")
        except:
            log_message("❌ Password was not entered.", "ERROR")

        time.sleep(1)

        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
            )
            login_button.click()
            log_message("✅ Login button clicked.", "INFO")
        except:
            log_message("❌ Login button was not clicked.", "ERROR")

        time.sleep(2)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-pendo-id='ExplorePanel']"))
            )
            log_message("✅ Home page loaded.", "INFO")
        except:
            log_message("❌ Home page did not load.", "ERROR")

        time.sleep(2)

        driver.get("https://squareshift.cloud.looker.com/dashboards/323")

        time.sleep(3)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"(//div[contains(@class, 'ElementTitle__EllipsisDiv-sc-cy6gpn-2')]"))
            )
            log_message("✅ Dashboard loaded.", "INFO")
        except:
            log_message("❌ Dashboard did not load.", "ERROR")

        time.sleep(2)

        try:
            element_title = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h2[@data-testid='dashboard-tile-title']"))
            )
            element_title.click()
            log_message("✅ Element title clicked.", "INFO")
        except:
            log_message("❌ Element title was not clicked.", "ERROR")

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

                log_message(f"✅ Hovered and clicked three dots menu on attempt {attempt + 1}", "INFO")
                break  # Exit loop on success

            except Exception as e:
                log_message(f"⚠️ Attempt {attempt + 1} failed: {e}", "ERROR")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        if attempt == max_attempts:
            log_message("❌ Failed to click the three dots menu after multiple attempts.", "ERROR")

        time.sleep(2)

        try:
            download_data_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Download data')]"))
            )
            download_data_button.click()
            log_message("✅ 'Download Data' button clicked.", "INFO")
        except:
            log_message("❌ 'Download Data' button was not clicked.", "ERROR")

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
            log_message("✅ Format set to CSV.", "INFO")
        except:
            log_message("❌ Failed to set format to CSV.", "ERROR")

        time.sleep(1)

        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='qr-export-modal-download']"))
            )
            download_button.click()
            log_message("✅ Download button clicked.", "INFO")
        except:
            log_message("❌ Download button was not clicked.", "ERROR")

        time.sleep(2)

        download_path = f"C:\\Users\\vivek\\Downloads\\{looker_dashboard_name}.csv"
        timeout = 60
        start_time = time.time()

        while not os.path.exists(download_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                log_message("❌ Download failed: File not found.", "ERROR")
                driver.quit()
                exit()

        log_message("✔️✔️✔️✔️✔️✔️ Looker CSV file is successfully downloaded!✔️✔️✔️✔️✔️✔️", "INFO")

        # Read CSV files with correct encoding and delimiter
        file_path = f"C:\\Users\\vivek\\Downloads\\{tableau_dashboard_name}.csv"
        file_path1 = f"C:\\Users\\vivek\\Downloads\\{looker_dashboard_name}.csv"

        # Try reading the Tableau CSV file
        try:
            if os.path.exists(file_path):
                df1 = pd.read_csv(file_path, encoding="utf-16", delimiter="\t")
                log_message("✅ Tableau CSV file read successfully!", "INFO")
            else:
                log_message(f"❌ Error: The file '{file_path}' was not found.", "ERROR")
                df1 = None
        except Exception as e:
            log_message(f"❌ Error reading the Tableau file: {e}", "ERROR")
            df1 = None

        # Try reading the Looker CSV file
        try:
            if os.path.exists(file_path1):
                df2 = pd.read_csv(file_path1)  # Assuming it's a normal CSV
                log_message("✅ Looker CSV file read successfully!", "INFO")
            else:
                log_message(f"❌ Error: The file '{file_path1}' was not found.", "ERROR")
                df2 = None
        except Exception as e:
            log_message(f"❌ Error reading the Looker file: {e}", "ERROR")
            df2 = None

        # Ensure both DataFrames are not None before proceeding
        if df1 is not None and df2 is not None:
            # Normalize column names: Remove extra spaces, lowercase all
            df1.columns = df1.columns.str.strip().str.lower()
            df2.columns = df2.columns.str.strip().str.lower()

            # Check for missing columns in df2
            missing_columns = [col for col in df1.columns if col not in df2.columns]

            if missing_columns:
                log_message(f"❌ Warning: The following columns are missing in Looker CSV: {', '.join(missing_columns)}",
                            "ERROR")

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
                log_message(f"⚠️ Skipping comparison: {e}", "INFO")
                differences = pd.DataFrame()

            # Find missing rows
            missing_rows = df1[~df1.isin(df2)].dropna(how="all")

            # Calculate accuracy percentage
            matching_rows = rows_original - len(differences)
            accuracy = (matching_rows / rows_original) * 100 if rows_original else 0

            # Print results
            log_message(f"🏆 Total Rows in Tableau File: {rows_original}", "INFO")
            log_message(f"🏆 Total Rows in Looker File: {rows_changed}", "INFO")
            log_message(f"🏆 Accuracy Percentage: {accuracy:.2f}%\n", "INFO")

            if not differences.empty:
                log_message("🔹 Exact Differences Found:")

                # Correct indentation here

            try:
                # Convert DataFrame to string before logging to avoid type errors
                log_message(differences.to_string(), "INFO")
            except Exception as log_error:
                log_message(f"❌ Error while logging differences: {str(log_error)}", "ERROR")
        else:
            log_message("🏆 No differences found!", "INFO")

        if not missing_rows.empty:
            log_message("\n🔸 Missing Rows in Changed CSV:", "ERROR")
            try:
                # Convert missing_rows DataFrame to string for logging
                log_message(missing_rows.to_string(), "ERROR")
            except Exception as log_error:
                log_message(f"❌ Error while logging missing rows: {str(log_error)}", "ERROR")
        else:
            log_message("\n🏆 No missing rows found!", "INFO")

    except Exception as e:
        log_message(f"❌ Error: {str(e)}", "ERROR")

    return log_message

    # Return logs as list (Optional)
    return buffer.getvalue().split("\n")

    # Return logs as list (Optional)
    return buffer.getvalue().split("\n")


@app.route('/run-selenium', methods=['POST'])
def run_selenium():
    data = request.json
    tableau_dashboard_name = data.get("tableau_dashboard_name")
    looker_dashboard_name = data.get("looker_dashboard_name")

    run_selenium_test(tableau_dashboard_name, looker_dashboard_name)

    return jsonify({"status": "success", "message": "Logs written to demo.log"}), 200


@app.route('/get-logs', methods=['GET'])
def get_logs():
    try:
        # Securely serve the log file
        return send_from_directory(os.path.dirname(LOG_FILE), os.path.basename(LOG_FILE), mimetype='text/plain')
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Log file not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
