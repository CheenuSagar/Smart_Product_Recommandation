let conversationHistory = [];
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textarea
    const textarea = document.getElementById('messageInput');
    textarea.addEventListener('input', autoResizeTextarea);
});

function autoResizeTextarea() {
    const textarea = document.getElementById('messageInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendPrompt(prompt) {
    document.getElementById('messageInput').value = prompt;
    sendMessage();
}

function togglePreferences() {
    const panel = document.getElementById('preferencesPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function searchWithPreferences() {
    const preferences = document.getElementById('preferences').value;
    const budget = document.getElementById('budget').value;
    
    if (!preferences) {
        alert('Please enter what you are looking for');
        return;
    }
    
    const message = `Find me a ${preferences} with budget of $${budget}`;
    document.getElementById('messageInput').value = message;
    sendMessage();
    togglePreferences();
}

function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message || isLoading) return;
    
    // Remove welcome message if exists
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    autoResizeTextarea();
    
    // Parse budget from message (handle $1000, 1000, under 1000, etc.)
    let budget = 1000;
    const dollarMatch = message.match(/\$(\d+)/);
    const underMatch = message.match(/under\s+(\d+)/i);
    const withinMatch = message.match(/within\s+(\d+)/i);
    const numberMatch = message.match(/(\d{4,})/); // Match 4+ digit numbers
    
    if (dollarMatch) {
        budget = parseInt(dollarMatch[1]);
    } else if (underMatch) {
        budget = parseInt(underMatch[1]);
    } else if (withinMatch) {
        budget = parseInt(withinMatch[1]);
    } else if (numberMatch) {
        budget = parseInt(numberMatch[1]);
    }
    
    // Extract preferences - look for product types first
    const productTypes = ['laptop', 'phone', 'tablet', 'headphone', 'smartwatch', 'camera', 'monitor'];
    let preferences = '';
    for (let type of productTypes) {
        if (message.toLowerCase().includes(type)) {
            preferences = type;
            break;
        }
    }
    
    // If no product type found, extract remaining text
    if (!preferences) {
        preferences = message.toLowerCase()
            .replace(/\d+/g, '')
            .replace(/budget|under|within|find|me|a|an|the|to|buy|want|i|am|you|gamin|gaming|sorry|no|products|\$|dollars?|rupees?|price|cost|inr|usd/gi, '')
            .trim();
    }
    
    // Send to backend with parsed data
    sendChatRequest(message, budget, preferences);
}

