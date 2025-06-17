from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sites  # Your separate module with site info

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def run_faucet(site_name, site_info):
    log(f"Connecting to {site_name}: {site_info['url']}")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(site_info['url'])
        wait = WebDriverWait(driver, 10)

        # Step 1: Click "NO THANKS"
        try:
            no_thanks_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='pushpad_deny_button' and normalize-space(text())='NO THANKS']"))
            )
            no_thanks_button.click()
            log(f"✅ {site_name}: 'NO THANKS' clicked")
        except Exception:
            log(f"ℹ️ {site_name}: 'NO THANKS' not found or already dismissed")

        # Step 2: Click any version of "LOGIN"
        login_clicked = False
        try:
            login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'login_menu_button') and contains(text(), 'LOGIN')]")
            login_button.click()
            login_clicked = True
        except:
            try:
                login_link = driver.find_element(By.XPATH, "//a[normalize-space(text())='LOGIN']")
                login_link.click()
                login_clicked = True
            except:
                try:
                    li_login = driver.find_element(By.XPATH, "//li[contains(@class,'login_menu_button')]//a[normalize-space(text())='LOGIN']")
                    li_login.click()
                    login_clicked = True
                except:
                    pass

        if login_clicked:
            log(f"✅ {site_name}: 'LOGIN' clicked")
        else:
            log(f"⚠️ {site_name}: Could not click any 'LOGIN' element")

        time.sleep(1)  # Allow login modal/form to load

        # Step 3: Fill credentials
        try:
            driver.find_element(By.ID, "login_form_btc_address").send_keys(site_info["email"])
            driver.find_element(By.ID, "login_form_password").send_keys(site_info["password"])
            log(f"✅ {site_name}: Credentials filled")
        except Exception as e:
            log(f"❌ {site_name}: Failed to fill login form — {e}")
            driver.quit()
            return

        # Step 4: Submit login
        try:
            driver.find_element(By.ID, "login_button").click()
            log(f"✅ {site_name}: Final 'LOGIN!' clicked")
            time.sleep(10)
        except Exception as e:
            log(f"❌ {site_name}: Failed to click final login — {e}")
            driver.quit()
            return
        

        # Step 5: Wait and press "ROLL!" button
        try:
            roll_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "free_play_form_button"))
            )
            log(f"🎲 {site_name}: ready to 'ROLL!'")
            #roll_button.click()
            #log(f"🎲 {site_name}: 'ROLL!' button clicked")
        except Exception as e:
            log(f"⚠️ {site_name}: Could not find or click 'ROLL!' — {e}")

        # Step 6: Wait before closing
        time.sleep(120)
        driver.quit()
        log(f"✅ {site_name}: Process finished and browser closed")

    except Exception as e:
        log(f"❌ {site_name}: Failed — {e}")



if __name__ == "__main__":
    while True:
        for site_name, site_info in sites.site_list.items():
            run_faucet(site_name, site_info)
        log("⏱ Sleeping for 60 minutes...\n")
        time.sleep(60 * 60)
