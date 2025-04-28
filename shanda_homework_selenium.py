from selenium import webdriver
import time
import os
import sys
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains

def execute_folder():
    return os.path.dirname(os.path.abspath(__file__))

def get_mobile_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", { "deviceName": "iPhone SE" })  
    chrome_options.add_experimental_option("detach", True)

    driver_path = os.path.join(execute_folder(), "chromedriver.exe")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def take_screenshot(driver, prefix="screenshot"):
    try:
        base_folder = execute_folder()
        screenshot_folder = os.path.join(base_folder, "screenshot")
        os.makedirs(screenshot_folder, exist_ok=True)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(screenshot_folder, f"{prefix}_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"Error occurred in take_screenshot: {e}")

import csv
import os
import time

def save_credit_card_links_report(data, prefix="credit_card_links"):
    try:
        base_folder = execute_folder()
        report_folder = os.path.join(base_folder, "report")
        os.makedirs(report_folder, exist_ok=True)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(report_folder, f"{prefix}_{timestamp}.csv")

        with open(report_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["項目", "連結"])
            for item in data:
                writer.writerow([item["text"], item["href"]])

        print(f"Report saved to {report_path}")

    except Exception as e:
        print(f"Error occurred in save_credit_card_links_report: {e}")

def navigate_to_cathaybk_and_screemshot(driver):
    try:
        url = "https://www.cathay-cube.com.tw/cathaybk"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Successfully navigated to the new page: {url}")
        time.sleep(3)
        
        take_screenshot(driver, "cathaybk")

    except Exception as e:
        print(f"Error occurred in Navigate_to_cathaybk_and_screemshot: {e}")

def navigate_and_count_credit_cards(driver):
    try:
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-mb-btn-burger')]"))
        )
        menu_button.click()
        time.sleep(1)

        product_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'產品介紹')]"))
        )
        product_button.click()
        time.sleep(1)

        credit_card_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='spa-root']/div/div[6]/div[1]/div/div[1]/div[2]/div[1]/div/header/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div[1]"))
        )
        credit_card_button.click()
        time.sleep(2)

        all_links = driver.find_elements(By.XPATH, "//a[@title and contains(@class, 'cursor-pointer')]")
        keyword_list = ["卡片介紹", "刷卡優惠", "小樹點", "卡友登錄", "卡友理財", "卡友權益", "行動支付", "申請信用卡"]
        results = []

        for link in all_links:
            title = link.get_attribute("title")
            href = link.get_attribute("href")
            if title and any(keyword in title for keyword in keyword_list):
                print(f"{title}: {href}")
                results.append({"text": title, "href": href})

        print(f"\n總共找到 {len(results)} 筆資料")

        save_credit_card_links_report(results)

        take_screenshot(driver, "credit_card_list")

    except Exception as e:
        print(f"Error occurred: {e}")

def click_swiper_and_screenshot(driver):
    try:
        card_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'卡片介紹')]"))
        )
        card_link.click()
        time.sleep(3)

        stop_card_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='cubre-a-iconTitle__text' and text()='停發卡']"))
        )

        swiper_bullets = stop_card_element.find_elements(By.XPATH, ".//following::span[contains(@class, 'swiper-pagination-bullet')]")

        print(f"總共找到 {len(swiper_bullets)} 個 swiper bullet（從停發卡後開始）")

        for idx in range(len(swiper_bullets)):
            bullets = stop_card_element.find_elements(By.XPATH, ".//following::span[contains(@class, 'swiper-pagination-bullet')]")
            current_bullet = bullets[idx]

            bullet_location = current_bullet.location_once_scrolled_into_view
            driver.execute_script(f"window.scrollTo(0, {bullet_location['y'] - 200});")
            time.sleep(0.5)

            current_bullet.click()
            print(f"點擊第 {idx+1} 個 swiper bullet")

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f".//following::span[contains(@class, 'swiper-pagination-bullet-active') and @aria-label='Go to slide {idx+1}']"))
            )

            time.sleep(0.8)

            take_screenshot(driver, prefix=f"slide_{idx+1}")

            time.sleep(0.5)

    except Exception as e:
        print(f"Error during click_swiper_and_screenshot: {e}")

if __name__ == "__main__":
    driver = get_mobile_driver()
    navigate_to_cathaybk_and_screemshot(driver)
    navigate_and_count_credit_cards(driver)
    click_swiper_and_screenshot(driver)
    time.sleep(3)
    input(" Mobile view is active. Press Enter to exit...")
