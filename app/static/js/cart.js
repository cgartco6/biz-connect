class ShoppingCart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('capebiz_cart')) || [];
        this.updateCartDisplay();
    }
    
    addItem(id, type, name, price, duration = null) {
        // Check if item already exists
        const existingIndex = this.items.findIndex(item => item.id === id && item.type === type);
        
        if (existingIndex > -1) {
            this.items[existingIndex].quantity += 1;
        } else {
            this.items.push({
                id,
                type,
                name,
                price,
                quantity: 1,
                duration,
                added: new Date().toISOString()
            });
        }
        
        this.saveCart();
        this.showNotification(`${name} added to cart`);
    }
    
    removeItem(index) {
        if (index > -1 && index < this.items.length) {
            const item = this.items[index];
            this.items.splice(index, 1);
            this.saveCart();
            this.showNotification(`${item.name} removed from cart`);
        }
    }
    
    updateQuantity(index, quantity) {
        if (index > -1 && index < this.items.length && quantity > 0) {
            this.items[index].quantity = quantity;
            this.saveCart();
        }
    }
    
    clearCart() {
        this.items = [];
        this.saveCart();
        this.showNotification('Cart cleared');
    }
    
    saveCart() {
        localStorage.setItem('capebiz_cart', JSON.stringify(this.items));
        this.updateCartDisplay();
        this.dispatchCartUpdateEvent();
    }
    
    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }
    
    getItemCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }
    
    updateCartDisplay() {
        // Update cart count badge
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(el => {
            el.textContent = this.getItemCount();
            el.style.display = this.getItemCount() > 0 ? 'inline-block' : 'none';
        });
        
        // Update cart total if on cart page
        const cartTotalElement = document.getElementById('cart-total');
        if (cartTotalElement) {
            cartTotalElement.textContent = `R${this.getTotal().toFixed(2)}`;
        }
        
        // Update cart items if on cart page
        this.renderCartItems();
    }
    
    renderCartItems() {
        const cartItemsElement = document.getElementById('cart-items');
        if (!cartItemsElement) return;
        
        if (this.items.length === 0) {
            cartItemsElement.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-cart-x fs-1 text-muted d-block mb-3"></i>
                    <p class="text-muted">Your cart is empty</p>
                    <a href="${window.location.origin}" class="btn btn-primary">Browse Businesses</a>
                </div>
            `;
            return;
        }
        
        cartItemsElement.innerHTML = this.items.map((item, index) => `
            <div class="card mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6 class="card-title">${item.name}</h6>
                            <p class="card-text mb-1">R${item.price.toFixed(2)} each</p>
                            ${item.duration ? `<small class="text-muted">Duration: ${item.duration}</small>` : ''}
                        </div>
                        <div class="d-flex align-items-center">
                            <div class="input-group input-group-sm me-3" style="width: 100px;">
                                <button class="btn btn-outline-secondary" type="button" onclick="cart.updateQuantity(${index}, ${item.quantity - 1})">-</button>
                                <input type="number" class="form-control text-center" value="${item.quantity}" min="1" 
                                       onchange="cart.updateQuantity(${index}, parseInt(this.value))">
                                <button class="btn btn-outline-secondary" type="button" onclick="cart.updateQuantity(${index}, ${item.quantity + 1})">+</button>
                            </div>
                            <button class="btn btn-outline-danger btn-sm" onclick="cart.removeItem(${index})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Update total display
        document.getElementById('cart-subtotal').textContent = `R${this.getTotal().toFixed(2)}`;
        document.getElementById('cart-tax').textContent = `R${(this.getTotal() * 0.15).toFixed(2)}`;
        document.getElementById('cart-grand-total').textContent = `R${(this.getTotal() * 1.15).toFixed(2)}`;
    }
    
    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'alert alert-success position-fixed top-0 end-0 m-3';
        notification.style.zIndex = '1050';
        notification.style.minWidth = '300px';
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-check-circle-fill me-2"></i>
                <div>${message}</div>
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    dispatchCartUpdateEvent() {
        window.dispatchEvent(new CustomEvent('cartUpdated', {
            detail: { itemCount: this.getItemCount(), total: this.getTotal() }
        }));
    }
    
    async checkout() {
        try {
            // Validate cart
            if (this.items.length === 0) {
                throw new Error('Cart is empty');
            }
            
            // Create checkout session
            const response = await fetch('/api/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    items: this.items,
                    total: this.getTotal()
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirect to payment gateway
                window.location.href = result.payment_url;
            } else {
                throw new Error(result.message || 'Checkout failed');
            }
        } catch (error) {
            this.showNotification(error.message, 'danger');
            console.error('Checkout error:', error);
        }
    }
}

// Initialize cart
const cart = new ShoppingCart();

// CSRF token helper function
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

// Export for global access
window.cart = cart;
