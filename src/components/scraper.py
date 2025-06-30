from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import pandas as pd
import uuid
import os
import shutil

from src.utils.exception import Custom_exception
from src.utils.logger import logging

def scrape_products(keyword:str, num_products:int) -> pd.DataFrame:
        
        driver = None
        unique_user_data_dir = None

        try:
            is_airflow = os.getenv("IS_AIRFLOW", "false").lower() == 'true'
            logging.info(f"Running in {'Airflow' if is_airflow else 'local'} environment")

            if is_airflow:
                path = "/usr/bin/chromedriver"
            else:
                path = "F:/Data Science/Projects/4.Ecommerce-Chatbot-Project/chromedriver.exe"

            # Initializing chrome_options
            chrome_options = Options()
            
            # configuration for airflow environment
            if is_airflow:
                unique_user_data_dir = f"/tmp/chrome_user_data_{uuid.uuid4()}"         # Create unique temporary directory for this Chrome instance 
                os.makedirs(unique_user_data_dir, exist_ok=True)

                chrome_options.add_argument(f"--user-data-dir={unique_user_data_dir}")
                chrome_options.binary_location = "/usr/bin/chromium"                   # chromium path in the container
                chrome_options.add_argument('--headless=new')                          # scrape without a new Chrome window every time.


            # configuration for both local and airflow environments 
            chrome_options.add_argument("--window-size=1920,1080")  # opening the new chrome window with maximum size

            # initializing the driver 
            driver = webdriver.Chrome(service=Service(path), options=chrome_options)
            
            # timeouts after driver initialization
            driver.set_page_load_timeout(30)  # 30 seconds for page load
            driver.implicitly_wait(10)        # 10 seconds for element finding
            
            logging.info("Chrome driver initialized successfully")
            
            url = "https://www.amazon.in/"

            try:
                logging.info(f"Attempting to navigate to: {url}")
                driver.get(url)
                logging.info(f"Successfully navigated to: {driver.current_url}")
            except Exception as nav_error:
                print(f"Error navigating to URL: {nav_error}")
                logging.error(f"Error navigating to URL: {nav_error}")
                # Try alternative approach
                driver.execute_script(f"window.location.href = '{url}';")
                time.sleep(5)   

            time.sleep(2)

            try:
                # captcha handling
                link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute("src")    # <div class=a-row a-text-center>
                
                captcha = AmazonCaptcha.fromlink(link)
                captcha_value = AmazonCaptcha.solve(captcha)

                logging.info("Captcha found and bypassing...")

                input_field = driver.find_element(By.ID, "captchacharacters")
                input_field.send_keys(captcha_value)

                continue_shopping = driver.find_element(By.CLASS_NAME, "a-button-text")
                continue_shopping.click()
                logging.info("Captcha bypassed successfully")

            except NoSuchElementException:
                logging.info("No captcha found")

            time.sleep(3)

            # search product
            #search_tab = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/div/input")
            search_tab = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
            #search_tab = driver.find_element(By.XPATH, "/html/body/div[1]/header/div[1]/div[1]/div[2]/div/form/div[2]/div[1]/input")  
                                                
            search_tab.send_keys(keyword)
            search_button = driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']")
            search_button.click()
            time.sleep(3)

            data = []
            current_page = 1

            while len(data) < num_products:

                logging.info(f"Scraping page {current_page}")

                # for "Mens formal shirts"
                #products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base a-text-center']")
                
                # for "Sarees for women" and for "Watches for men"
                products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")
                logging.info(f"Number of products found on page {current_page}: {len(products)}")

                # iterating through each products 
                # for i in range(len(products)):
                #     print(f"Scraping product {i+1} on page {current_page}")
                #     product = products[i] 

                for product in products:
                    total_scraped = len(data)+1
                    logging.info(f"Scraping product {total_scraped} on page {current_page}")

                    try:
                        brand_name = product.find_element(By.XPATH,".//h2[@class='a-size-mini s-line-clamp-1']//span").text
                    except:
                        brand_name = "na"
                    
                    try:   
                        product_name = product.find_element(By.XPATH, ".//h2[@class='a-size-base-plus a-spacing-none a-color-base a-text-normal']//span").text
                    except:
                        product_name = "na"
                        
                    try:
                        # .text doesn't work because of unknown factors like css, therefore we use 'textContent'
                        rating_element = product.find_element(By.XPATH, ".//i[@data-cy='reviews-ratings-slot']//span")
                        rating = rating_element.get_attribute('textContent')
                    except:
                        rating = "na"

                    try: 
                        rating_count = product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text
                    except:
                        rating_count = "na"

                    try: 
                        selling_price_element = product.find_element(By.XPATH, ".//span[@class='a-price']//span[@class='a-offscreen']")
                        selling_price = selling_price_element.get_attribute('textContent')
                    except:
                        selling_price = "na"
                    
                    try: 
                        mrp = product.find_element(By.XPATH, ".//span[@class='a-price a-text-price']//span[@aria-hidden='true']").text
                    except:
                        mrp = "na"

                    try: 
                        offer = product.find_element(By.XPATH, ".//div[@class='a-row']//span[contains(text(), '%')]").text
                    except:
                        offer = "na"
                    
                    # try:
                    #     delivery_price = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/span/div/div/div[2]/div[5]/div/div[2]/span/span[1]")
                    # except:
                    #     delivery_price = "na"


                    data.append({"Brand Name": brand_name,
                                "Product Name": product_name,
                                "Rating": rating,
                                "Rating Count": rating_count,
                                "Selling Price": selling_price,
                                "MRP": mrp,
                                "Offer": offer})
                                #"Delivery Price: ", delivery_price})
                
                    # Break out of the loop if the desired number of products is reached
                    if len(data) == num_products:
                        #break
                        df = pd.DataFrame(data)
                        return df                       # Immediately exits the entire function if condition is met

                # Click the "Next" button to go to the next page if the desired number of products isn't reached
                time.sleep(3)
                try:
                    next_button = driver.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']")
                    next_button.click()
                    current_page += 1
                    logging.info(f"Moving to next page: {current_page}")
                    time.sleep(3)  
                    
                except NoSuchElementException:
                    logging.info("No next page found. Ending scrape.")
                    break 
                    
            df = pd.DataFrame(data)
            return df 
        
        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise Custom_exception(e, sys)

        finally:
            # quit driver 
            if driver is not None:
                try:
                    driver.quit()
                    logging.info("Chrome driver closed successfully")
                except Exception as cleanup_error:
                    logging.error(f"Error closing driver: {cleanup_error}")
            
            # Clean up temporary directory
            if unique_user_data_dir and os.path.exists(unique_user_data_dir):
                try:
                    shutil.rmtree(unique_user_data_dir, ignore_errors=True)
                    logging.info("Temporary directory cleaned up")
                except Exception as cleanup_error:
                    logging.info(f"Error cleaning temp directory: {cleanup_error}")