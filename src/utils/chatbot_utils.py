import os 
import sys
from typing import Any

from langchain_nvidia import NVIDIAEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.utils.logger import logging
from src.utils.exception import Custom_exception
from dotenv import load_dotenv
load_dotenv()



class BuildRetrievalchain:
    """
    contains helper function for creating chatbot
    embeddings, llm, prompt, vector_store, retriever, retrieval_chain
    """

    def __init__(self):
        pass

    def load_embeddings(self):
        try:
            logging.info("Initializing NVIDIA Embeddings.")
            embeddings = NVIDIAEmbeddings(model="nvidia/nv-embedqa-mistral-7b-v2",
                                        api_key=os.getenv("NVIDIA_API_KEY"),
                                        truncate="NONE")
                
            logging.info("Embeddings initialized successfully.")
            return embeddings
            
        except Exception as e:
            logging.error(f"Error initializing embeddings: {str(e)}")
            raise Custom_exception(e, sys)



    def load_llm(self):
        try:
            logging.info("Initializing Llama2 model with Groq")
            llm = ChatGroq(temperature=0.6,
                        model_name="llama-3.3-70b-versatile",
                        groq_api_key=os.getenv("GROQ_API_KEY"),
                        max_tokens=4096)
            
            logging.info("LLM initialized successfully")
            return llm
            
        except Exception as e:
            logging.error(f"Error initializing LLM: {str(e)}")
            raise Custom_exception(e, sys)
        


    def setup_prompt(self):
        try:
            logging.info("Creating prompt template")
            system_prompt = """You are a knowledgeable and friendly personal assistant" 
            
            Your role: 
            "I'm your personal assistant and I can help with product information and recommendations, order processing and order tracking. We sell
                - Shirts for men
                - Sarees for women
                - Watches for men 
            How can I assist you today?" 

            Your store specializes in:
            - Men's shirts 
            - Women's sarees
            - Watches for men 

            CORE FUNCTIONS:
                1. Product Information & Recommendations
                   - ONLY provide details explicitly mentioned in the context
                   - Format prices exactly as shown in the context
                
                2. Order Processing
                   - Accept multiple items in a single order
                   - Confirm the order. If the customer/user buy more than 10 pieces of the same product respond "Currenlty we have only 10 pieces of the product <product which customer requested>"
                     NOTE: every product has 10 pieces as its stock, you have to keep track of the stock and if the product is out of stock, just say so.
                   - Calculate accurate totals including any applicable taxes/shipping. The tax rate is 5% and 5% of tax to every order.
                   - Generate order confirmation with unique order ID. The order ID should be like this "Order-No-1", change the "1" to "2" and "2" to "3".... for new orders
                
                3. Order Tracking
                   - Provide real-time order status when given an order ID
                   - Only share tracking information from the provided context
                   - If asked the status of the order response: "Your order <order id> is confirmed and is currently being processed. You should receive a shipping confirmation email with tracking information"

            
            Current context about our products and inventory:
            {context}

            IMPORTANT INSTRUCTIONS:
            1. ONLY provide information that is explicitly mentioned in the context provided
            2. If specific details (prices, brands, materials) of a product are not in the context, DO NOT make them up.
            3. Include relevant details about materials, styles, and pricing IF AND ONLY they are in the context
            4. If asked about products we don't carry or aren't in the context, say "I apologize, but I don't see that specific item in our current inventory. Would you like to know about similar items we do have?" 
                        and then provide the types of products/items which you specialize in and which are in your inventory.
            5. If you're unsure or don't have enough information, say so directly
            6. When asked to recommend a product under or inbetween certain price range, recommend those product which is under or inbetween the price range, in other words recommend the product which meets the user's condition.
                        for example: User asks you "Recommend me a shirt under rupees 500", you should recommend only those mens shirt which is priced under rupees 500. 
                        another example: User asks you "Recommend me a shirt under rupess 1000 and above rupees 500", you should recommend only those mens shirts which is priced above 500 rupess and below 1000 rupees.
                This is very important don't respond that you do not have 
            7. Format prices exactly as they appear in the context, don't modify them especially the rupee symbol with the dollar symbol
            8. Most importantly when you are recommending a product your response should be in this EXACT format:
                            Brand name :    xxxxx
                            Product name:   xxxxx
                            Price:          xxxxx
                            MRP:            xxxxx
                            Offer:          xxxxx   
                Note: Maintain exact spacing and formatting. Use '─' for lines.
                Even if there are multiple products to recommend maintain the format as it is easy to understand and appealing.
             9. Generate invoices in this EXACT format (maintain the spacing and lines):

                        Order Invoice
                        ─────────────────────────────────────────
                        Item                     Qty    Price    
                        ─────────────────────────────────────────
                        [Product Name]            x1    ₹XXX.XX
                        [Product Name]            x2    ₹XXX.XX
                        ─────────────────────────────────────────
                        Subtotal:                       ₹XXX.XX
                        Tax (5%):                       ₹XX.XX
                        ─────────────────────────────────────────
                        Total:                          ₹XXX.XX
                        
                        Order ID: Order-No-X

                        Note: Maintain exact spacing and formatting. Use '─' for lines.
                        
            Remember: 
            - If you're not 100% certain about a detail, don't mention it
            - Better to say "I don't have that information" than to make assumptions
            - Only reference products and details that are explicitly provided above in the context
            - Be professional but brief in your responses
            - No assumptions or guesses
            - No unnecessary explanations or small talk
            - Keep responses focused and factual"""
        
            prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                        MessagesPlaceholder(variable_name="chat_history"),  # For maintaining conversation history
                                                        ("human", "{input}")]) 
            
            logging.info("Prompt template has been created")
            return prompt
        
        except Exception as e:
            logging.error(f"Error creating prompt: {str(e)}")
            raise Custom_exception(e, sys)
            


    def load_vectorstore(self, embeddings):
        try:
            logging.info("Loading vectorstore ")
            vector_store = PineconeVectorStore.from_existing_index(index_name="ecommerce-chatbot-project",
                                                                   embedding=embeddings)

            logging.info("Successfully loaded vectorstore")
            return vector_store
        
        except Exception as e:
            raise Custom_exception(e, sys)
        


    def build_retriever(self, vector_store: PineconeVectorStore):
        try:

            logging.info("Initializing vector_store as retriever")
            retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
                                                  search_kwargs={"k": 5,                    # Number of documents to return
                                                                 "score_threshold": 0.7})   # Minimum relevance threshold
                                                            
            logging.info("Retriever has be initializing")
            return retriever
        
        except Exception as e:
            logging.info(f"Error initializing retriever: {str(e)}")
            raise Custom_exception(e, sys)
        


    def build_chains(self, llm: Any, prompt: ChatPromptTemplate, retriever: Any):
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
        


    def build_retrieval_chain(self):
        try:
            embeddings = self.load_embeddings()
            llm = self.load_llm()
            prompt = self.setup_prompt()
            vector_store = self.load_vectorstore(embeddings)
            retriever = self.build_retriever(vector_store)
            retrieval_chain = self.build_chains(llm, prompt, retriever)

            return retrieval_chain
        except Exception as e:
            raise Custom_exception(e, sys)
        
    
    

class BuildChatbot:
    def __init__(self):
        self.store = {}  # Persistent dictionary to maintain chat history


    def get_session_id(self, session_id: str) -> BaseChatMessageHistory:
        """creates and retrieves a chat history session."""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]


    def initialize_chatbot(self):
        """Initializes the chatbot with session memory."""
        utils = BuildRetrievalchain()
        retrieval_chain = utils.build_retrieval_chain()

        chatbot = RunnableWithMessageHistory(runnable=retrieval_chain,
                                             get_session_history=self.get_session_id,
                                             input_messages_key="input",
                                             history_messages_key="chat_history",
                                             output_messages_key="answer")

        return chatbot
