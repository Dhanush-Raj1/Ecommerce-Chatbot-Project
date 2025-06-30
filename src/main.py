import sys 

from src.components.data_collection import DataCollection
from src.components.data_cleaning import DataCleaner
from src.components.vectorstore_builder import VectorStoreBuilder
from src.components.chatbot_builder import ChatbotBuilder

from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv

load_dotenv()

def main():
    try:    
        # data_collection = DataCollection()
        # data_collection.initiate_data_collection()

        data_cleaner = DataCleaner()
        data_cleaner.clean_data()

        vectorstore_builder = VectorStoreBuilder()
        vector_store = vectorstore_builder.run_pipeline()

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
    
