import undetected_chromedriver as uc
import pyautogui
import time
from datetime import datetime
import sites  # your sites.py

# Time-stamped logger
def log(message):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}")

# Helper: Click on screen coords
def click(x, y, delay=0.5):
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()
    time.sleep(delay)

# Helper: Type text
def type_text(text, delay=0.5):
    pyautogui.write(text, interval=0.05)
    time.sleep(delay)

# Main automation flow
def run_faucet(site_name, site_info):
    log(f"🌐 Connecting to {site_name}: {site_info['url']}")
    
    # Launch undetected browser
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get(site_info["url"])
    
    time.sleep(6)  # Wait for page + ads

    # Coordinates — UPDATE THESE to match your screen!
    coords = {
        "no_thanks": (954, 276),         # location of "NO THANKS"
        "login_button": (1500, 140),      # LOGIN on header
        "email_field": (980, 325),      # Email input field
        "password_field": (980, 405),     # Password field
        "final_login": (1080, 585),        # Final LOGIN button
        "captcha_checkbox": (860, 650),   # Manual CAPTCHA checkbox
        "roll_button": (945, 905),        # ROLL! button
    }

    # NO THANKS
    click(*coords["no_thanks"])
    log("✅ 'NO THANKS' clicked")

    # LOGIN button
    click(*coords["login_button"])
    log("✅ 'LOGIN' clicked")
    time.sleep(2)

    # Email and Password
    click(*coords["email_field"])
    type_text(site_info["email"])
    
    click(*coords["password_field"])
    type_text(site_info["password"])
    log("✅ Credentials entered")

    # Final LOGIN
    click(*coords["final_login"])
    log("✅ Final login clicked")
    time.sleep(8)

    # Wait after login to let page load
    time.sleep(5)

    # Scroll to bottom (simulate PAGE_DOWN)
    pyautogui.press("pagedown")
    time.sleep(1)
    pyautogui.press("pagedown")
    time.sleep(1)

    # Click ROLL!
    click(*coords["roll_button"])
    log("🎲 'ROLL' button clicked")

    time.sleep(10)
    driver.quit()
    log("✅ Browser closed")

# Run loop
if __name__ == "__main__":
    while True:
        for site_name, site_info in sites.site_list.items():
            run_faucet(site_name, site_info)
        log("⏱ Sleeping 60 minutes...")
        time.sleep(60 * 60)
