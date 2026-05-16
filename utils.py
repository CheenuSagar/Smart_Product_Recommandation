import json
import os
from datetime import datetime
from typing import List, Dict, Optional

def load_json_db(filename: str) -> Dict:
    """Load database from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_json_db(filename: str, data: Dict) -> bool:
    """Save database to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False

def parse_budget_from_message(message: str) -> Optional[float]:
    """Extract budget amount from user message"""
    import re
    match = re.search(r'\$(\d+(?:\.\d{2})?)', message)
    if match:
        return float(match.group(1))
    
    # Try to find spelled out numbers
    numbers = {
        'hundred': 100,
        'thousand': 1000,
        'million': 1000000
    }
    for word, value in numbers.items():
        if word in message.lower():
            match = re.search(rf'(\d+)\s*{word}', message.lower())
            if match:
                return float(match.group(1)) * value
    return None

def format_price(price: float, currency: str = 'USD') -> str:
    """Format price with currency"""
    if currency == 'USD':
        return f"${price:,.2f}"
    return f"{price:,.2f} {currency}"

def calculate_value_score(price: float, rating: float, budget: float) -> float:
    """Calculate value-for-money score (0-100)"""
    if price > budget:
        return 0
    
    # Price factor: closer to budget is worse, much cheaper is better
    price_factor = (1 - (price / budget)) * 50 if price <= budget else 0
    
    # Rating factor: higher rating is better
    rating_factor = (rating / 5.0) * 50
    
    return min(100, price_factor + rating_factor)

def get_product_category(product_name: str) -> Optional[str]:
    """Identify product category from name"""
    categories = {
        'laptop': ['dell', 'hp', 'lenovo', 'asus', 'macbook', 'mac', 'xps'],
        'phone': ['iphone', 'samsung', 'pixel', 'nokia', 'oneplus'],
        'tablet': ['ipad', 'galaxy tab', 'surface', 'fire'],
        'headphones': ['airpods', 'sony', 'bose', 'sennheiser', 'jbl']
    }
    
    product_lower = product_name.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in product_lower:
                return category
    return None

def create_price_alert(
    product_id: int,
    product_name: str,
    current_price: float,
    target_price: float,
    user_email: str
) -> Dict:
    """Create a price alert entry"""
    return {
        'product_id': product_id,
        'product_name': product_name,
        'current_price': current_price,
        'target_price': target_price,
        'user_email': user_email,
        'created_at': datetime.now().isoformat(),
        'triggered': False,
        'triggered_at': None
    }

def check_price_alerts(
    product_id: int,
    current_price: float,
    alerts_db: Dict
) -> List[Dict]:
    """Check if any alerts should be triggered for a product"""
    triggered_alerts = []
    
    for alert_key, alert_data in alerts_db.items():
        if (alert_data['product_id'] == product_id and 
            current_price <= alert_data['target_price'] and 
            not alert_data['triggered']):
            triggered_alerts.append(alert_data)
            alert_data['triggered'] = True
            alert_data['triggered_at'] = datetime.now().isoformat()
    
    return triggered_alerts

def format_product_comparison(products: List[Dict]) -> str:
    """Format products for comparison display"""
    if not products:
        return "No products found to compare."
    
    comparison = "📊 Product Comparison:\n\n"
    
    for i, product in enumerate(products[:5], 1):
        comparison += f"{i}. **{product['name']}**\n"
        comparison += f"   💰 Price: {format_price(product['price'])}\n"
        comparison += f"   ⭐ Rating: {product['rating']}/5.0\n"
        comparison += f"   📋 Features: {product['features']}\n"
        
        # Calculate and show value score
        budget = max(product['price'] * 1.5, 1000)  # Estimate budget
        value = calculate_value_score(product['price'], product['rating'], budget)
        comparison += f"   📈 Value Score: {value:.1f}/100\n\n"
    
    return comparison

def get_recommendation_reason(product: Dict, competitors: List[Dict]) -> str:
    """Generate recommendation reason based on comparison"""
    reasons = []
    
    # Best price
    min_price = min(p['price'] for p in competitors)
    if product['price'] <= min_price:
        reasons.append("Best price")
    
    # Best rating
    max_rating = max(p['rating'] for p in competitors)
    if product['rating'] == max_rating:
        reasons.append("Highest rated")
    
    # Best value (price vs rating)
    product_value = calculate_value_score(
        product['price'], 
        product['rating'], 
        max(p['price'] for p in competitors)
    )
    max_value = max(
        calculate_value_score(p['price'], p['rating'], max(c['price'] for c in competitors))
        for p in competitors
    )
    if product_value == max_value:
        reasons.append("Best value for money")
    
    if reasons:
        return f"Recommended because: {', '.join(reasons)}"
    return "Solid option with good features"

def export_chat_history(history: List[Dict], filename: str = 'chat_history.json') -> bool:
    """Export chat history to JSON file"""
    return save_json_db(filename, {'messages': history, 'exported_at': datetime.now().isoformat()})

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
