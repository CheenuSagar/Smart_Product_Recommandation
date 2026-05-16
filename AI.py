git from flask import Flask, render_template, request, jsonify
from crewai import Agent, Task, Crew

try:
    from langchain.chat_models import ChatOllama
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        ChatOllama = None

from datetime import datetime
import json
import os
import requests
from typing import List, Dict
import threading
import time

app = Flask(__name__)

# Initialize LLM
llm = None
crew_enabled = False
if ChatOllama is not None:
    try:
        llm = ChatOllama(model="llama3.2")
        crew_enabled = True
    except Exception:
        llm = None

if not crew_enabled:
    llm = "dummy"

# Database for tracking products and prices
PRODUCTS_DB = "products_db.json"
ALERTS_DB = "alerts_db.json"

def load_db(filename):
    """Load database from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_db(filename, data):
    """Save database to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def search_products_api(query: str, budget: float) -> List[Dict]:
    """
    Search products from APIs (Fake API for demonstration)
    In production, integrate with real APIs like:
    - Amazon Product API
    - eBay API
    - Price comparison APIs
    """
    # Simulated product data (in production, use real APIs)
    products_db = {
        "laptop": [
            {"id": 1, "name": "Dell XPS 13", "price": 1299, "rating": 4.8, "features": "Intel i7, 16GB RAM, 512GB SSD"},
            {"id": 2, "name": "MacBook Air M2", "price": 1199, "rating": 4.7, "features": "Apple M2, 8GB RAM, 256GB SSD"},
            {"id": 3, "name": "ASUS Vivobook 15", "price": 699, "rating": 4.5, "features": "Intel i5, 8GB RAM, 256GB SSD"},
        ],
        "phone": [
            {"id": 4, "name": "iPhone 14", "price": 999, "rating": 4.7, "features": "A16 Bionic, 128GB, iOS 16"},
            {"id": 5, "name": "Samsung Galaxy S23", "price": 899, "rating": 4.6, "features": "Snapdragon 8 Gen 2, 128GB, Android 13"},
            {"id": 6, "name": "Google Pixel 7", "price": 599, "rating": 4.5, "features": "Tensor, 128GB, Android 13"},
        ],
        "tablet": [
            {"id": 7, "name": "iPad Pro", "price": 1099, "rating": 4.8, "features": "M2 chip, 128GB, 12.9 inch"},
            {"id": 8, "name": "Samsung Galaxy Tab S9", "price": 799, "rating": 4.6, "features": "Snapdragon 8 Gen 1, 128GB, 11 inch"},
            {"id": 9, "name": "Amazon Fire HD 10", "price": 199, "rating": 4.3, "features": "MediaTek, 32GB, 10 inch"},
        ],
        "headphones": [
            {"id": 10, "name": "Sony WH-1000XM5", "price": 399, "rating": 4.8, "features": "Noise Cancel, 30hr battery, Wireless"},
            {"id": 11, "name": "Apple AirPods Max", "price": 549, "rating": 4.7, "features": "Spatial Audio, 20hr battery, Wireless"},
            {"id": 12, "name": "Anker Soundcore", "price": 99, "rating": 4.4, "features": "BassUp, 50hr battery, Wireless"},
        ]
    }
    
    # Normalize query
    query = query.lower().strip()
    
    # Filter by category and budget
    results = []
    
    # Search in each category
    for category, products in products_db.items():
        # Check if query matches category or if query is empty (show all categories if no preference)
        if query == '' or category.lower() in query.lower() or query in category.lower():
            for product in products:
                if product['price'] <= budget:
                    results.append(product)
    
    # If no exact category match, search all products if budget is reasonable
    if not results and query.strip():
        for category, products in products_db.items():
            for product in products:
                if product['price'] <= budget:
                    results.append(product)
    
    # Sort by rating
    results.sort(key=lambda x: x['rating'], reverse=True)
    return results

