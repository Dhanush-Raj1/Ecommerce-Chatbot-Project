from flask import Flask, request, render_template, url_for
from langchain_pinecone import PineconeVectorStore

from src.utils.logger import logging
from src.utils.exception import Custom_exception




app = Flask(__name__)


# route for home page
@app.route('/')
def home():
    return render_template('home_page.html')



@app.route('/chat', methods=["GET", "POST"])
def chat():
    question = request.form.get['input']
    
    vector_store = PineconeVectorStore.from_existing_documents(name='ecommercer-chatbot-project', )
    retriever = vector_store.as_retriever()
    response = retriever.invoke(question)

    return render_template('home_page.html', )



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)        