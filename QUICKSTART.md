# Smart Product Recommendation Agent - Quick Start Guide 🚀

## 5-Minute Setup

### Step 1: Install Ollama (3 minutes)
```bash
# Download from https://ollama.ai
# Run the installer and follow prompts
# Then pull the model:
ollama pull llama3.2
```

### Step 2: Install Python Dependencies (1 minute)
```bash
cd smartPRODUCT
pip install -r requirements.txt
```

### Step 3: Run the Application (1 minute)
```bash
python AI.py
```

### Step 4: Open in Browser
Go to: **http://localhost:5000**

---

## What to Try First 👇

### Search Examples
1. **Budget Laptop Search**
   - Type: "Find me a laptop under $1000"
   - Expected: 3 laptops within budget, ranked by rating

2. **Smartphone Comparison**
   - Type: "Show me phones under $600"
   - Expected: Best phones in the $600 range

3. **Premium Product**
   - Type: "Best tablet within $500"
   - Expected: Top-rated tablets up to $500

4. **Specific Features**
   - Type: "Headphones with best rating under $300"
   - Expected: Top-rated headphones within budget

### Using the UI

**Quick Buttons** (Bottom of chat):
- Pre-filled search queries for common items
- Click any button to search instantly

**Settings Panel** (⚙️ icon):
- Set what you're looking for
- Enter your budget
- Get personalized results

**Product Cards**:
- **Alert**: Get notified when price drops
- **Select**: Save for later purchase

---

## Understanding the 3 Agents 🤖

### 🔍 Search Agent
Finds products matching your criteria:
- Parses your request
- Searches product database
- Filters by budget
- Returns matching items

### ⚖️ Comparison Agent
Compares found products:
- Analyzes specifications
- Compares prices
- Evaluates ratings
- Recommends best option

### 🔔 Alert Agent
Tracks prices and alerts:
- Monitors price changes
- Sends drop notifications
- Tracks purchase history
- Suggests best buying time

---

## Setting Price Alerts 🔔

1. See a product you like?
2. Click the **"Alert"** button
3. Enter target price (when to notify)
4. Add your email
5. Get notified when price drops!

---

## Troubleshooting Quick Fixes 🔧

### "Connection refused" error
```bash
# Make sure Ollama is running
ollama serve
# In another terminal, run the app
python AI.py
```

### "Port 5000 in use" error
```bash
# Change port in AI.py (line 235):
app.run(debug=True, host='localhost', port=5001)
```

### "Module not found" error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Advanced Features 🚀

### Custom Product Database
1. Edit `search_products_api()` in `AI.py`
2. Add your own products
3. Restart the app

### Real API Integration
1. Edit `config.py`
2. Set `ENABLE_REAL_APIS = True`
3. Add your API keys
4. Integrate Amazon, eBay, etc.

### Email Notifications
1. Set up email in `config.py`
2. Add SMTP credentials
3. Price drops trigger emails

---

## File Overview 📁

| File | Purpose |
|------|---------|
| `AI.py` | Main Flask app + CrewAI agents |
| `requirements.txt` | Python packages needed |
| `config.py` | Configuration settings |
| `utils.py` | Helper functions |
| `templates/index.html` | Web interface |
| `static/style.css` | UI styling |
| `static/script.js` | Frontend logic |

---

## Next Steps 📝

1. **Customize Products** → Add your product catalog
2. **Real APIs** → Connect to Amazon, eBay, etc.
3. **Email Alerts** → Send price drop notifications
4. **User Accounts** → Save preferences & history
5. **Deploy** → Host on Heroku, AWS, or Vercel

---

## Getting Help 💬

### Common Questions

**Q: Can I use a different AI model?**
A: Yes! In `AI.py` line 9, change:
```python
llm = ChatOllama(model="your-model-name")
```

**Q: How do I add real products?**
A: Edit `search_products_api()` function to fetch from APIs

**Q: Can I deploy this online?**
A: Yes! Just deploy to Heroku, AWS, or similar cloud service

**Q: How do I get email notifications?**
A: Set up SMTP in `config.py` and implement email sending

---

## Performance Tips ⚡

- **Faster responses**: Use lighter LLM models
- **Better results**: Fine-tune prompts in agents
- **Scalability**: Use database instead of JSON files

---

**You're ready! Open http://localhost:5000 and start searching! 🎉**
