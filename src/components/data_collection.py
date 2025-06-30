import os 
import sys 

from src.components import scraper 
from src.utils.logger import logging
from src.utils.exception import Custom_exception

from dataclasses import dataclass


products_config = [
    {
        'keyword': 'Mens formal shirts',
        'num_products': 2000,
        'file_path': 'data_shirts.csv',
    },
    {
        'keyword': 'Sarees',
        'num_products': 2000,
        'file_path': 'data_sarees.csv',
    },
    {
        'keyword': 'Watches for men',
        'num_products': 2000,
        'file_path': 'data_watches.csv',
    },
]


@dataclass
class DataCollectionConfig:
    is_airflow = os.getenv("IS_AIRFLOW", "false").lower() == "true"

    if is_airflow:
        path = '/opt/airflow/data'
    else:     
        path = 'data'   
    
 

class DataCollection:
    def __init__(self):
        self.data_collection_config = DataCollectionConfig()

    def initiate_data_collection(self):

        try:
            logging.info("Starting multi-product data collection")

            successful_products = []
            failed_products = []

            for product in products_config:
                try:
                    logging.info(f"Collecting data for: {product['keyword']}, target products: {product['num_products']}") 

                    data = scraper.scrape_products(product['keyword'], 
                                                   product['num_products'])        

                    print("Data shape for", product['keyword'], "is: ", data.shape)
                    print("Sample data for", product['keyword'], "is: ", data.head())

                    file_path = os.path.join(self.data_collection_config.path, product['file_path'])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    data.to_csv(file_path, index=False)

                    successful_products.append(product['keyword'])

                    logging.info(f"Successfully collected and saved data for: {product['keyword']}")

                except Exception as e:
                    logging.error(f"Failed to collect data for {product['keyword']}: {str(e)}")
                    failed_products.append(product['keyword'])
                    # continue scraping other products insteading of failing entire pipeline
                    continue

            logging.info(f"Data collection completed. Successful: {len(successful_products)}, Failed: {len(failed_products)}")

            if successful_products:
                logging.info(f"Successfully collected data for: {', '.join(successful_products)}")

            if failed_products:
                logging.info(f"Failed to collect data for: {', '.join(failed_products)}")


            if len(failed_products) == len(products_config):
                raise Exception("All products scraping attempt failed")
            return f"Collected data for {len(successful_products)} out of {len(products_config)} products"
        
        except Exception as e:
            logging.info(f"Error occured in multi-product data collection: {str(e)}")
            raise Custom_exception(e, sys)
        

# if __name__=="__main__":
#     data_collection = DataCollection()
#     data_collection.initiate_data_collection()
