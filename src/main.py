import sys 

from src.components.data_cleaning import DataCleaner
from src.components.vectorstore_builder import DataPipeline
from src.components.chatbot_builder import ChatbotBuilder

from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv

load_dotenv()

def main():
    try:    
        data_cleaner = DataCleaner()
        data_cleaner.clean_data(r"F:\Data Science\Projects\Ecommerce-Chatbot-Project\Data")

        data_pipeline = DataPipeline()
        vector_store = data_pipeline.run_pipeline(r"F:\Data Science\Projects\Ecommerce-Chatbot-Project\Data\data_cleaned.csv")

        chatbot_builder = ChatbotBuilder()
        chatbot = chatbot_builder.build_chatbot(vector_store)

        # test code
        test_response = chatbot.invoke({"input": "What do you do?"})

        logging.info(f"Test Response: {test_response}")
        print("Test response: ", test_response)

    except Exception as e:
        raise Custom_exception(e, sys)
    


if __name__=="__main__":
    main()
    
