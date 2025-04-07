import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").sheet1

# Setup Selenium and Chromium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)

# Open Wingo Game Page
driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")
time.sleep(8)

# Extract period and result
try:
    period = driver.find_element(By.CLASS_NAME, "gameRecordExpect").text.strip()
    result = driver.find_element(By.CLASS_NAME, "gameRecordNumber").text.strip()

    result_digits = result.split(" ")
    total = sum(int(x) for x in result_digits)

    size = "Big" if total >= 14 else "Small"
    color = (
        "Green" if total in [1,4,7,10,16,19,22,25]
        else "Red" if total in [3,6,9,12,15,18,21,24]
        else "Violet"
    )

    # Save to Google Sheet
    sheet.append_row([period, result, size, color])
    print("Data Saved:", period, result, size, color)

except Exception as e:
    print("Error occurred:", e)

driver.quit()
