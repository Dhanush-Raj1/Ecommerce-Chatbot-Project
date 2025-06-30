<h1 align="center">🤖 Ecommerce Chatbot</h1>
<h3 align="center"> End to End MLOps Data Science Project: "Customer Service Chatbot for an Ecommerce Clothing Company"</h3>
<h3 align="center">LLM-powered Ecommerce Chatbot with MLOps (Apache Airflow Orchestration)</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=black&labelColor=white&color=FFD43B" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=black&labelColor=white&color=1C3C3C" />
  <img src="https://img.shields.io/badge/Apache%20Airflow-blue?style=for-the-badge&logo=apache-airflow&logoColor=black&labelColor=white&color=#148f77" />
  <img src="https://img.shields.io/badge/Groq-234452?style=for-the-badge&logoColor=black&labelColor=white&color=f4a852" />
  <img src="https://img.shields.io/badge/Pinecone_DataBase-234452?style=for-the-badge&logoColor=black&labelColor=green&color=cyan" />
  <img src="https://img.shields.io/badge/RAG-234452?style=for-the-badge&logoColor=black&labelColor=white&color=yellow" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=black&labelColor=white&color=darkblue" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=black&labelColor=white&color=teal" />
  <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=black&labelColor=white&color=E34F26" />
  <img src="https://img.shields.io/badge/CSS-663399?style=for-the-badge&logo=CSS&logoColor=black&labelColor=white&color=fuchsia" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=black&labelColor=white&color=blue" />
</p>

<br>

# 📌 Ecommerce Chatbot
A GenAI-powered customer service chatbot designed for an e-commerce clothing company. Built with **LangChain, Pinecone, Groq, llama3.3 70b model**. The chatbot provides product recommendations, processes orders, tracks shipments, and remembers past conversations for a seamless user experience. The full pipeline — from data collection to chatbot deployment — is automated and orchestrated using **Apache Airflow**, enabling scalable and production-grade MLOps workflows.

<br>

## 🎯 Project Overview
### 1. Data Collection
- The first step in our project was collecting **real world product data** from Amazon.
- Implemented automated web scraping using Selenium to extract product information from Amazon.
- Targeted different product categories including:
    - Formal Shirts for men
    - Sarees for women
    - Watches for men
- For each category the below details has been collected:
    - Brand name
    - Product name
    - Rating
    - Rating counts
    - Selling Price
    - MRP (original price)
    - Offer percentage

### 2. Data Cleaning and Preprocessing
- Performed thorough data cleaning and preprocessing on the collected dataset
- Handled missing values in ratings, rating counts, and other relevant columns
- Applied mode imputation to replace missing values as most of the columns are categorical

### 3. Vector Embedding
- Leveraged NVIDIA's embedding model "nv-embedqa-mistral-7b-v2" for vector embeddings
- Selected this model based on its top performance on the MTEB leaderboard
- Implemented embedding generation through the LangChain framework

### 4. Loading the Embeddings to Pinecone Vector Store
- Transferred generated embeddings to Pinecone, Pinecone is a purpose-built vector database for AI applications
- First created a Pinecone index using Python and 
- Uploaded the embeddings to the index to enable semantic search capabilities

### 5. LLM Model and Prompt Engineering
- Integrated "llama-3.3-70b-versatile" model via Groq through the LangChain framework
- Selected Groq for its significant enhancements in computational efficiency and response speed
- Developed optimized prompts with specific instructions and guidelines to maximize model performance and response

### 6. Setting up RAG (Retrieval Augmented Generation)
- Setup the Pinecone vector store as an retriever
- Created document chain after LLM and prompt configuration
- Created retrieval chain utilizing both the retriever and document chain
- Finally our fully functional RAG-based chatbot system is to be used

### 7. Flask Web Application
- Developed a web interface using Flask framework
- Created an e-commerce website with integrated chatbot functionality using HTML and CSS
- Handled the chatbot receive and response part through javascript.    
- The final result delivers a user experience that is similar in a interaction with a customer service representative of a clothing company

