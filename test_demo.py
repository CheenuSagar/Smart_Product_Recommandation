#!/usr/bin/env python3
"""
Demo script to test the Smart Product Recommendation Agent
Run this to verify the system works before launching the web server
"""

import json
from utils import (
    parse_budget_from_message,
    format_price,
    calculate_value_score,
    format_product_comparison,
    validate_email
)

def test_utils():
    """Test utility functions"""
    print("=" * 60)
    print("🧪 Testing Utility Functions")
    print("=" * 60)
    
    # Test budget parsing
    print("\n1️⃣ Budget Parsing:")
    test_messages = [
        "Find me a laptop under $1000",
        "Show me phones under 600 dollars",
        "Tablet within 5 hundred",
    ]
    for msg in test_messages:
        budget = parse_budget_from_message(msg)
        print(f"   '{msg}' → ${budget}")
    
    # Test price formatting
    print("\n2️⃣ Price Formatting:")
    prices = [999.99, 1299.50, 199.00]
    for price in prices:
        print(f"   {price} → {format_price(price)}")
    
    # Test value score
    print("\n3️⃣ Value Score Calculation:")
    test_cases = [
        (799, 4.8, 1000),
        (1299, 4.5, 1500),
        (199, 4.0, 300),
    ]
    for price, rating, budget in test_cases:
        score = calculate_value_score(price, rating, budget)
        print(f"   Price: {format_price(price)}, Rating: {rating}/5, Budget: {format_price(budget)}")
        print(f"   → Value Score: {score:.1f}/100\n")
    
    # Test email validation
    print("4️⃣ Email Validation:")
    test_emails = [
        "user@example.com",
        "invalid.email@",
        "another@domain.co.uk",
        "notanemail",
    ]
    for email in test_emails:
        valid = validate_email(email)
        print(f"   {email} → {'✅ Valid' if valid else '❌ Invalid'}")

def test_product_data():
    """Test product data structure"""
    print("\n" + "=" * 60)
    print("📦 Testing Product Data")
    print("=" * 60)
    
    sample_products = [
        {
            "id": 1,
            "name": "Dell XPS 13",
            "price": 1299,
            "rating": 4.8,
            "features": "Intel i7, 16GB RAM, 512GB SSD"
        },
        {
            "id": 3,
            "name": "ASUS Vivobook 15",
            "price": 699,
            "rating": 4.5,
            "features": "Intel i5, 8GB RAM, 256GB SSD"
        },
        {
            "id": 2,
            "name": "MacBook Air M2",
            "price": 1199,
            "rating": 4.7,
            "features": "Apple M2, 8GB RAM, 256GB SSD"
        }
    ]
    
    print("\nProduct Comparison:")
    comparison = format_product_comparison(sample_products)
    print(comparison)

def test_alert_system():
    """Test alert system"""
    print("=" * 60)
    print("🔔 Testing Alert System")
    print("=" * 60)
    
    print("\nSample Alert Structure:")
    sample_alert = {
        "product_id": 1,
        "product_name": "Dell XPS 13",
        "current_price": 1299,
        "target_price": 1199,
        "user_email": "user@example.com",
        "created_at": "2024-01-15T10:30:00",
        "triggered": False,
        "triggered_at": None
    }
    
    print(json.dumps(sample_alert, indent=2))
    
    print("\n✅ Alert would trigger when price reaches: ", end="")
    print(f"{format_price(sample_alert['target_price'])}")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Smart Product Recommendation Agent" + " " * 14 + "║")
    print("║" + " " * 15 + "Demo & Test Suite" + " " * 27 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    try:
        test_utils()
        test_product_data()
        test_alert_system()
        
        print("\n" + "=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print("\n🚀 Ready to run the application:")
        print("   python AI.py")
        print("\n💻 Then open: http://localhost:5000\n")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
