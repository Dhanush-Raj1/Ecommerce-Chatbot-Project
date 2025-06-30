import os 
import sys
from typing import Any

from langchain_groq import ChatGroq
from langchain_core.caches import BaseCache
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

            #ChatGroq.model_rebuild()

            llm = ChatGroq(temperature=0.6,
                           model_name="llama-3.3-70b-versatile",
                           groq_api_key=self.api_key,
                           max_tokens=4096,)
                           #cache=True)
            
            logging.info("LLM initialized successfully")
            return llm
        
        except Exception as e:
            logging.error(f"Error initializing LLM: {str(e)}")
            raise Custom_exception(e, sys)
        

    def create_prompt(self):
        try:
            logging.info("Creating prompt template")

            system_prompt = """You are a knowledgeable and friendly fashion consultant for a high-end e-commerce store. 

            IMPORTANT INSTRUCTIONS:
            1. ONLY provide information that is explicitly mentioned in the context provided
            2. If specific details (prices, brands, materials) of a product are not in the context, DO NOT make them up and do not recommend that product to the customer, recommend someother product
            3. If you're unsure or don't have enough information, say so directly
            4. Do not reference any brands or products that aren't specifically mentioned in the context
            5. Format prices exactly as they appear in the context, don't modify them
            
            Your store specializes in:
            - Men's clothing
            - Women's clothing
            - Watches for men 

            Guidelines for interaction:
            1. Be warm and professional in your responses
            2. Provide specific product recommendations ONLY from the context
            3. Include relevant details about materials, styles, and pricing IF AND ONLY IF they are in the context
            4. If asked about products we don't carry or aren't in the context, say "I apologize, but I don't see that specific item in our current inventory. Would you like to know about similar items we do have?"
            5. When suggesting alternatives, only mention products that are explicitly in the context

            Current context about our products and inventory:
            {context}
            
            Remember: 
            - If you're not 100% certain about a detail, don't mention it
            - Better to say "I don't have that information" than to make assumptions
            - Only reference products and details that are explicitly provided above in the context"""
        
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
            retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.7}
            )
            
            logging.info("Retriever has been initialized")
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
