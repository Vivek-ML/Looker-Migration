import difflib
import time
import os
import pandas as pd
import self
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from src.config_reader import ConfigReader
from src.logger import log_message



class SeleniumRunner:

    def __init__(self):
        self.config = ConfigReader()
        self.driver = None
        self.looker_dashboard_names = []
        self.dashboard_names = []


    def setup_driver(self):
        """Initialize WebDriver with options."""
        browser = self.config.get("SELENIUM", "browser")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(int(self.config.get("SELENIUM", "implicit_wait")))

    def login_tableau(self):
        """Automates login to Tableau."""
        self.driver.get(self.config.get("SELENIUM", "tableau_login_url"))
        log_message("<SPEED_METER> Opening Tableau login page...", "INFO")

        try:
            email_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "email"))
            )
            email_element.send_keys(self.config.get("CREDENTIALS", "tableau_email"))
            log_message("<SPEED_METER>Email entered successfully.", "INFO")

            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "login-submit"))
            )
            login_button.click()
            log_message("<SPEED_METER>Login button clicked.", "INFO")

        except Exception as e:
            log_message(f"Error in login step: {e}", "ERROR")

    def download_csv_from_tableau(self):
        # **3️⃣ Enter URI**
        try:
            uri_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='site-uri']"))
            )
            uri_element.send_keys("vishnuprakash-ce8986c494")
            log_message("<SPEED_METER> URI entered successfully", "INFO")
        except:
            log_message("<SPEED_METER> URI input element did not appear within the timeout.", "ERROR")

        # **4️⃣ Click the Continue button**
        try:
            verify_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='verify-button']"))
            )
            verify_button.click()
            log_message("<SPEED_METER> Continue button clicked", "INFO")
        except:
            log_message("<SPEED_METER> Continue button did not appear within the timeout.", "ERROR")

        # **5️⃣ Wait for the promo content**
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='login-promo__content']"))
            )
            log_message("<SPEED_METER> Promo content is visible", "INFO")
        except:
            log_message("<SPEED_METER> Promo content did not appear within the timeout.", "INFO")

        # **6️⃣ Enter Password**
        try:
            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.send_keys("Vishnu@2001")
            log_message("<SPEED_METER> Password entered successfully", "INFO")
        except:
            log_message("<RIGHT_ARROW> Password input element did not appear within the timeout.", "ERROR")

        # **7️⃣ Click the final Sign In button**
        try:
            final_login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            final_login_button.click()
            log_message("<SPEED_METER> Signed in successfully", "INFO")
        except:
            log_message("<RIGHT_ARROW> Final login button did not appear within the timeout.", "ERROR")
        """Navigates to Tableau dashboard and downloads CSV."""
        time.sleep(7)
        try:
            dashboard_url = self.config.get("SELENIUM", "tableau_dashboard_url")
            self.driver.get(dashboard_url)
            log_message(f"<SPEED_METER>Navigating to Tableau dashboard", "INFO")
            time.sleep(2)
            self.driver.refresh()
            time.sleep(12)

            # Switch to iframe
            iframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self.driver.switch_to.frame(iframe)

            time.sleep(6)

            max_attempts = 3  # Number of retry attempts
            attempt = 0  # Initialize attempt counter

            while attempt < max_attempts:
                try:
                    # Wait for the button to be present in the DOM
                    download_button = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@id='download']"))
                    )

                    # Scroll the button into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                    time.sleep(2)  # Allow time for any animations

                    # Ensure the button is clickable
                    download_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@id='download']"))
                    )

                    # Remove any overlay issues
                    self.driver.execute_script("arguments[0].style.pointerEvents = 'auto';", download_button)

                    # Try clicking the button normally
                    try:
                        download_button.click()
                    except:
                        # Use JavaScript click if normal click fails
                        self.driver.execute_script("arguments[0].click();", download_button)

                    log_message(f"<SPEED_METER> Download button clicked on attempt {attempt + 1}", "INFO")
                    break  # Exit loop on success

                except Exception as e:
                    log_message(f"⚠️ Attempt {attempt + 1} failed: {e}", "ERROR")
                    attempt += 1
                    time.sleep(2)  # Wait before retrying

            time.sleep(3)

            if attempt == max_attempts:
                log_message("<RIGHT_ARROW> Failed to click the download button after multiple attempts.", "ERROR")

            # **1️⃣1️⃣ Wait for Crosstab Option & Click**
            try:
                crosstab_option = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='frvoegc'][contains(.,'Crosstab')]"))
                )
                crosstab_option.click()
                log_message("<SPEED_METER> Crosstab option clicked", "INFO")
                time.sleep(2)
            except:
                log_message("<RIGHT_ARROW> Crosstab option did not appear within the timeout.", "ERROR")


            # Extract dashboard names dynamically
            dashboard_elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[@class='thumbnail-title_f178rywr']"))
            )
            self.dashboard_names = [dashboard.text for dashboard in dashboard_elements]

            self.looker_dashboard_names = [dashboard.text for dashboard in dashboard_elements]

            # Log the extracted dashboard names
            for i, name in enumerate(self.dashboard_names, 1):
                log_message(f"Dashboard {i}: {name}")

            time.sleep(2)

            try:
                Close_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-tb-test-id='export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-CloseButton']"))
                )
                Close_button.click()
                time.sleep(2)
            except:
                log_message("<RIGHT_ARROW> Close button did not appear within the timeout.", "ERROR")
            time.sleep(2)
            #Iterate through each dashboard and download CSV

            # for index, dashboard_name in enumerate(reversed(self.dashboard_names)):
            #     try:
            #         max_attempts = 3  # Number of retry attempts
            #         attempt = 0  # Initialize attempt counter
            #
            #         while attempt < max_attempts:
            #             try:
            #                 # Wait for the button to be present in the DOM
            #                 download_button = WebDriverWait(self.driver, 20).until(
            #                     EC.presence_of_element_located((By.XPATH, "//button[@id='download']"))
            #                 )
            #
            #                 # Scroll the button into view
            #                 self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",
            #                                            download_button)
            #                 time.sleep(2)  # Allow time for any animations
            #
            #                 # Ensure the button is clickable
            #                 download_button = WebDriverWait(self.driver, 10).until(
            #                     EC.element_to_be_clickable((By.XPATH, "//button[@id='download']"))
            #                 )
            #
            #                 # Remove any overlay issues
            #                 self.driver.execute_script("arguments[0].style.pointerEvents = 'auto';", download_button)
            #
            #                 # Try clicking the button normally
            #                 try:
            #                     download_button.click()
            #                 except:
            #                     # Use JavaScript click if normal click fails
            #                     self.driver.execute_script("arguments[0].click();", download_button)
            #
            #                 break  # Exit loop on success
            #
            #             except Exception as e:
            #                 attempt += 1
            #                 time.sleep(2)  # Wait before retrying
            #
            #         time.sleep(3)
            #
            #         if attempt == max_attempts:
            #             log_message("<RIGHT_ARROW> Failed to click the download button after multiple attempts.",
            #                         "ERROR")
            #
            #         # **1️⃣1️⃣ Wait for Crosstab Option & Click**
            #         try:
            #             crosstab_option = WebDriverWait(self.driver, 20).until(
            #                 EC.element_to_be_clickable((By.XPATH, "//span[@class='frvoegc'][contains(.,'Crosstab')]"))
            #             )
            #             crosstab_option.click()
            #             time.sleep(5)
            #         except:
            #             log_message("<RIGHT_ARROW> Crosstab option did not appear within the timeout.", "ERROR")
            #
            #         # **Check if it's NOT the last iteration**
            #         if index < len(self.dashboard_names) - 1:
            #             # Select Dashboard in Dialog
            #             dashboard_option = WebDriverWait(self.driver, 20).until(
            #                 EC.element_to_be_clickable((By.XPATH,
            #                                             f"//span[@class ='thumbnail-title_f178rywr'][contains(.,'{dashboard_name}')]"))
            #             )
            #
            #             self.driver.execute_script("arguments[0].scrollIntoView();", dashboard_option)
            #             time.sleep(1)
            #             dashboard_option.click()
            #             log_message(f"Selected dashboard: {dashboard_name}")
            #             time.sleep(2)
            #
            #         # Click CSV Option
            #         csv_option = WebDriverWait(self.driver, 20).until(
            #             EC.element_to_be_clickable((By.XPATH, "//div[@class='f1u2kjnq'][contains(.,'CSV')]"))
            #         )
            #         csv_option.click()
            #         log_message("<RIGHT_ARROW>CSV format selected", "ERROR")
            #         time.sleep(1)
            #
            #         # Click Final Download Button
            #         final_download_button = WebDriverWait(self.driver, 20).until(
            #             EC.element_to_be_clickable(
            #                 (By.XPATH, "//button[@data-tb-test-id='export-crosstab-export-Button']"))
            #         )
            #         final_download_button.click()
            #         log_message("Download started")
            #         # Wait for Download Completion
            #         download_path = "C:\\Users\\User\\Downloads"  # Double backslashes
            #
            #         file_path = f"{download_path}\\{dashboard_name}.csv"
            #         timeout = 60
            #         start_time = time.time()
            #
            #         while not os.path.exists(file_path):
            #             time.sleep(1)
            #             if time.time() - start_time > timeout:
            #                 log_message(f"Download failed for {dashboard_name}", "ERROR")
            #                 break
            #         else:
            #             log_message(f"Downloaded successfully: {dashboard_name}.csv", "INFO")
            #
            #     except Exception as e:
            #         log_message(f"Error processing {dashboard_name}: {e}", "ERROR")

        except Exception as e:
            log_message(f"<RIGHT_ARROW> Error: {str(e)}", "ERROR")


    def login_looker(self):
        log_message("<RIGHT_ARROW> NoW opening the Looker Site to download the CSV file", "INFO")
        self.driver.get(self.config.get("SELENIUM", "looker_login_url"))


        try:
            email_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
            )
            email_element.send_keys(self.config.get("CREDENTIALS", "looker_email"))
            log_message("<RIGHT_ARROW> Email was entered.", "INFO")
        except:
            log_message("<RIGHT_ARROW> Email was not entered.", "ERROR")

        time.sleep(1)

        try:
            password_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            password_element.send_keys(self.config.get("CREDENTIALS", "looker_password"))
            log_message("<RIGHT_ARROW> Password was entered.", "INFO")
        except:
            log_message("<RIGHT_ARROW> Password was not entered.", "ERROR")

        time.sleep(1)

        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
            )
            login_button.click()
            log_message("<RIGHT_ARROW> Login button clicked.", "INFO")
        except:
            log_message("<RIGHT_ARROW> Login button was not clicked.", "ERROR")

        time.sleep(2)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-pendo-id='ExplorePanel']"))
            )
            log_message("<RIGHT_ARROW> Home page loaded.", "INFO")
        except:
            log_message("<RIGHT_ARROW> Home page did not load.", "ERROR")

        time.sleep(2)

    def download_csv_from_looker(self):


        # dashboard_url = "https://squareshift.cloud.looker.com/dashboards/sales_data::pie_line_bar_scatter_dashboard_9876"
        # self.driver.get(dashboard_url)
        #
        # time.sleep(5)

        # for index, title in enumerate(self.looker_dashboard_names, start=1):
        #     try:
        #         # Click chart title
        #         element_title = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH, f"//h2[@data-testid='dashboard-tile-title'][contains(.,'{title}')]"))
        #         )
        #         element_title.click()
        #         time.sleep(3)
        #
        #         # Click the corresponding three-dot menu
        #         time.sleep(3)
        #
        #         max_attempts = 3  # Number of retry attempts
        #         attempt = 0  # Initialize attempt counter
        #
        #         while attempt < max_attempts:
        #             try:
        #                 # Wait for the three dots menu to be present in the DOM
        #                 three_dots_menu = WebDriverWait(self.driver, 10).until(
        #                     EC.presence_of_element_located(
        #                         (By.XPATH,
        #                          f"(//button[contains(@class, 'ElementOverlay__VerticalIconContainer-sc')])[{index}]"))
        #                 )
        #
        #                 # Scroll into view
        #                 self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", three_dots_menu)
        #                 time.sleep(1)  # Give time for UI to settle
        #
        #                 # Hover over the menu
        #                 actions = ActionChains(self.driver)
        #                 actions.move_to_element(three_dots_menu).perform()
        #                 time.sleep(1)  # Allow time for hover effects
        #
        #                 # Ensure the button is clickable
        #                 three_dots_menu = WebDriverWait(self.driver, 10).until(
        #                     EC.element_to_be_clickable(
        #                         (By.XPATH,
        #                          f"(//button[contains(@class, 'ElementOverlay__VerticalIconContainer-sc')])[{index}]"))
        #                 )
        #
        #                 # Remove any overlay issues
        #                 self.driver.execute_script("arguments[0].style.pointerEvents = 'auto';", three_dots_menu)
        #
        #                 # Click the menu
        #                 try:
        #                     three_dots_menu.click()
        #                 except:
        #                     # Use JavaScript click if normal click fails
        #                     self.driver.execute_script("arguments[0].click();", three_dots_menu)
        #
        #                 log_message(f"<RIGHT_ARROW> Hovered and clicked three dots menu on attempt {attempt + 1}",
        #                             "INFO")
        #                 break  # Exit loop on success
        #
        #             except Exception as e:
        #                 log_message(f"⚠️ Attempt {attempt + 1} failed: {e}", "ERROR")
        #                 attempt += 1
        #                 time.sleep(2)  # Wait before retrying
        #
        #         if attempt == max_attempts:
        #             log_message("<RIGHT_ARROW> Failed to click the three dots menu after multiple attempts.", "ERROR")
        #
        #         time.sleep(2)
        #
        #         # Click 'Download data'
        #         download_data_button = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Download data')]"))
        #         )
        #         download_data_button.click()
        #         time.sleep(3)
        #
        #         # Select CSV format
        #         format_dropdown = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//input[@name='formatOption']"))
        #         )
        #         format_dropdown.click()
        #         time.sleep(1)
        #         format_dropdown.send_keys(Keys.ARROW_DOWN)
        #         time.sleep(1)
        #         format_dropdown.send_keys(Keys.ARROW_DOWN)
        #         time.sleep(1)
        #         format_dropdown.send_keys(Keys.ENTER)
        #         time.sleep(1)
        #
        #         # Click download button
        #         download_button = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//button[@id='qr-export-modal-download']"))
        #         )
        #         try:
        #             download_button = WebDriverWait(self.driver, 10).until(
        #                 EC.element_to_be_clickable((By.XPATH, "//button[@id='qr-export-modal-download']"))
        #             )
        #             download_button.click()
        #             log_message("<DOWNLOAD> Download button clicked.", "INFO")
        #         except:
        #             log_message("<DOWNLOAD> Download button was not clicked.", "ERROR")
        #
        #         time.sleep(2)
        #
        #     except Exception as e:
        #         print(f"Error processing {title}: {e}")

        for index, title in enumerate(self.looker_dashboard_names, start=1):
            download_path = f"C:\\Users\\User\\Downloads\\{title} (1).csv"
            log_message(f"Download_path {download_path}")
            timeout = 60
            start_time = time.time()

            while not os.path.exists(download_path):
                time.sleep(1)
                if time.time() - start_time > timeout:
                    log_message("<RIGHT_ARROW> Download failed: File not found.", "ERROR")
                    self.driver.quit()
                    exit()

            log_message(f" <DOWNLOAD> {title} Looker CSV file is successfully downloaded!",
                        "INFO")  # Allow time for download to complete

        log_message("<DOWNLOAD> All Looker CSV files downloaded.")

    def compare_tableau_and_looker_files(self):
        try:
            for tableau_dashboard_name in self.dashboard_names:
                looker_dashboard_name = f"{tableau_dashboard_name} (1)"
                tableau_file_path = f"C:\\Users\\User\\Downloads\\{tableau_dashboard_name}.csv"
                looker_file_path = f"C:\\Users\\User\\Downloads\\{looker_dashboard_name}.csv"

                # Check if both files exist
                if not os.path.exists(tableau_file_path) or not os.path.exists(looker_file_path):
                    log_message(f"Error: One or both files for '{tableau_dashboard_name}' are missing.", "ERROR")
                    continue

                # Read CSV files dynamically
                try:
                    df_tableau = pd.read_csv(tableau_file_path, encoding="utf-16", delimiter="\t")
                    df_looker = pd.read_csv(looker_file_path)
                except Exception as e:
                    log_message(f"Error reading files '{tableau_dashboard_name}': {e}", "ERROR")
                    continue

                # Normalize column names
                df_tableau.columns = df_tableau.columns.str.strip().str.lower()
                df_looker.columns = df_looker.columns.str.strip().str.lower()
                df_looker.columns = [col.replace("orders ", "") for col in df_looker.columns]

                # Find missing and extra columns dynamically
                missing_in_looker = set(df_tableau.columns) - set(df_looker.columns)
                extra_in_looker = set(df_looker.columns) - set(df_tableau.columns)

                if missing_in_looker:
                    log_message(f"Missing columns in Looker '{looker_dashboard_name}': {', '.join(missing_in_looker)}",
                                "ERROR")
                    for col in missing_in_looker:
                        df_looker[col] = None

                if extra_in_looker:
                    log_message(f"Extra columns in Looker '{looker_dashboard_name}': {', '.join(extra_in_looker)}",
                                "WARNING")
                    df_looker = df_looker.drop(columns=extra_in_looker)

                # Ensure column order matches
                df_looker = df_looker[df_tableau.columns]

                # Compare row counts
                rows_tableau, rows_looker = len(df_tableau), len(df_looker)
                if rows_tableau != rows_looker:
                    log_message(
                        f"Row count mismatch in '{tableau_dashboard_name}': Tableau ({rows_tableau}) vs Looker ({rows_looker})",
                        "WARNING")

                # Compare values dynamically
                try:
                    differences = df_tableau.compare(df_looker, keep_shape=True, keep_equal=False)
                    if not differences.empty:
                        log_message(f"Differences found in '{tableau_dashboard_name}':", "ERROR")
                        for index, row in differences.iterrows():
                            diff_details = ", ".join(
                                [f"{col}: Tableau='{row[0]}', Looker='{row[1]}'" for col in differences.columns]
                            )
                            log_message(f"Row {index}: {diff_details}", "ERROR")
                    else:
                        log_message(f"No differences in values for '{tableau_dashboard_name}'.", "INFO")

                except ValueError as e:
                    log_message(f"Skipping comparison for '{tableau_dashboard_name}' due to error: {e}", "WARNING")

        except Exception as e:
            log_message(f"Error: {str(e)}", "ERROR")



    def run(self):
        """Executes the Selenium automation."""
        try:
            self.setup_driver()
            self.login_tableau()
            self.download_csv_from_tableau()
            #self.login_looker()
            self.download_csv_from_looker()
            self.compare_tableau_and_looker_files()
        finally:
            self.driver.quit()
            log_message("Selenium session closed.", "INFO")


# Run the script
if __name__ == "__main__":
    bot = SeleniumRunner()
    bot.run()

