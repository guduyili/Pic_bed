import time

from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:8000/docs")
        time.sleep(3)
        getlist_detail_btn = driver.find_element(By.CLASS_NAME, 'opblock-summary-control')
        getlist_detail_btn.click()
        time.sleep(3)
        try_it_out_btn = driver.find_element(By.CLASS_NAME, 'try-out__btn')
        try_it_out_btn.click()
        time.sleep(3)
        execute_btn = driver.find_element(By.CLASS_NAME, 'opblock-control__btn')
        execute_btn.click()
        time.sleep(3)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()