from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd



def scrape_products(keyword, num_products):

    try:
        path = Service(r"F:/Data Science/Projects/Ecommerce-Chatbot-Project/chromedriver.exe")
            
        # Initializing chrome_options
        chrome_options = Options()
            
        # opening the new chrome window with maximum size
        chrome_options.add_argument("--start-maximized")
            
        # timeout value for 10 seconds
        chrome_options.add_argument('--timeout=15')
            
        # scrape without a new Chrome window every time.
        # chrome_options.add_argument('headless')

        # initializing the driver
        driver = webdriver.Chrome(service=path, options=chrome_options)
            
        #driver.set_window_size(1120, 1000)

        # url of the website
        url = "https://www.amazon.in/"

        # connecting to the url
        driver.get(url)

        time.sleep(2)

        try:
            # captcha handling
            link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute("src")    # <div class=a-row a-text-center>
            
            captcha = AmazonCaptcha.fromlink(link)
            captcha_value = AmazonCaptcha.solve(captcha)

            input_field = driver.find_element(By.ID, "captchacharacters")
            input_field.send_keys(captcha_value)

            continue_shopping = driver.find_element(By.CLASS_NAME, "a-button-text")
            continue_shopping.click()

        except NoSuchElementException:
            print("No captcha found")

        time.sleep(3)

        # search product
        search_tab = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/div/input")
        search_tab.send_keys(keyword)
        search_button = driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']")
        search_button.click()
        time.sleep(3)

        data = []
        current_page = 1

        while len(data) < num_products:

            print(f"\nScraping page {current_page}")

            # for "Mens formal shirts"
            #products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base a-text-center']")
            
            # for "Sarees for women" and for "Watches for men"
            products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")
            print(f"Number of products found on page {current_page}: {len(products)}")

            # iterating through each products 
            for i in range(len(products)):
                print(f"Scraping product {i+1} on page {current_page}")
                product = products[i]   # get product element 

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
                    return df  # Immediately exits the entire function if condition is met

            # Click the "Next" button to go to the next page if the desired number of products isn't reached
            time.sleep(3)
            try:
                next_button = driver.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']")
                next_button.click()
                current_page += 1
                time.sleep(3)  
                
            except NoSuchElementException:
                print("No next page found. Ending scrape.")
                break
                
        df = pd.DataFrame(data)
        return df 
     
    finally:
        driver.quit()
    
