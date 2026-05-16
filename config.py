# Configuration file for Smart Product Recommendation Agent

# Flask Configuration
FLASK_DEBUG = True
FLASK_HOST = 'localhost'
FLASK_PORT = 5000

# Ollama Configuration
OLLAMA_MODEL = 'llama3.2'
OLLAMA_HOST = 'http://localhost:11434'

# Application Settings
MAX_PRODUCTS_PER_SEARCH = 10
DEFAULT_BUDGET = 1000
CURRENCY = 'USD'

# Database Settings
PRODUCTS_DB_FILE = 'products_db.json'
ALERTS_DB_FILE = 'alerts_db.json'

# API Settings
ENABLE_REAL_APIS = False  # Set to True to enable real product APIs
AMAZON_API_KEY = 'your-api-key'
EBAY_API_KEY = 'your-api-key'
PRICE_API_KEY = 'your-api-key'

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'app.log'

# Email Notifications (for price alerts)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'

# Product Categories
PRODUCT_CATEGORIES = [
    'laptop',
    'phone',
    'tablet',
    'headphones',
    'smartwatch',
    'camera',
    'monitor'
]

# Feature Keywords
KEY_FEATURES = {
    'laptop': ['processor', 'RAM', 'storage', 'display', 'battery'],
    'phone': ['processor', 'RAM', 'storage', 'camera', 'battery'],
    'tablet': ['processor', 'RAM', 'storage', 'display', 'battery'],
    'headphones': ['noise_cancellation', 'battery', 'connectivity', 'sound_quality']
}
