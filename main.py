import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").sheet1

# Headless Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")
print("Opening website...")

try:
    wait = WebDriverWait(driver, 20)

    # Wait for period number
    period_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "period")))
    result_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lottery-number")))
    color_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "color")))

    period = period_element.text.strip()
    result = result_element.text.strip()
    color = color_element.text.strip()
    big_small = "big" if int(result) >= 5 else "small"

    # Add row to Google Sheet
    sheet.append_row([period, result, color, big_small])
    print(f"Inserted: {period}, {result}, {color}, {big_small}")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