### 8. MLOps Integration with Apache Airflow
- Integrated Apache Airflow to orchestrate the complete data pipeline.
- Each pipeline stage is defined as a task:
    - Data Collection DAG: Scrapes product data from Amazon using Selenium.
    - Data Cleaning DAG: Cleans and preprocesses raw product data.
    - Vector Store Builder DAG: Embeds product data and stores it in Pinecone.
    - Chatbot Builder DAG: Builds and updates the chatbot using LLaMA and LangChain.
- The pipeline runs daily at a scheduled time automatically as a result the chatbot gets trained with new product data. 
- Enables better automation, monitoring, retry handling.

<br>

# 🚀 Features
- **MLOps Orchestration**: Automates and monitors the entire pipeline with **Apache Airflow**.
- **Product Recommendations**: Suggests products based on user queries and budget.
- **Order Processing**: Handles multiple items, calculates totals, and generates order confirmations.
- **Order Tracking**: Provides real-time order status updates.
- **Conversational Memory**: Retains chat history using **LangGraph** for better interactions.
- **Efficient Retrieval**: Uses **Pinecone** for fast, relevant document retrieval.

<br>

# 🏗️ Tech Stack
- **Python**  
- **Flask** (Flask for Web Interface)
- **Apache Airflow** (MLOps pipeline orchestration)
- **Selenium** (For Webscraping amazon website)
- **LangChain** (LLM integration & retrieval-augmented generation)
- **Pinecone** (Vector database for retrieval)
- **GROQ API** (GROQ for accessing Llama 3.3 70b model)
- **HTML & CSS** (Frontend for chatbot UI)


<br>

# 📂 Project Structure
```
/📂Ecommerce-Chatbot-Project
│── /📂dags                             # dag pipeline
│   ├── pipeline.py
│── /📂artifacts                             # artifact files
│   ├── data_cleaned.csv    
│── /📂data                             # Data collected from amazon                   
|   ├── data_shirts.csv                  
│   ├── data_sarees.csv                      
│   ├── data_watches.csv             
│── /📂readme_images                  # Screenshots of the webapp
│   │── screenshot_1.png
│   │── screenshot_2.png
│── /📂src                            # Source files (core files of the project)
|   ├── main.py                       # Running the chabot locally
|   │── /📂components                 # Main components files
|   |  ├── scraper.py                
|   |  ├── data_colletion.py          
|   |  ├── data_cleaning.py          
|   |  ├── vectorstore_builder.py     
|   |  ├── chatbot_builder.py         
|   │── /📂utils                      # Utilities files 
|   |  ├── exception.py                
|   |  ├── logger.py                  
|   |  ├── chatbot_utils.py            
│── /📂static                         # Static folder
|   │── /📂css                        # Css files 
|   |   │── hp_style.css              # Home page styles
|   │── /📂images                     # Website Images
|   │── /📂js                         # javascripts  
│── /📂templates                      # Templates (html files)
|   │── /home_page.html
│── .gitignore
│── LICENCE
│── README.md
│── app.py                            # Flask backend
│── chromedriver.exe                  # Chrome driver application
│── docker-compose.yml                # airflow docker container configuration
│── dockerfile                  # airflow image 
│── requirements.txt                  # Python dependencies
│── setup.py                          # Setup
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

### 6️⃣ Run airflow pipeline
```sh
docker-compose up --build
```

Access the Airflow UI at **http://localhost:8080/** and trigger the DAGs manually or set a schedule for automation.

<br>

# :triangular_flag_on_post: Working with the chatbot  
- Chat in natural language.  
- Ask any kind of questions related to any products to the chatbot. Some products are listed in the website mention the product name or other details and ask further questions about the product.  
- Make orders.  
- Ask for invoice of your order.  
- Ask for recommendation for example: Recommend me a shirt under the budget of rupees 1000 but above rupees 500.   

<br>

# 📸 Screenshots  
### Screenshot of the website:  *(Click the icon on the right bottom of the screen to open the chatbot)*  
<img src="readme_images/screenshot_1.PNG" width="950" height="550">  
     
<br>  
  
### Screenshot of the chatbot:      
<img src="readme_images/screenshot_2.PNG" width="350" height="450">    

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

<br>

# 📄 License
This project is licensed under the **MIT License** – [LICENSE](LICENSE)  
