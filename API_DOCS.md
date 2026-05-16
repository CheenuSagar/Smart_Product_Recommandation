# Smart Product Recommendation API Documentation 📡

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### 1. Chat Endpoint
**Main endpoint for product search and recommendations**

#### Request
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Find me a laptop under $1000",
  "budget": 1000,
  "preferences": "laptop"
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | Natural language request from user |
| `budget` | number | Yes | Maximum budget in USD |
| `preferences` | string | Yes | Product type (laptop, phone, tablet, headphones) |

#### Response (Success)
```json
{
  "status": "success",
  "response": "Found 3 products matching your criteria...",
  "products": [
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
    }
  ]
}
```

#### Response (Error)
```json
{
  "status": "error",
  "response": "An error occurred: [error message]"
}
```

---

### 2. Set Price Alert
**Create a price drop alert for a product**

#### Request
```http
POST /api/set-alert
Content-Type: application/json

{
  "product_id": 1,
  "target_price": 1199,
  "email": "user@example.com"
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | integer | Yes | ID of the product to alert |
| `target_price` | number | Yes | Price at which to trigger alert |
| `email` | string | Yes | Email to receive notifications |

#### Response (Success)
```json
{
  "status": "success",
  "message": "Price alert set! You'll be notified when price drops to $1199"
}
```

#### Response (Error)
```json
{
  "status": "error",
  "message": "Error setting alert: [error message]"
}
```

---

### 3. Track Product Price
**Record current price for historical tracking**

#### Request
```http
POST /api/track-price
Content-Type: application/json

{
  "product_id": 1,
  "product_name": "Dell XPS 13",
  "current_price": 1299
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | integer | Yes | Unique product identifier |
| `product_name` | string | Yes | Name of the product |
| `current_price` | number | Yes | Current price in USD |

#### Response (Success)
```json
{
  "status": "success",
  "message": "Price tracked successfully"
}
```

#### Response (Error)
```json
{
  "status": "error",
  "message": "Error tracking price: [error message]"
}
```

---

### 4. Get Price History
**Retrieve price history for a product**

#### Request
```http
GET /api/get-price-history?product_id=1
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | integer | Yes | ID of product to get history for |

#### Response (Success)
```json
{
  "status": "success",
  "product": {
    "name": "Dell XPS 13",
    "price_history": [
      {
        "price": 1299,
        "timestamp": "2024-01-15T10:30:00"
      },
      {
        "price": 1249,
        "timestamp": "2024-01-16T14:20:00"
      },
      {
        "price": 1199,
        "timestamp": "2024-01-17T09:15:00"
      }
    ]
  }
}
```

#### Response (Error)
```json
{
  "status": "error",
  "message": "Product not found"
}
```

---

## Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Example Usage

### Using cURL
```bash
# Search for products
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me a laptop under $1000",
    "budget": 1000,
    "preferences": "laptop"
  }'

# Set price alert
curl -X POST http://localhost:5000/api/set-alert \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "target_price": 1199,
    "email": "user@example.com"
  }'

# Get price history
curl -X GET "http://localhost:5000/api/get-price-history?product_id=1"
```

### Using Python Requests
```python
import requests

# Search for products
response = requests.post(
    'http://localhost:5000/api/chat',
    json={
        'message': 'Find me a laptop under $1000',
        'budget': 1000,
        'preferences': 'laptop'
    }
)
print(response.json())

# Set price alert
response = requests.post(
    'http://localhost:5000/api/set-alert',
    json={
        'product_id': 1,
        'target_price': 1199,
        'email': 'user@example.com'
    }
)
print(response.json())
```

### Using JavaScript Fetch
```javascript
// Search for products
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Find me a laptop under $1000',
    budget: 1000,
    preferences: 'laptop'
  })
})
.then(r => r.json())
.then(data => console.log(data));

// Set price alert
fetch('/api/set-alert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    product_id: 1,
    target_price: 1199,
    email: 'user@example.com'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Rate Limiting
Currently no rate limiting is implemented. For production:
- Implement 100 requests/minute per IP
- Use Redis or similar for tracking

---

## Authentication
Currently no authentication required. For production:
- Implement JWT tokens
- Use API keys for endpoints
- Secure sensitive operations

---

## CORS
CORS is disabled by default. Enable in production with:
```python
from flask_cors import CORS
CORS(app)
```

---

## Webhook Events
Future feature for real-time price alerts:
```
POST /webhook/price-alert
POST /webhook/order-confirmation
POST /webhook/inventory-update
```

---

## Data Formats

### Product Object
```json
{
  "id": 1,
  "name": "Dell XPS 13",
  "price": 1299,
  "rating": 4.8,
  "features": "Intel i7, 16GB RAM, 512GB SSD",
  "category": "laptop",
  "in_stock": true,
  "reviews_count": 1250
}
```

### Alert Object
```json
{
  "product_id": 1,
  "target_price": 1199,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00",
  "triggered": false,
  "triggered_at": null
}
```

### Price History Entry
```json
{
  "price": 1299,
  "timestamp": "2024-01-15T10:30:00",
  "source": "amazon"
}
```

---

## Error Handling

### Common Errors

**Invalid Budget**
```json
{
  "status": "error",
  "message": "Budget must be a positive number"
}
```

**Invalid Email**
```json
{
  "status": "error",
  "message": "Invalid email format"
}
```

**Product Not Found**
```json
{
  "status": "error",
  "message": "Product with ID 999 not found"
}
```

---

## Best Practices

1. **Always validate input** on client-side before sending
2. **Handle errors gracefully** in your application
3. **Cache responses** when possible to reduce load
4. **Use proper error codes** in responses
5. **Implement rate limiting** for production
6. **Secure sensitive data** like emails and prices
7. **Log all API calls** for debugging
8. **Test endpoints** before deployment

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01-15 | Initial API release |
| 1.1 | 2024-01-20 | Added price history endpoint |
| 1.2 | 2024-02-01 | Enhanced filtering options |

---

## Contact & Support

For API support, documentation updates, or feature requests:
- Create an issue on GitHub
- Email: support@smartproduct.ai
- Discord: [Join Community]

---

**Last Updated: January 2024**
