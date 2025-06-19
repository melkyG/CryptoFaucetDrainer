import undetected_chromedriver as uc
import pyautogui
import pytesseract
from PIL import Image
import pyperclip
import re
import webbrowser
import time
from datetime import datetime
import sites  # your sites.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your images
ASSET_PATH = r"C:\Users\gmelk\OneDrive\Desktop\Trading & Coding\Python Projects\CryptoFaucetDrainer\assets"
pyautogui.FAILSAFE = False
MAX_RETRIES = 3
GREEN = '\033[92m'
RESET = '\033[0m'
RED = '\033[91m'
YELLOW = '\033[93m'

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
    log("[🌐] Starting VPN automation")

    for attempt in range(MAX_RETRIES):
        pyautogui.hotkey("ctrl", "esc")
        time.sleep(1.5)
        pyautogui.write("nordvpn", interval=0.05)
        time.sleep(1)
        pyautogui.press("enter")
        if click_image("quickconnect2.png", confidence=0.7, timeout=5):
            log("'Quick Connect' clicked")
            break
        else:
            log(f"trying again... {attempt + 1}")
            
    """    
    start_time = time.time()

    while time.time() - start_time < 25:
        if click_image("quickconnect2.png", confidence=0.7, timeout=5):
            log("'Quick Connect' clicked")
            break
        else:
            time.sleep(1) 
            try: click_image("changeconnection.png") 
            except:
                print("couldnt find changeconnection")
      
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
    """
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

    # NO THANKS
    for attempt in range(MAX_RETRIES):
        if click_image("nothanks.png", confidence=0.7, timeout=8):
            log("'NO THANKS' clicked")
            time.sleep(1)
            break
        else:
            log(f"NO THANKS not found, trying again... {attempt + 1}") 
    
    # LOGIN button
    for attempt in range(MAX_RETRIES):
        if click_image("login.png", confidence=0.7, timeout=7):
            log("'LOGIN' clicked")
            time.sleep(1)
            break
        else:
            log(f"'LOGIN' not found, trying again... {attempt + 1}") 
    
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
    click_image("login2.png") #click(*coords["final_login"])
    log(f"{GREEN}✅ Final 'LOGIN!' clicked{RESET}")
    
    #"""
    # Check for authentication message
    auth_needed = True
    #"""
    try:
        log("checking for authentication message..")
        auth_needed = click_image("authmessage.png", confidence=0.7, timeout=20)
    except Exception as e:
        log(f"❌ Could not detect auth message: {e}")
        auth_needed = False
    
    #"""
    if auth_needed:
        log("🔐 Auth message detected, beginning manual authentication flow...")
        print("looking for chrome")
        # Reveal Start menu and launch Chrome
        for attempt in range(MAX_RETRIES):
            pyautogui.hotkey("ctrl", "esc")
            time.sleep(1.5)
            if click_image("chrome.png", confidence=0.94, timeout=10):
                log("📨 'Chrome' clicked")
                break
            else:
                print(f"No chrome found, trying again... {attempt + 1}") 
        
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

        if not click_image("authemail.png", confidence=0.7, timeout=15):
            # Click Gmail search bar
            if click_image("searchmail.png", confidence=0.7, timeout=20):
                log("🔍 Search Mail clicked")
                time.sleep(1)
                pyautogui.write("freebitco.in", interval=0.05)
                pyautogui.press("enter")
                time.sleep(5)


            try:
                print("checking for recent..")
                recent = click_image("mostrecent.png", confidence=0.6, timeout=10)
                time.sleep(3)
                pyautogui.click()
                pyautogui.moveRel(0, 60, duration=0.5)
                pyautogui.click()
            except Exception as e:
                log(f"❌ Not Recent: {e}")
                recent = False
            
        log("📧 First email clicked")
        time.sleep(6)
        for _ in range(30):  # Scroll down 20 times
            pyautogui.press("pagedown")
            time.sleep(0.3)

        """
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
        """
        click_image("locatelink.png")
        pyautogui.moveRel(0, 33, duration=0.5)
        pyautogui.rightClick()
        time.sleep(1.5)
        click_image("copylink.png")

        # Reveal Start menu and launch Chrome
        for attempt in range(MAX_RETRIES):
            pyautogui.hotkey("ctrl", "esc")
            time.sleep(1.5)
            if click_image("chrome.png", confidence=0.94, timeout=10):
                log("📨 'Chrome' clicked")
                break
            else:
                print(f"No chrome found, trying again... {attempt + 1}") 
        time.sleep(7)

        click_image("guest.png")
        time.sleep(7)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

        if click_image("confirm.png", confidence=0.7, timeout=20):
            log("Confirm clicked")
            log("waiting for redirecting...")
            time.sleep(42)
            
    else:
        log("✅ No authentication needed")
    

    

    claim_ready = False

    for attempt in range(MAX_RETRIES):
        pyautogui.press("pagedown")
        time.sleep(1.5)
        pyautogui.press("pagedown")
        time.sleep(1.5)

        if click_image("notready.png", confidence=0.7, timeout=15):
            log(f"{RED}⚠️ Claim not ready. (might've logged into wrong acc){RESET}")
            break

        log(f"🔍 Attempt {attempt + 1} to find 'verify.png'")
        if click_image("verify.png", confidence=0.7, timeout=15):
            log("🔐 'Verify' clicked")
            claim_ready = True
            time.sleep(10)
            break
        else:
            log("⚠️ 'verify.png' not found on this attempt. Will retry.")

    if claim_ready:
        # Click ROLL!
        pyautogui.press("pagedown")
        click_image("roll.png")
        log("🎲 'ROLL' button clicked")
        time.sleep(4)
        pyautogui.scroll(+100) 
        for attempt in range(MAX_RETRIES):
            if click_image("closeplaynow.png", confidence=0.7, timeout=15):
                log("🎉 Roll success detected")
                break
            else:
                log(f"couldnt find close button, trying again... {attempt + 1}")
        time.sleep(2)
        pyautogui.scroll(-650) 

        start_time = time.time()

        while time.time() - start_time < 15:
            if click_image("rollsuccess.png", confidence=0.7, timeout=15):
                log("🎉 Roll success detected")
                found_result = True

                # Screenshot and OCR
                screenshot = pyautogui.screenshot()
                text = pytesseract.image_to_string(screenshot)

                match = re.search(r"You win ([\d.]+) BTC", text)
                if match:
                    btc_reward = match.group(1)
                    log(f"{GREEN}💰 Reward detected: {YELLOW}{btc_reward} {RED}BTC{RESET}")
                else:
                    log("⚠️ Roll success, but reward text not found.")
                break

            elif click_image("0.png", confidence=0.7, timeout=15):
                log(f"{RED}⚠️ Busted by captcha. Retry in 5 mins!{RESET}")
                found_result = True
                break

        if not found_result:
            log("⚠️ No roll result detected within 15 seconds.")

    time.sleep(10)
    driver.quit()
    log("✅ Browser closed")
    log("brb 4 min nap (due to same site)")
    time.sleep(301)


# Run loop
if __name__ == "__main__":
    while True:
        log("Starting new run...")
        countdown = 5
        start_time = time.time()

        for i in range(countdown):
            log(f"{countdown}...")
            time.sleep(1)
            countdown -= 1

        for site_name, site_info in sites.site_list.items():
            ensure_vpn_connected()
            run_faucet(site_name, site_info)
        log("⏱ Sleeping 60 minutes...")
        time.sleep(60 * 60)