async function sendChatRequest(message, budget, preferences) {
    isLoading = true;
    
    // Show loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="loading-spinner">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
    `;
    document.getElementById('messagesArea').appendChild(loadingDiv);
    document.getElementById('messagesArea').scrollTop = document.getElementById('messagesArea').scrollHeight;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                budget: budget,
                preferences: preferences
            })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        loadingDiv.remove();
        
        if (data.status === 'success') {
            // Add AI response
            addMessage(data.response, 'ai');
            
            // Add products if available
            if (data.products && data.products.length > 0) {
                addProducts(data.products);
            }
        } else {
            addMessage(data.response || 'An error occurred', 'ai');
        }
        
    } catch (error) {
        loadingDiv.remove();
        addMessage(`Error: ${error.message}`, 'ai');
    } finally {
        isLoading = false;
        document.getElementById('messagesArea').scrollTop = document.getElementById('messagesArea').scrollHeight;
    }
}

function addMessage(content, role) {
    const messagesArea = document.getElementById('messagesArea');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    messagesArea.appendChild(messageDiv);
    
    // Store in history
    conversationHistory.push({
        role: role,
        content: content,
        timestamp: new Date()
    });
    
    // Scroll to bottom
    setTimeout(() => {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 100);
}

function addProducts(products) {
    const messagesArea = document.getElementById('messagesArea');
    
    const productsDiv = document.createElement('div');
    productsDiv.className = 'message ai';
    
    let productsHTML = '<div class="message-content"><div class="products-grid">';
    
    products.forEach(product => {
        productsHTML += `
            <div class="product-card">
                <h4>${product.name}</h4>
                <div class="product-info">ID: ${product.id}</div>
                <div class="product-price">$${product.price}</div>
                <div class="product-rating">
                    <i class="fas fa-star"></i> ${product.rating}/5.0
                </div>
                <div class="product-info">${product.features}</div>
                <div class="product-actions">
                    <button onclick="setAlert(${product.id}, '${product.name}', ${product.price})">
                        <i class="fas fa-bell"></i> Alert
                    </button>
                    <button class="primary" onclick="selectProduct(${product.id}, '${product.name}')">
                        Select
                    </button>
                </div>
            </div>
        `;
    });
    
    productsHTML += '</div></div>';
    productsDiv.innerHTML = productsHTML;
    messagesArea.appendChild(productsDiv);
    
    // Scroll to bottom
    setTimeout(() => {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 100);
}

function setAlert(productId, productName, currentPrice) {
    const targetPrice = prompt(`Set alert for ${productName}\n\nCurrent Price: $${currentPrice}\n\nEnter target price:`, Math.floor(currentPrice * 0.9));
    
    if (targetPrice === null) return;
    
    const email = prompt('Enter your email for alerts:', '');
    
    if (!email) {
        alert('Email is required for price alerts');
        return;
    }
    
    // Save alert
    fetch('/api/set-alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            target_price: parseFloat(targetPrice),
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            addMessage(`✅ ${data.message}`, 'ai');
        } else {
            addMessage(`❌ ${data.message}`, 'ai');
        }
    })
    .catch(error => {
        addMessage(`Error: ${error.message}`, 'ai');
    });
}

function selectProduct(productId, productName) {
    // Track price
    fetch('/api/track-price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            product_name: productName,
            current_price: 0 // Would be actual price in production
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            addMessage(`✅ You selected ${productName}. I'll track price changes for you!`, 'ai');
        }
    });
}

function newChat() {
    conversationHistory = [];
    document.getElementById('messagesArea').innerHTML = `
        <div class="welcome-message">
            <div class="welcome-content">
                <h2>Welcome to Smart Product Advisor</h2>
                <p>I help you find the best products based on your budget and preferences</p>
                
                <div class="agent-roles">
                    <div class="role-card">
                        <i class="fas fa-magnifying-glass"></i>
                        <h3>Search Agent</h3>
                        <p>Searches products from multiple APIs</p>
                    </div>
                    <div class="role-card">
                        <i class="fas fa-balance-scale"></i>
                        <h3>Comparison Agent</h3>
                        <p>Compares price, ratings & features</p>
                    </div>
                    <div class="role-card">
                        <i class="fas fa-bell"></i>
                        <h3>Alert Agent</h3>
                        <p>Tracks prices & alerts on drops</p>
                    </div>
                </div>

                <div class="quick-prompts">
                    <h3>Try asking:</h3>
                    <button class="prompt-btn" onclick="sendPrompt('Find me a laptop under $1000')">
                        <i class="fas fa-laptop"></i>
                        Find me a laptop under $1000
                    </button>
                    <button class="prompt-btn" onclick="sendPrompt('Show me phones under $600')">
                        <i class="fas fa-mobile"></i>
                        Show me phones under $600
                    </button>
                    <button class="prompt-btn" onclick="sendPrompt('Best tablet within $500 budget')">
                        <i class="fas fa-tablet"></i>
                        Best tablet within $500 budget
                    </button>
                    <button class="prompt-btn" onclick="sendPrompt('Headphones with best rating under $300')">
                        <i class="fas fa-headphones"></i>
                        Headphones with best rating under $300
                    </button>
                </div>
            </div>
        </div>
    `;
    document.getElementById('preferencesPanel').style.display = 'none';
}

function loadChat(chatId) {
    // Load previous chat if needed
    newChat();
}

function closeProductModal() {
    document.getElementById('productModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
