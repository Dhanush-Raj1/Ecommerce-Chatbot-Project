import os 
import sys
from typing import Any

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_pinecone import PineconeVectorStore


from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv

load_dotenv()


class ChatbotBuilder:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        

    def create_llm(self):
        try:
            logging.info("Initializing Llama2 model with Groq")
            llm = ChatGroq(temperature=0.6,
                           model_name="llama-3.3-70b-versatile",
                           groq_api_key=self.api_key,
                           max_tokens=4096)
            
            logging.info("LLM initialized successfully")
            return llm
        
        except Exception as e:
            logging.error(f"Error initializing LLM: {str(e)}")
            raise Custom_exception(e, sys)
        

    def create_prompt(self):
        try:
            logging.info("Creating prompt template")

            system_prompt = """You are a knowledgeable and friendly fashion consultant for a high-end e-commerce store. 
            Your store specializes in:
            - Men's clothing
            - Women's clothing
            - Watches for men 

            Guidelines for interaction:
            1. Be warm and professional in your responses
            2. Provide specific product recommendations based on the context
            3. Include relevant details about materials, styles, and pricing when available
            4. If asked about products we don't carry, politely explain our product range
            6. Always prioritize customer satisfaction while being honest about product availability

            Current context about our products and inventory:
            {context}
            
            Remember: Only provide information based on the context above. If certain details aren't available, 
            be honest and offer to help the customer find relevant alternatives or suggest contacting customer service for more specific information."""
        
            prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                        #MessagesPlaceholder(variable_name="chat_history"),  # For maintaining conversation history
                                                        ("human", "{input}")]) 

            logging.info("Prompt template has been created")
            return prompt
        
        except Exception as e:
            logging.error(f"Error creating prompt: {str(e)}")
            raise Custom_exception(e, sys)
        

    def create_retriever(self, vector_store: PineconeVectorStore):
        try:
            logging.info("Initializing vector_store as retriever")
            retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
                                                  search_kwargs={"score_threshold": 0.7})
            
            logging.info("Retriever has be initializing")
            return retriever
        
        except Exception as e:
            logging.info(f"Error initializing retriever: {str(e)}")
            raise Custom_exception(e, sys)
        

    def create_chains(self, llm: Any, prompt: ChatPromptTemplate, retriever: Any):
        try:
            logging.info("Creating stuff document chain...")
            doc_chain = create_stuff_documents_chain(llm=llm, 
                                                     prompt=prompt,
                                                     output_parser=StrOutputParser(),
                                                     document_variable_name="context")
            
            logging.info("Creating retrieval chain...")
            retrieval_chain = create_retrieval_chain(retriever=retriever, 
                                                     combine_docs_chain=doc_chain)
            
            logging.info("Chains created successfully")
            return retrieval_chain
        
        except Exception as e:
            logging.info(f"Error creating chains {str(e)}")
            raise Custom_exception(e, sys)
        

    def build_chatbot(self, vector_store: PineconeVectorStore):
        try:
            logging.info("Starting chatbot building")
            llm = self.create_llm()
            prompt = self.create_prompt()
            retriever = self.create_retriever(vector_store)
            retrieval_chain = self.create_chains(llm, prompt, retriever)
            
            logging.info("Chatbot building completed successfully")
            return retrieval_chain
        
        except Exception as e:
            logging.error(f"Error in model building: {str(e)}")
            raise Custom_exception(e, sys)
