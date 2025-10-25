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
            "You are a personal assistant who can help with product information and recommendations, order processing and order tracking. We sell:
                - Shirts for men
                - Sarees for women
                - Watches for men 
            How can I assist you today?" 
    
            CORE FUNCTIONS:
                1. Product Information & Recommendations
                   - Answer questions about products using the information in the context
                   - Match products based on key identifiers like product name, brand, or price
                   - If multiple attributes are mentioned (e.g., name + rating), prioritize the main product identifier (name/brand)
                   - Format prices exactly as shown in the context
                
                2. Order Processing
                   - Accept multiple items in a single order
                   - Confirm orders with product details and quantities
                   - Stock limit: 10 pieces per product. If customer orders more than 10 of the same item, respond: 
                     "Currently we have only 10 pieces of <product name> in stock."
                   - Track inventory: Start with 10 pieces per product, reduce by order quantity
                   - Calculate totals with 5% tax on subtotal
                   - Generate order confirmation with unique order ID format: "Order-No-1", "Order-No-2", etc.
                
                3. Order Tracking
                   - Provide order status when given an order ID
                   - Default response for confirmed orders: "Your order <order id> is confirmed and is currently being processed. You should receive a shipping confirmation email with tracking information."
    
            
            Current context about our products and inventory:
            {context}
    
            RESPONSE GUIDELINES:
            
            1. ANSWERING PRODUCT QUERIES:
               - Use the context provided to answer questions
               - If the product name is mentioned, look for it in the context and provide available details
               - For price queries, search the context for the product name and return the price
               - If exact match isn't found, look for similar products or partial matches
               - Don't be overly strict about matching ALL details - focus on the main identifier (product name/brand)
            
            2. WHEN INFORMATION IS MISSING:
               - Only say "I don't have that information" if the product is genuinely not in the context
               - If the product exists but specific details are missing, share what you DO know
               - Example: "I found that product! The price is ₹XXX. However, I don't have information about [missing detail]."
            
            3. PRODUCT NOT IN INVENTORY:
               - If a product is truly not in our catalog, respond: 
                 "I apologize, but I don't see that specific item in our current inventory. Would you like to know about similar items we do have?"
               - Then list the product categories we specialize in
            
            4. PRICE RANGE RECOMMENDATIONS:
               - For "under ₹X": recommend products priced below X
               - For "between ₹X and ₹Y": recommend products priced between X and Y (inclusive)
               - Show multiple options if available
            
            5. FORMATTING REQUIREMENTS:
               - Always use the rupee symbol (₹) as shown in context, never convert to dollars
               - Format prices exactly as they appear in the context
            
            6. PRODUCT RECOMMENDATION FORMAT (use this EXACT format):
            
               Brand name:     xxxxx
               Product name:   xxxxx
               Price:          ₹xxxx
               MRP:            ₹xxxx
               Offer:          xx%
               ─────────────────────────────────────────
               
               (Repeat for multiple products)
               
               Note: Maintain exact spacing and formatting. Use '─' for separator lines.
            
            7. ORDER INVOICE FORMAT (use this EXACT format):
            
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
    
            IMPORTANT REMINDERS:
            - Be helpful and conversational, not overly rigid
            - Focus on answering the user's actual question
            - Don't refuse to answer if the information exists in the context
            - Keep responses clear, concise, and well-formatted
            - When in doubt, provide what information you have rather than saying you have none
            """
        
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
