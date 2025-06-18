import undetected_chromedriver as uc
import pyautogui
import pyperclip
import re
import webbrowser
import time
from datetime import datetime
import sites  # your sites.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Path to your images
ASSET_PATH = r"C:\Users\gmelk\OneDrive\Desktop\Trading & Coding\Python Projects\CryptoFaucetDrainer\assets"
pyautogui.FAILSAFE = False
MAX_RETRIES = 3

"""
print("Move your mouse to the desired position. Ctrl+C to stop.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone.")
"""

def open_link_in_fresh_session(url):
    options = Options()
    options.add_argument("--guest")  # Or use --guest for full isolation
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    # This avoids using default profile or cookies
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    print(f"🧼 Opened clean session for: {url}")
    # Optional: wait for user or time before closing
    time.sleep(15)  # Adjust as needed
    #driver.quit()

# Helper to locate and click an image
def click_image(image_name, confidence=0.8, timeout=10):
    image_path = os.path.join(ASSET_PATH, image_name)
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                pyautogui.click(location)
                return True
        except pyautogui.ImageNotFoundException:
            pass  
        time.sleep(0.5)

    print(f"[⚠️] Image not found: {image_name}")
    return False

# Main function to connect to VPN
def ensure_vpn_connected():
    print("[🌐] Starting VPN automation")

    #pyautogui.moveTo(1274, 1078, duration=2)  # Reveal taskbar
    pyautogui.hotkey("ctrl", "esc")
    time.sleep(1)

    pyautogui.write("nordvpn", interval=0.05)
    time.sleep(1)
    pyautogui.press("enter")
    start_time = time.time()

    while time.time() - start_time < 25:
        if click_image("quickconnect2.png", confidence=0.7, timeout=5):
            break
        else: 
            time.sleep(1)

      
    try: click_image("finish.png", confidence=0.7, timeout=5)
    except:
        print("finishing setup...")
        time.sleep(10)

    

    try: click_image("changeconnection.png")    
    except:
        print("couldnt find changeconnection")
        try: click_image("quickconnect2.png")
        except:
            print("couldnt find quickconnect2")

    print("[⏳] Waiting for VPN to establish connection...")
    time.sleep(15)

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
    #"""
    log(f"🌐 Connecting to {site_name}: {site_info['url']}")
    
    # Launch undetected browser
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get(site_info["url"])
    # Clear cookies for FreeBitco.in before doing anything else
    driver.delete_all_cookies()
    driver.refresh()
    log("🧹 Cleared cookies and refreshed")
    
    time.sleep(10)  # Wait for page + ads

    # Coordinates — UPDATE THESE to match your screen!
    coords = {
        "no_thanks": (954, 276),         # location of "NO THANKS"
        "login_button": (1500, 140),     # LOGIN on header
        "email_field": (980, 325),       # Email input field
        "password_field": (980, 405),    # Password field
        "final_login": (1080, 585),      # Final LOGIN button
        "captcha_checkbox": (860, 650),  # Manual CAPTCHA checkbox
        "roll_button": (945, 910),       # ROLL! button
    }

    # NO THANKS
    click(*coords["no_thanks"])
    log("✅ 'NO THANKS' clicked")
    time.sleep(1)

    # LOGIN button
    click(*coords["login_button"])
    log("✅ 'LOGIN' clicked")
    time.sleep(2)

    for attempt in range(MAX_RETRIES):
        if click_image("emailaddress.png", confidence=0.7, timeout=15):
            pyautogui.moveRel(0, 30, duration=0.5)
            pyautogui.click()
            type_text(site_info["email"])
            break
        else:
            pyautogui.scroll(-200) 
            time.sleep(1)
  
    
    click_image("password.png") #click(*coords["password_field"])
    type_text(site_info["password"])
    log("✅ Credentials entered")
    time.sleep(1)

    # Final LOGIN
    click_image("login.png") #click(*coords["final_login"])
    log("✅ Final login clicked")
    time.sleep(6)
    #"""

    # Check for authentication message
    auth_needed = True
    #"""
    try:
        print("checking for authentication message..")
        auth_needed = click_image("authmessage.png", confidence=0.7, timeout=10)
    except Exception as e:
        log(f"❌ Could not detect auth message: {e}")
        auth_needed = False
    
    #"""
    if auth_needed:
        log("🔐 Auth message detected, beginning manual authentication flow...")

        # Reveal Start menu and launch Chrome
        pyautogui.hotkey("ctrl", "esc")
        time.sleep(1.5)

        print("looking for chrome")
        if click_image("chrome.png", confidence=0.94, timeout=10):
            log("📨 'Chrome' clicked")
        time.sleep(7)

        click_image("whousing.png")
        time.sleep(7)

        # Open new tab
        if not click_image("newtab.png"):
            if not click_image("newtab2.png"):
                click_image("newtab3.png")
        time.sleep(7)

        # Launch Gmail
        if click_image("gmail.png", confidence=0.7, timeout=15):
            log("📫 Gmail clicked")
            time.sleep(12)

        # Click Gmail search bar
        if click_image("searchmail.png", confidence=0.7, timeout=20):
            log("🔍 Search Mail clicked")
            time.sleep(1)
            pyautogui.write("freebitco.in", interval=0.05)
            pyautogui.press("enter")
            time.sleep(5)

        # Sort by recent if possible
        recent = True
        try:
            print("checking for recent..")
            recent = click_image("mostrecent.png", confidence=0.6, timeout=10)
            time.sleep(3)
            pyautogui.click()
            pyautogui.moveRel(0, 60, duration=0.5)
        except Exception as e:
            log(f"❌ Not Recent: {e}")
            recent = False

        if not recent:
            click_image("mostrelevant.png", confidence=0.7, timeout=10)
            log("📨 'Most relevant' clicked")
            time.sleep(2)
            if click_image("mostrecent.png", confidence=0.7, timeout=10):
                log("📨 'Most recent' clicked")
                pyautogui.moveRel(0, -10, duration=0.5)
                time.sleep(2)

        # Click top email
        pyautogui.click()
        
        log("📧 First email clicked")
        time.sleep(6)
        for _ in range(20):  # Scroll down 20 times
            pyautogui.press("pagedown")
            time.sleep(0.3)


        
        # Copy email content
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1.5)

        # Extract content from clipboard
        email_text = pyperclip.paste()
        log(f"📋 Email text length: {len(email_text)}")
        log(f"📋 Email text preview:\n{email_text[:500]}")  # Preview first 500 characters
        time.sleep(1.5)
        #print("📋 Clipboard content:")
        #print(email_text)

        # Get the local-part (before the @) of the email used for this run
        expected_to = site_info["email"].split('@')[0]
        time.sleep(1.5)

        # Find all "to <email>" lines and the link(s) that follow them
        blocks = re.findall(r'to ([^\s]+).*?(https?://[^\s">]*freebitco\.in[^\s">]*)', email_text, re.DOTALL)

        # Filter to only include links for the current email's local-part
        matching_links = [link for to_field, link in blocks if expected_to in to_field]

        if matching_links:
            link = matching_links[-1]  # Pick the last (most recent) link
            log(f"🔗 Found latest verification link for {expected_to}: {link}")
            log(f"Manually verify this link: {link}")
            open_link_in_fresh_session(link)
        
        click_image("link.png")
        if click_image("confirm.png", confidence=0.7, timeout=20):
            log("Confirm clicked")
            time.sleep(42)
            
    else:
        log("✅ No authentication needed")
        time.sleep(7)
    


    # Scroll to bottom (simulate PAGE_DOWN)
    pyautogui.press("pagedown")
    time.sleep(1)
    pyautogui.press("pagedown")
    time.sleep(7)

    found_verify = False

    for attempt in range(MAX_RETRIES):
        log(f"🔍 Attempt {attempt + 1} to find 'verify.png'")
        if click_image("verify.png", confidence=0.7, timeout=15):
            log("🔐 'Verify' clicked")
            time.sleep(10)
            found_verify = True
            break
        else:
            pyautogui.press("f5")
            time.sleep(5)
            pyautogui.press("pagedown")
            time.sleep(1)
            pyautogui.press("pagedown")
            time.sleep(7)

    if not found_verify:
        log("⚠️ 'verify.png' not found after retries. Continuing without clicking.")

    # Click ROLL!
    pyautogui.press("pagedown")
    click_image("roll.png")
    log("🎲 'ROLL' button clicked")

    time.sleep(10)
    driver.quit()
    log("✅ Browser closed")
    log("brb 5 min nap (due to same site)")
    time.sleep(301)


# Run loop
if __name__ == "__main__":
    while True:
        for site_name, site_info in sites.site_list.items():
            #ensure_vpn_connected()
            run_faucet(site_name, site_info)
        log("⏱ Sleeping 60 minutes...")
        time.sleep(60 * 60)
