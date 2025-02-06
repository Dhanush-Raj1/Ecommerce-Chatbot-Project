import os
import logging
from datetime import datetime

logs_file_name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + ".log" 
logs_folder_name = datetime.now().strftime('%d_%m_%Y')

logs_path = os.path.join(os.getcwd(), "Logs", logs_folder_name)
os.makedirs(logs_path, exist_ok=True)

logs_file_path = os.path.join(logs_path, logs_file_name)

logging.basicConfig(filename=logs_file_path,
                    format="[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)



if __name__=="__main__":
    logging.info("Logging has started.")

