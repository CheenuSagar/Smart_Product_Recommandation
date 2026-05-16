# Project File Structure Guide 📁

## Complete Directory Layout

```
smartPRODUCT/
│
├── AI.py                          # 🎯 Main application (Flask + CrewAI)
├── config.py                      # ⚙️  Configuration settings
├── utils.py                       # 🔧 Helper functions & utilities
├── requirements.txt               # 📦 Python dependencies
│
├── README.md                      # 📖 Main documentation
├── QUICKSTART.md                  # 🚀 5-minute quick start guide
├── API_DOCS.md                    # 📡 Complete API reference
├── PROJECT_STRUCTURE.md           # 📁 This file
│
├── .env.example                   # 📋 Environment template
│
├── templates/                     # 🎨 HTML templates
│   └── index.html                 # Main web interface
│
├── static/                        # 📦 Static assets
│   ├── style.css                  # UI styling (ChatGPT-like)
│   └── script.js                  # Frontend JavaScript logic
│
├── products_db.json               # 💾 Product price history (auto-created)
└── alerts_db.json                 # 🔔 Price alert storage (auto-created)
```

---

## File Descriptions

### Core Application Files

#### `AI.py` (Main Application)
**Purpose**: Flask web server + CrewAI agent framework
**Key Components**:
- Flask app setup and routing
- 3 CrewAI Agents (Search, Comparison, Alert)
- 4 API endpoints
- Product search and comparison logic
- Database management (JSON-based)

**Size**: ~400 lines
**Language**: Python
**Dependencies**: Flask, crewai, langchain, ollama

---

#### `config.py` (Configuration)
**Purpose**: Centralized configuration management
**Contains**:
- Flask settings (host, port, debug mode)
- Ollama LLM configuration
- Database file paths
- Product categories
- Email settings
- API keys (template)
- Feature flags

**Size**: ~60 lines
**Language**: Python

---

#### `utils.py` (Utilities)
**Purpose**: Reusable helper functions
**Functions**:
- `load_json_db()` - Load JSON databases
- `save_json_db()` - Save to JSON
- `parse_budget_from_message()` - Extract budget from text
- `format_price()` - Format currency display
- `calculate_value_score()` - Compute product value
- `check_price_alerts()` - Check if alerts triggered
- `validate_email()` - Email validation

**Size**: ~280 lines
**Language**: Python

---

### Frontend Files

#### `templates/index.html` (Main Interface)
**Purpose**: Web user interface (ChatGPT-like)
**Components**:
- Sidebar with logo and navigation
- Chat message area
- Input field with preferences panel
- Product display cards
- Modal for product details
- Welcome message with quick prompts

**Size**: ~220 lines
**Language**: HTML5
**Features**:
- Responsive design
- Modal support
- Real-time chat
- Product cards with actions

---

#### `static/style.css` (UI Styling)
**Purpose**: Complete CSS styling for ChatGPT-like interface
**Features**:
- Dark/light mode support via CSS variables
- Responsive grid layouts
- Smooth animations and transitions
- Custom scrollbar styling
- Mobile-friendly design
- Accessibility support

**Size**: ~850 lines
**Language**: CSS3
**Key Styles**:
- Sidebar navigation
- Message bubbles (user vs AI)
- Product cards grid
- Input area with buttons
- Loading spinner animation
- Modal dialogs

---

#### `static/script.js` (Frontend Logic)
**Purpose**: Client-side JavaScript for interactivity
**Functions**:
- `sendMessage()` - Send chat messages
- `sendChatRequest()` - API communication
- `addMessage()` - Render messages
- `addProducts()` - Display product cards
- `setAlert()` - Price alert setup
- `selectProduct()` - Save product selection
- `newChat()` - Start fresh conversation
- `togglePreferences()` - Show/hide settings

**Size**: ~380 lines
**Language**: JavaScript (Vanilla, no frameworks)

---

### Documentation Files

#### `README.md` (Main Documentation)
**Purpose**: Complete project overview
**Sections**:
- Features overview
- Architecture diagram
- Installation steps
- Usage instructions
- API endpoints summary
- Agent roles explanation
- Customization guide
- Troubleshooting
- Future enhancements

**Size**: ~350 lines
**Format**: Markdown

---

#### `QUICKSTART.md` (Quick Start Guide)
**Purpose**: Get started in 5 minutes
**Sections**:
- 4-step installation
- Example searches to try
- UI walkthrough
- Agent explanations
- Alert setup instructions
- Common troubleshooting
- Advanced features preview

**Size**: ~200 lines
**Format**: Markdown

---

#### `API_DOCS.md` (API Reference)
**Purpose**: Complete API documentation
**Sections**:
- Base URL and endpoints
- POST /api/chat (main search)
- POST /api/set-alert (price alerts)
- POST /api/track-price (price tracking)
- GET /api/get-price-history (historical data)
- Response codes and examples
- cURL, Python, JavaScript examples
- Data format specifications
- Error handling guide