def compare_products(products: List[Dict]) -> str:
    """Compare products and return comparison analysis"""
    if not products:
        return "No products found to compare."
    
    comparison = "Product Comparison:\n\n"
    for i, product in enumerate(products[:3], 1):
        comparison += f"{i}. {product['name']}\n"
        comparison += f"   Price: ${product['price']}\n"
        comparison += f"   Rating: {product['rating']}/5.0\n"
        comparison += f"   Features: {product['features']}\n\n"
    
    return comparison

# Define Agents only if a valid LLM is available
search_agent = None
comparison_agent = None
alert_agent = None
if crew_enabled:
    search_agent = Agent(
        role="Product Search Agent",
        goal="Find products based on user budget and preferences",
        backstory="Expert at searching and filtering products from multiple sources",
        llm=llm,
        verbose=True
    )

    comparison_agent = Agent(
        role="Product Comparison Agent",
        goal="Compare products and recommend the best option based on price, rating, and features",
        backstory="Expert at analyzing product specifications and comparing features",
        llm=llm,
        verbose=True
    )

    alert_agent = Agent(
        role="Price Alert Agent",
        goal="Track price changes and alert users when prices drop",
        backstory="Expert at monitoring prices and notifying users of deals",
        llm=llm,
        verbose=True
    )

@app.route('/')
def index():
    """Serve the chatbot UI"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '')
    budget = data.get('budget', 1000)
    preferences = data.get('preferences', '')
    
    try:
        # If CrewAI and a supported LLM are available, create tasks for the crew.
        if crew_enabled and search_agent is not None and comparison_agent is not None:
            search_task = Task(
                description=f"User wants to find a {preferences} product within budget of ${budget}. Search for the best options.",
                agent=search_agent,
                expected_output="List of recommended products"
            )
            
            comparison_task = Task(
                description=f"Compare the found products and recommend the best one based on price, rating, and features for budget ${budget}",
                agent=comparison_agent,
                expected_output="Best product recommendation with reasoning"
            )
            
            # Create crew
            crew = Crew(
                agents=[search_agent, comparison_agent],
                tasks=[search_task, comparison_task],
                verbose=True
            )

        # Get search results
        search_results = search_products_api(preferences, budget)
        
        if search_results:
            comparison = compare_products(search_results)
            response = f"Found {len(search_results)} products matching your criteria:\n\n{comparison}"
        else:
            response = f"Sorry, no products found within your budget of ${budget}. Try increasing your budget or changing preferences."
        
        return jsonify({
            'status': 'success',
            'response': response,
            'products': search_results[:3]  # Return top 3 products
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f"An error occurred: {str(e)}"
        })

@app.route('/api/set-alert', methods=['POST'])
def set_alert():
    """Set price alert for a product"""
    data = request.json
    product_id = data.get('product_id')
    target_price = data.get('target_price')
    email = data.get('email', '')
    
    try:
        alerts_db = load_db(ALERTS_DB)
        alert_key = f"alert_{product_id}_{datetime.now().timestamp()}"
        
        alerts_db[alert_key] = {
            'product_id': product_id,
            'target_price': target_price,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        
        save_db(ALERTS_DB, alerts_db)
        
        return jsonify({
            'status': 'success',
            'message': f"Price alert set! You'll be notified when price drops to ${target_price}"
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Error setting alert: {str(e)}"
        })

@app.route('/api/track-price', methods=['POST'])
def track_price():
    """Track price changes for a product"""
    data = request.json
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    current_price = data.get('current_price')
    
    try:
        products_db = load_db(PRODUCTS_DB)
        
        if product_id not in products_db:
            products_db[product_id] = {
                'name': product_name,
                'price_history': []
            }
        
        products_db[product_id]['price_history'].append({
            'price': current_price,
            'timestamp': datetime.now().isoformat()
        })
        
        save_db(PRODUCTS_DB, products_db)
        
        return jsonify({
            'status': 'success',
            'message': 'Price tracked successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Error tracking price: {str(e)}"
        })

@app.route('/api/get-price-history', methods=['GET'])
def get_price_history():
    """Get price history for a product"""
    product_id = request.args.get('product_id')
    
    try:
        products_db = load_db(PRODUCTS_DB)
        
        if product_id in products_db:
            return jsonify({
                'status': 'success',
                'product': products_db[product_id]
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Error fetching price history: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)