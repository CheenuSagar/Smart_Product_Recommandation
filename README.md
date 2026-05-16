# Smart Product Recommendation Agent 🤖

A ChatGPT-like web interface for intelligent product recommendations with multi-agent architecture using CrewAI.

## Features ✨

### Core Functionality
- **🔍 Search Agent**: Searches products from multiple APIs based on user preferences
- **⚖️ Comparison Agent**: Compares products by price, ratings, and features
- **🔔 Alert Agent**: Tracks price changes and alerts users when prices drop
- **💰 Budget-Aware Recommendations**: Filters products within user's budget
- **⭐ Rating & Feature Analysis**: Comprehensive product comparison
- **📊 Price Tracking**: Historical price monitoring for smart purchasing

### User Interface
- **ChatGPT-like Interface**: Modern, intuitive web design
- **Real-time Chat**: Interactive conversation with AI agents
- **Quick Prompts**: Predefined search templates for quick access
- **Product Cards**: Visual display of recommended products
- **Price Alerts**: Set custom price drop notifications
- **Responsive Design**: Works on desktop and mobile devices

## Architecture 🏗️

```
Smart Product Recommendation System
├── Backend (Flask + CrewAI)
│   ├── 3 Agent Crew
│   │   ├── Search Agent
│   │   ├── Comparison Agent
│   │   └── Alert Agent
│   └── APIs
│       ├── /api/chat (Main chat endpoint)
│       ├── /api/set-alert (Price alert management)
│       ├── /api/track-price (Price tracking)
│       └── /api/get-price-history (Historical data)
├── Frontend (HTML + CSS + JavaScript)
│   ├── Sidebar Navigation
│   ├── Chat Interface
│   ├── Product Display
│   └── Settings Panel
└── Data Storage
    ├── products_db.json
    └── alerts_db.json
```

## Installation 📦

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Ollama with llama3.2 model installed

### Step 1: Install Ollama
1. Download from: https://ollama.ai
2. Install and start the Ollama service
3. Pull the model: `ollama pull llama3.2`

### Step 2: Clone and Setup Project
```bash
cd smartPRODUCT
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python AI.py
```

The application will start at: `http://localhost:5000`

## Usage 🚀

### Basic Search
1. Open http://localhost:5000 in your browser
2. Type your search query, e.g., "Find me a laptop under $1000"
3. The agents will search, compare, and recommend products
4. Click "Alert" on any product to set a price drop notification

### Using Quick Prompts
Click any of the quick prompt buttons:
- 💻 Find me a laptop under $1000
- 📱 Show me phones under $600
- 📊 Best tablet within $500 budget
- 🎧 Headphones with best rating under $300

### Setting Preferences
1. Click the settings button (⚙️) in the input area
2. Enter what you're looking for
3. Set your budget limit
4. Click "Search"

### Price Alerts
1. Click "Alert" on any product card
2. Enter your target price
3. Provide your email
4. You'll receive notifications when the price drops

## API Endpoints 📡

### POST /api/chat
Search and compare products
```json
{
  "message": "Find me a laptop under $1000",
  "budget": 1000,
  "preferences": "laptop"
}
```

### POST /api/set-alert
Set price drop alerts
```json
{
  "product_id": 1,
  "target_price": 1200,
  "email": "user@example.com"
}
```

### POST /api/track-price
Track product price
```json
{
  "product_id": 1,
  "product_name": "Dell XPS 13",
  "current_price": 1299
}
```

### GET /api/get-price-history
Get price history for a product
```
?product_id=1
```

## Agent Roles Explained 🤝

### Search Agent 🔍
- **Role**: Product Search Specialist
- **Goal**: Find relevant products based on user preferences
- **Actions**:
  - Parse user requirements
  - Search product databases/APIs
  - Filter by category and budget
  - Return matching products

### Comparison Agent ⚖️
- **Role**: Product Comparison Expert
- **Goal**: Recommend best product based on value
- **Actions**:
  - Analyze product specifications
  - Compare prices and ratings
  - Calculate value-for-money
  - Provide detailed comparison

### Alert Agent 🔔
- **Role**: Price Monitoring Specialist
- **Goal**: Help users get the best deals
- **Actions**:
  - Monitor price changes
  - Track price history
  - Send drop alerts
  - Suggest optimal purchase times

## Product Database 📊

Currently supports these categories:
- 💻 Laptops (Dell, MacBook, ASUS)
- 📱 Phones (iPhone, Samsung, Google Pixel)
- 📊 Tablets (iPad, Samsung Galaxy Tab, Amazon Fire)
- 🎧 Headphones (Sony, Apple, Anker)

**Note**: In production, integrate with real APIs like:
- Amazon Product API
- eBay API
- Shopify API
- PriceAPI

## Customization 🎨

### Change LLM Model
Edit `AI.py` line 9:
```python
llm = ChatOllama(model="your-model-name")
```

### Add New Product Categories
Edit the `search_products_api()` function in `AI.py` to add more products.

### Customize UI Colors
Edit `static/style.css` CSS variables at the top:
```css
:root {
    --primary-color: #10a37f;
    --bg-primary: #ffffff;
    /* ... more colors ... */
}
```

## Troubleshooting 🔧

### Ollama Not Found
```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull llama3.2
```

### Port 5000 Already in Use
Change the port in `AI.py` line 235:
```python
app.run(debug=True, host='localhost', port=5001)
```

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## Future Enhancements 🚀

- [ ] Integration with real product APIs (Amazon, eBay, etc.)
- [ ] User authentication and saved preferences
- [ ] Email notifications for price drops
- [ ] Product review analysis
- [ ] Wishlist functionality
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Historical price charts
- [ ] Competitor price tracking
- [ ] Mobile app version

## Project Structure 📁

```
smartPRODUCT/
├── AI.py                  # Main Flask app + CrewAI agents
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── products_db.json      # Product price history
├── alerts_db.json        # User price alerts
├── templates/
│   └── index.html        # Web interface
└── static/
    ├── style.css         # UI styling
    └── script.js         # Frontend logic
```

## Technologies Used 🛠️

- **Backend**: Flask (Python web framework)
- **AI**: CrewAI (Multi-agent framework)
- **LLM**: Ollama with Llama 3.2
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data**: JSON (local storage)

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues, questions, or suggestions, please create an issue in the repository.

---

**Made with ❤️ for smart product recommendations**
