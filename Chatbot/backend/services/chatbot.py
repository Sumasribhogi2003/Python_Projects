import openai
from models.db import get_db_connection

# Chatbot function to handle queries and fetch data
def handle_query(query: str):
    # Interact with LangChain or another LLM
    response = summarize_query_with_llm(query)

    # Example: Fetch relevant product or supplier info from the database
    if "product" in query.lower():
        data = fetch_product_data(query)
    elif "supplier" in query.lower():
        data = fetch_supplier_data(query)
    else:
        data = []

    return response, data

# Example function to fetch product data from the database
def fetch_product_data(query: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    result = cursor.fetchall()
    connection.close()
    return result

# Example function to fetch supplier data from the database
def fetch_supplier_data(query: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM suppliers WHERE name LIKE '%{query}%'")
    result = cursor.fetchall()
    connection.close()
    return result

# Placeholder function to summarize the query using LLM (e.g., GPT-3, GPT-2, or LangChain)
def summarize_query_with_llm(query: str):
    # Use your LLM here (example using OpenAI's GPT-3)
    openai.api_key = "your-openai-api-key"
    prompt = f"Summarize this query: {query}"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the correct model for summarization
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
