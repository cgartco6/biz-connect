class ShoppingCart {
    constructor() {
        this.items = [];
        this.loadCart();
    }
    
    loadCart() {
        const savedCart = localStorage.getItem('capebiz_cart');
        if (savedCart) {
            this.items = JSON.parse(savedCart);
        }
        this.updateCartDisplay();
    }
    
    saveCart() {
        localStorage.setItem('capebiz_cart', JSON.stringify(this.items));
        this.updateCartDisplay();
    }
    
    addItem(productId, productType, name, price) {
        this.items.push({
            id: productId,
            type: productType,
            name: name,
            price: price,
            added: new Date().toISOString()
        });
        this.saveCart();
    }
    
    removeItem(index) {
        this.items.splice(index, 1);
        this.saveCart();
    }
    
    clearCart() {
        this.items = [];
        this.saveCart();
    }
    
    getTotal() {
        return this.items.reduce((total, item) => total + item.price, 0);
    }
    
    updateCartDisplay() {
        const cartCount = document.getElementById('cart-count');
        const cartTotal = document.getElementById('cart-total');
        
        if (cartCount) {
            cartCount.textContent = this.items.length;
        }
        
        if (cartTotal) {
            cartTotal.textContent = 'R' + this.getTotal().toFixed(2);
        }
    }
    
    // Checkout process
    async checkout() {
        try {
            const response = await fetch('/api/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    items: this.items,
                    total: this.getTotal()
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirect to payment page
                window.location.href = result.payment_url;
            } else {
                alert('Checkout failed: ' + result.message);
            }
        } catch (error) {
            console.error('Checkout error:', error);
            alert('An error occurred during checkout.');
        }
    }
}

// Initialize cart
const cart = new ShoppingCart();

// Add event listeners for boost buttons
document.querySelectorAll('.boost-btn').forEach(button => {
    button.addEventListener('click', () => {
        const businessId = button.dataset.businessId;
        const businessName = button.dataset.businessName;
        cart.addItem(businessId, 'boost', `Boost for ${businessName}`, 99);
        alert('Boost added to cart!');
    });
});

// Add event listeners for subscription buttons
document.querySelectorAll('.subscription-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tier = button.dataset.tier;
        const price = parseInt(button.dataset.price);
        cart.addItem(tier, 'subscription', `${tier} Subscription`, price);
        alert('Subscription added to cart!');
    });
});
