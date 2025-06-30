from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging
import sys
import os

sys.path.append('/opt/airflow')

from src.components.data_collection import DataCollection
from src.components.data_cleaning import DataCleaner
from src.components.vectorstore_builder import VectorStoreBuilder
from src.components.chatbot_builder import ChatbotBuilder

from langchain_pinecone import PineconeVectorStore

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,               # does the current DAG run depends on the previous DAG run? 
    'start_date': datetime(2025, 6, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=4),    # if a task fails in a dag run, it will be retried after 4 minutes  
                                            # we can try to solve the error within 4 minutes for a successfull rerun
}

dag = DAG(
    'Ecommerce-Chatbot-Pipeline',
    default_args=default_args,
    description='Ecommerce Chatbot Pipeline',
    schedule_interval=None,               # DAG runs will start only with a manual trigger 
    catchup=False,
)


# task functions
def collect_data():
    DataCollection().initiate_data_collection()

def clean_data():
    DataCleaner().clean_data()

def build_vectorstore():                                # creating the vectorstore
    VectorStoreBuilder().run_pipeline()       

def build_chatbot():
    pipeline = VectorStoreBuilder()                     # loading the created vectorstore as we don't want to pass the result from one task to another 
    embeddings = pipeline.create_embeddings()
    vector_store = PineconeVectorStore.from_existing_index(
        index_name="ecommerce-chatbot-project", 
        embedding=embeddings
    )
   
    ChatbotBuilder().build_chatbot(vector_store)


with dag:
    task1 = PythonOperator(
        task_id='data_collection',
        python_callable=collect_data
    )

    task2 = PythonOperator(
        task_id='data_cleaning',
        python_callable=clean_data
    )

    task3 = PythonOperator(
        task_id='vectorstore_build',
        python_callable=build_vectorstore
    )

    task4 = PythonOperator(
        task_id='chatbot_build',
        python_callable=build_chatbot
    )

    task1 >> task2 >> task3 >> task4