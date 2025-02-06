import os 
import sys 

from src.components import scraper 
from src.utils.logger import logging
from src.utils.exception import Custom_exception

from dataclasses import dataclass

@dataclass
class DataCollectionConfig:
    path = os.path.join('Data', 'data_watches.csv')   # 'data_shirts.csv'


class DataCollection:
    def __init__(self):
        self.data_collection_config = DataCollectionConfig()

    def initiate_data_collection(self):
        try:
            logging.info("Data collection of watches has been started")

            #collect_data = scraper.scrape_products("Mens formal shirts", 2000)
            #collect_data = scraper.scrape_products("Sarees", 2000)
            collect_data = scraper.scrape_products("Watches for men", 2000)   
            collect_data

            os.makedirs(os.path.dirname(self.data_collection_config.path), exist_ok=True)

            logging.info("Storing the data")
            collect_data.to_csv(self.data_collection_config.path, index=False)

            logging.info("Data collection of watches has been completed")
        
        except Exception as e:
            raise Custom_exception(e, sys)
        

if __name__=="__main__":
    data_collection = DataCollection()
    data_collection.initiate_data_collection()


    