<h1 align="center">🤖 Ecommerce Chatbot</h1>

![Static Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=White&labelColor=white&color=red)
![Static Badge](https://img.shields.io/badge/Agno-3776AB?style=for-the-badge&logo=&logoColor=White&labelColor=white&color=blue)
![Static Badge](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=black&labelColor=white&color=yellow)
![Static Badge](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=blue&labelColor=white&color=purple)
![Static Badge](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=red&labelColor=white&color=black)

![Static Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=White&labelColor=red&color=red)
![Static Badge](https://img.shields.io/badge/Agno-3776AB?style=for-the-badge&logo=&logoColor=White&labelColor=blue&color=blue)
![Static Badge](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white&labelColor=yellow&color=yellow)
![Static Badge](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=white&labelColor=purple&color=purple)
![Static Badge](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white&labelColor=black&color=black)

# End to End Ecommerce Chatbot Project: "Customer Service Chatbot for an Ecommerce Clothing Company"

# 🛍️ E-Commerce Chatbot

An GenAI-powered customer service chatbot for e-commerce, built using **LangChain, Pinecone, Groq, llama3.3 70b model**. The chatbot provides product recommendations, processes orders, tracks shipments, and remembers past conversations for a seamless user experience.


## 🚀 Features
- **Product Recommendations**: Suggests products based on user queries and budget.
- **Order Processing**: Handles multiple items, calculates totals, and generates order confirmations.
- **Order Tracking**: Provides real-time order status updates.
- **Conversational Memory**: Retains chat history using **LangGraph** for better interactions.
- **Efficient Retrieval**: Uses **Pinecone** for fast, relevant document retrieval.


## 🏗️ Tech Stack
- **Python** (Flask for Web Interface)
- **Selenium** (For Webscraping amazon website)
- **LangChain** (LLM integration & retrieval-augmented generation)
- **Pinecone** (Vector database for retrieval)
- **HTML & CSS** (Frontend for chatbot UI)
- **GROQ API** (GROQ for accessing Llama 3.3 70b model) 


## :triangular_flag_on_post: Working with the chatbot  
- Chat in natural language.  
- Ask any kind of questions related to any products to the chatbot. Some products are listed in the website mention the product name or other details and ask further questions about the product.  
- Make orders.  
- Ask for invoice of your order.  
- Ask for recommendation for example: Recommend me a shirt under the budget of rupees 1000 but above rupees 500.   
  
## :bricks: Project Overview:    
## 1. Data Collection: 
    
- The first step in our project was collecting product data from Amazon. This data includes product details, pricing, and other metadata.       
- I used selenium to automate the webscraping process.    
- collected real-world product data from Amazon using Selenium for web scraping. The dataset includes details for:    
    - Men's Formal Shirts    
    - Women's Sarees    
    - Men's Watches    
- For each product, the following attributes were extracted:  
    - Brand Name  
    - Product Name  
    - Rating  
    - Rating Count  
    - Selling Price  
    - MRP (Maximum Retail Price)  
    - Offer/Discount  
  
## 2. Data Cleaning:
    
- The collected data has to been cleaned.    
- I have to handle the missing values as we will use the data to create a vector store and missing values negatively impact the reponse of our chatbot.  
- Used mode (most occured value) to fill in the missing values.  
- Majority of missing values were in the Rating column and Rating count.  
- Some missing values were found in the Price column and MRP.  
    
## 3. Pinecone Vector Store:
    
- I used the nvidia embedding model "nvidia/nv-embedqa-mistral-7b-v2", accessed the model directly through nvidia website.    
- Once embeddings has been setup, I create the pinecone vector index.     
- Upload documents to the vector store.        
  
## 4. Initiate LLM:
  
- Used the **Groq** to access the "llama3.3 70b" model.    
- Used groq because it enhances the speed of the response of an llm which is suitable for our chatbot.     
         
## 5. Build Retriever:
  
- Load the pinecone vector store and initiate it as a retriever.    
-  Our chatbot has to remember of the conversation, therefore we have to memory / history for the chatbot. Used the inbuild "chat_history" and "session_id" to build memory for the chatbot.  
        
## 6. Deployment:
  
- Developed a Flask application to deploy the chatbot for real time access.      
- Build an ecommerce website through html, css and integrated the chatbot in it.     
- Handled the chatbot receive and response part through javascript.      
  
  
## 📸 Screenshots  
- Screenshot of the website:  (Click the icon on the right bottom of the screen to open the chatbot)   
<img src="readme_images/screenshot_1.PNG" width="950" height="550">     
<br><br>  
- Screenshot of the chatbot:    
<img src="readme_images/screenshot_2.PNG" width="400" height="450">    

## 🎯 Future Enhancements
- Support for more product categories
- Integration with payment gateways
- Multi-language support




