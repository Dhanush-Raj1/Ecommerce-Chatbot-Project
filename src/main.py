import sys 
from src.components.vectorstore_builder import DataPipeline
from src.components.chatbot_builder import ChatbotBuilder

from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv

load_dotenv()

def main():
    try:    
        data_pipeline = DataPipeline()
        vector_store = data_pipeline.run_pipeline(r"F:\Data Science\Projects\Ecommerce-Chatbot-Project\Data")

        chatbot_builder = ChatbotBuilder()
        chatbot = chatbot_builder.build_chatbot(vector_store)

        # test code
        test_input = "What do you do?"
        test_response = chatbot.invoke({"input": "What do you do?"})

        logging.info(f"Test Input: {test_input}")
        logging.info(f"Test Response: {test_response}")
        print("Test response: ", test_response)

    except Exception as e:
        raise Custom_exception(e, sys)
    


if __name__=="__main__":
    main()
    
