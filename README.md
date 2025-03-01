<h1 align="center">🤖 Ecommerce Chatbot</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=black&labelColor=white&color=red" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=black&labelColor=white&color=blue" />
  <img src="https://img.shields.io/badge/Groq-234452?style=for-the-badge&logoColor=black&labelColor=white&color=brown" />
  <img src="https://img.shields.io/badge/RAG-234452?style=for-the-badge&logoColor=black&labelColor=white&color=yellow" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=black&labelColor=white&color=darkblue" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=black&labelColor=white&color=teal" />
  <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=black&labelColor=white&color=brightgreen" />
  <img src="https://img.shields.io/badge/CSS-663399?style=for-the-badge&logo=CSS&logoColor=black&labelColor=white&color=fuchsia" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=black&labelColor=white&color=cyan" />
</p>
<h1 align="center"> End to End Ecommerce Chatbot Project: "Customer Service Chatbot for an Ecommerce Clothing Company"</h1>

<br>

# 📌 Overview

An GenAI-powered customer service chatbot for e-commerce, built using **LangChain, Pinecone, Groq, llama3.3 70b model**. The chatbot provides product recommendations, processes orders, tracks shipments, and remembers past conversations for a seamless user experience.

<br>

# 🚀 Features
- **Product Recommendations**: Suggests products based on user queries and budget.
- **Order Processing**: Handles multiple items, calculates totals, and generates order confirmations.
- **Order Tracking**: Provides real-time order status updates.
- **Conversational Memory**: Retains chat history using **LangGraph** for better interactions.
- **Efficient Retrieval**: Uses **Pinecone** for fast, relevant document retrieval.

<br>

# 🏗️ Tech Stack
- **Python** (Flask for Web Interface)
- **Selenium** (For Webscraping amazon website)
- **LangChain** (LLM integration & retrieval-augmented generation)
- **Pinecone** (Vector database for retrieval)
- **HTML & CSS** (Frontend for chatbot UI)
- **GROQ API** (GROQ for accessing Llama 3.3 70b model) 

<br>

# :triangular_flag_on_post: Working with the chatbot  
- Chat in natural language.  
- Ask any kind of questions related to any products to the chatbot. Some products are listed in the website mention the product name or other details and ask further questions about the product.  
- Make orders.  
- Ask for invoice of your order.  
- Ask for recommendation for example: Recommend me a shirt under the budget of rupees 1000 but above rupees 500.   

<br>
  
# :bricks: Project Overview:    
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

<br>
  
# 📸 Screenshots  
- Screenshot of the website:  (Click the icon on the right bottom of the screen to open the chatbot)   
<img src="readme_images/screenshot_1.PNG" width="950" height="550">
     
<br>  
  
- Screenshot of the chatbot:      
<img src="readme_images/screenshot_2.PNG" width="350" height="450">    

<br>

# 📂 Project Structure
```
/📂Product-Search-Agent-WebApp
│── /📂static
│   ├── styles.css  # CSS for UI styling
│── /📂templates
│   ├── index.html  # Main webpage template
│── app.py  # Flask backend
│── agent_builder.py  # AI agent logic
│── exception.py  # Custom exception handling
│── requirements.txt  # Python dependencies
│── .env  # Environment variables
```

<br>

# 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Dhanush-Raj1/Ecommerce-Chatbot-Project.git
cd Ecommerce-Chatbot-Project
```

### 2️⃣ Create a Virtual Environment
```sh
conda create -p envi python==3.9 -y
source venv/bin/activate   # On macOS/Linux
conda activate envi     # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add:
```sh
NVIDIA_API_KEY=your_nvidia_api_key
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

### 5️⃣ Run the Flask App
```sh
python app.py
```

The app will be available at: **http://127.0.0.1:5000/**

<br>


# 🎯 Future Enhancements
- Support for more product categories
- Integration with payment gateways
- Connectivity between customers and customer service employees
- Advanced memory support with backend database connection
- Improved accuracy on product recommendations
- Multi-language support

<br>

# 🤝 Contributing  
💡 Have an idea? Feel free to contribute or open an issue and pull requests!  

# 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details. 
