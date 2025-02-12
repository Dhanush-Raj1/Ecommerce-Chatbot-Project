# End to End Ecommerce Chatbot Project: "Customer Service Chatbot for an Ecommerce Clothing Company"

# 🛍️ E-Commerce Chatbot

An AI-powered customer service chatbot for e-commerce, built using **LangChain, Pinecone, Groq, llama3.3 70b model**. The chatbot provides product recommendations, processes orders, tracks shipments, and remembers past conversations for a seamless user experience.


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


## :bricks: Project Overview:
### 1. Data Collection
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

2. Data Cleaning
    - The collected data has to been cleaned.
    - I have to handle the missing values as we will use the data to create a vector store and missing values negatively impact the reponse of our chatbot.
    - Used mode (most occured value) to fill in the missing values.
    - Majority of missing values were in the Rating column.
    - Some missing values were found in the Price column.
  
3. Pinecone Vector Store
    - Create embeddings
    - Create vector store
    - Upload documents to the vector store      

4. Initiate LLM 
    - Initiate llm through Groq
      
5. Build Retriever
      - load the vector store, turn it in to retriever
      - setup chat history through session_id
6. Deployment
      - Flask
      - Html, css, js 


## 📸 Screenshots
(Include chatbot UI and order processing screenshots here)

## 🎯 Future Enhancements
- Support for more product categories
- Integration with payment gateways
- Multi-language support

## 📜 License
This project is licensed under the MIT License.

---

🎉 **Happy Shopping with Your AI Assistant!**