**Size**: ~450 lines
**Format**: Markdown

---

### Configuration Files

#### `requirements.txt` (Dependencies)
**Purpose**: Python package dependencies
**Packages**:
- Flask (web framework)
- crewai (multi-agent framework)
- langchain (LLM framework)
- langchain-community (additional tools)
- ollama (LLM interface)
- requests (HTTP library)
- python-dotenv (environment variables)

**Format**: pip requirements

---

#### `.env.example` (Environment Template)
**Purpose**: Template for environment variables
**Variables**:
- Flask configuration
- Ollama settings
- Database paths
- API keys (template)
- Email configuration
- Feature flags

**Usage**: Copy to `.env` and fill in your values

---

### Auto-Generated Database Files

#### `products_db.json`
**Purpose**: Store product price history
**Format**:
```json
{
  "1": {
    "name": "Dell XPS 13",
    "price_history": [
      {"price": 1299, "timestamp": "..."},
      {"price": 1249, "timestamp": "..."}
    ]
  }
}
```
**Created**: Automatically on first price tracking
**Updated**: When new prices are tracked

---

#### `alerts_db.json`
**Purpose**: Store user price alerts
**Format**:
```json
{
  "alert_1_timestamp": {
    "product_id": 1,
    "target_price": 1199,
    "email": "user@example.com",
    "created_at": "...",
    "triggered": false
  }
}
```
**Created**: When user sets alert
**Updated**: When alert is triggered

---

## File Dependencies

```
index.html
├── style.css
└── script.js
    └── /api/chat (AI.py)
    └── /api/set-alert (AI.py)
    └── /api/track-price (AI.py)

AI.py
├── config.py
├── utils.py
├── CrewAI framework
│   ├── langchain
│   └── ollama
├── products_db.json
└── alerts_db.json
```

---

## Modification Guide

### Add New Feature
1. Update `AI.py` with new endpoint
2. Add UI in `index.html`
3. Add styling in `style.css`
4. Add JavaScript in `script.js`
5. Update `API_DOCS.md`

### Change Colors/Theme
1. Edit CSS variables in `style.css` (top of file)
2. No need to change other files

### Add Product Categories
1. Edit `search_products_api()` in `AI.py`
2. Add to `PRODUCT_CATEGORIES` in `config.py`
3. Update `KEY_FEATURES` in `config.py`

### Integrate Real APIs
1. Create new function in `AI.py`
2. Add API credentials in `.env`
3. Update `search_products_api()` to use real APIs
4. Set `ENABLE_REAL_APIS = True` in `config.py`

### Add Email Notifications
1. Configure SMTP in `.env`
2. Add email sending function in `utils.py`
3. Call from alert trigger in `AI.py`
4. Set `ENABLE_EMAIL_ALERTS = True`

---

## Performance Considerations

| File | Load Impact | Optimization |
|------|------------|--------------|
| AI.py | Initial startup | Use lightweight LLM model |
| style.css | 50KB | Minify for production |
| script.js | 15KB | Compress and cache |
| index.html | 10KB | Use CDN for fonts |

---

## Security Considerations

- ✅ No API keys in source code (use .env)
- ✅ Email validation before sending alerts
- ✅ Input sanitization in form fields
- ⚠️ Add CORS for production
- ⚠️ Implement authentication for user accounts
- ⚠️ Use HTTPS in production
- ⚠️ Add rate limiting to APIs

---

## Deployment Checklist

Before deploying to production:
- [ ] Set `FLASK_DEBUG = False`
- [ ] Use production database (not JSON)
- [ ] Add proper logging
- [ ] Implement authentication
- [ ] Enable HTTPS
- [ ] Set up email notifications
- [ ] Add monitoring/alerting
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Minify CSS/JavaScript
- [ ] Add API rate limiting

---

## Total Project Size

| Component | Size | Type |
|-----------|------|------|
| Backend (AI.py) | 400 lines | Python |
| Config (config.py) | 60 lines | Python |
| Utils (utils.py) | 280 lines | Python |
| Frontend (index.html) | 220 lines | HTML |
| Styling (style.css) | 850 lines | CSS |
| Logic (script.js) | 380 lines | JavaScript |
| Documentation | ~1200 lines | Markdown |
| **Total** | **~3500 lines** | Mixed |

---

## Next Steps

1. **Get Started**: Run `python AI.py` and open localhost:5000
2. **Explore**: Try the quick search examples
3. **Customize**: Modify colors, add products
4. **Integrate**: Add real product APIs
5. **Deploy**: Host on cloud platform

---

**Project Created**: January 2024
**Last Updated**: January 2024
**Status**: Ready for Development ✅
