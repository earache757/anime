import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

# Set up WebDriver
service = Service("/usr/bin/geckodriver")
driver = webdriver.Firefox(service=service)

url = "https://work-nu-tawny.vercel.app/anime.html"
download_dir = "/home/eric/Downloads"  # Change if needed

# Gotify settings
gotify_url = "http://192.168.0.161:8098/message"  # Replace with your Gotify URL
gotify_api_key = "A7.KRQ4eEdO1sQ-"  # Replace with your Gotify API key

# Function to send Gotify notification with API key
def send_gotify_notification(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gotify_api_key}"
    }
    payload = {"title": "ICS Update", "message": message}
    try:
        response = requests.post(gotify_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print(f"Failed to send notification: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")

# Get latest file timestamp before clicking
def get_latest_ics():
    files = [f for f in os.listdir(download_dir) if f.endswith(".ics")]
    if not files:
        return None
    return max(files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))

latest_before = get_latest_ics()

driver.get(url)

# Click the button to generate the calendar
button = driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
button.click()

# Wait for ICS file to appear
print("Waiting for new ICS file to download...")
timeout = time.time() + 60  # 60 seconds timeout

downloaded_file = None
while time.time() < timeout:
    latest_after = get_latest_ics()
    
    # If there's a new file after clicking, we're good
    if latest_after and latest_after != latest_before:
        downloaded_file = latest_after
        print(f"New ICS file detected: {downloaded_file}")
        break
    
    print("No new ICS file yet, retrying...")
    time.sleep(2)  # Check every 2 seconds

if downloaded_file:
    print(f"ICS file successfully downloaded: {os.path.join(download_dir, downloaded_file)}")

    # Move the file to the correct directory and replace any existing file
    destination_dir = "/home/eric/anime_calendar"
    destination_file = os.path.join(destination_dir, "anime_schedule.ics")
    
    # Delete any existing file
    if os.path.exists(destination_file):
        os.remove(destination_file)

    # Move the new file
    os.rename(os.path.join(download_dir, downloaded_file), destination_file)
    print(f"Moved ICS to {destination_file}")

    # Send a Gotify notification
    send_gotify_notification(f"A new ICS file has been downloaded and replaced in the anime calendar folder: {downloaded_file}")
else:
    print("Timeout! No new ICS file detected.")

# Keep the browser open for 10 seconds for manual check (Optional)
time.sleep(10)

# Close the browser
driver.quit()
