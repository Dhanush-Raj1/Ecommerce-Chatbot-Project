import os 
import sys 
import time
from typing import List
from dataclasses import dataclass

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document

from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv

load_dotenv()


@dataclass
class VectorStoreBuilderConfig:
    is_airflow = os.getenv("IS_AIRFLOW", "false").lower() == "true"

    if is_airflow:
        path = "/opt/airflow/artifacts/data_cleaned.csv"

    else:
        path = "artifacts/data_cleaned.csv"

class VectorStoreBuilder:
    """
    Load data 
    Create embeddings 
    Create vector store and return the vector store 
    """

    def __init__(self):
        self.vectorstore_builder_config = VectorStoreBuilderConfig()
        
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        if not self.nvidia_api_key or not self.pinecone_api_key:
            raise ValueError("Required API keys not set")



    def load_data(self, data_path: str) -> List[Document]:
        try:
            logging.info(f"Loading data from {data_path}")
            loader = CSVLoader(file_path=data_path,
                               encoding="utf-8",
                                csv_args={"delimiter": ",",
                                          "quotechar": '"'})
            docs = loader.load()

            logging.info(f"Sample data: {docs[:5]}")
            logging.info(f"Successfully loaded {len(docs)} documents.")
            return docs 
        
        except Exception as e:
            logging.error(f"Error in loading data: {str(e)}")
            raise Custom_exception(e, sys)
    


    def create_embeddings(self) -> NVIDIAEmbeddings:
        try:
            logging.info("Initializing NVIDIA Embeddings.")
            embeddings = NVIDIAEmbeddings(
                model="nvidia/nv-embedqa-mistral-7b-v2",
                api_key=self.nvidia_api_key,
                truncate="NONE")
            
            logging.info("Embeddings initialized successfully.")
            return embeddings
        
        except Exception as e:
            logging.error(f"Error initializing embeddings: {str(e)}")
            raise Custom_exception(e, sys)
    


    def create_vector_store(self, documents: List[Document], 
                            embeddings: NVIDIAEmbeddings, 
                            index_name: str = 'ecommerce-chatbot-project') -> PineconeVectorStore:
        try:
            logging.info(f"Connecting to Pinecone and creating index: {index_name}")
            pc = Pinecone(api_key=self.pinecone_api_key)

            pc.create_index(name=index_name,
                             dimension = 4096,
                             metric="cosine",
                             spec=ServerlessSpec(cloud="aws",region="us-east-1"))
            
            time.sleep(10)
            index = pc.Index(index_name)
            time.sleep(10)

            initial_stats = index.describe_index_stats()
            logging.info(f"Index status before uploading: {initial_stats}")

            vector_store = PineconeVectorStore.from_documents(documents=documents,
                                                              index_name=index_name, 
                                                              embedding = embeddings)
            
            final_stats = index.describe_index_stats()
            logging.info(f"Index status after uploading: {final_stats}")

            logging.info(f"Successfully created vector store with {len(documents)} documents")
            return vector_store
        
        except Exception as e:
            logging.error(f"Error creating vector store: {str(e)}")
            raise Custom_exception(e, sys)
        


    def run_pipeline(self) -> PineconeVectorStore:
        try:
            logging.info("Starting vectorstore pipeline")
            docs = self.load_data(self.vectorstore_builder_config.path)
            embeddings = self.create_embeddings()
            vector_store = self.create_vector_store(docs, embeddings)

            logging.info("Vectorstore pipeline completed successfully")
            return vector_store
        
        except Exception as e:
            logging.error(f"Error in pipeline execution: {str(e)}")
            raise Custom_exception(e, sys)




# if __name__=="__main__":
#     pipe = DataPipeline()
#     pipe.run_pipeline(r"F:\Data Science\Projects\Ecommerce-Chatbot-Project\Data")