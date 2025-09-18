// Main JavaScript for CapeBiz Connect

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Search functionality
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
    
    // Category filter
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }
    
    // Town filter
    const townFilter = document.getElementById('town-filter');
    if (townFilter) {
        townFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }
    
    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img.lazy');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Business view tracking
    const businessPage = document.querySelector('.business-page');
    if (businessPage) {
        const businessId = businessPage.dataset.businessId;
        
        // Track view after a short delay to ensure page is loaded
        setTimeout(() => {
            fetch(`/api/business/${businessId}/view`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            }).catch(() => {}); // Silently fail if tracking doesn't work
        }, 1000);
    }
    
    // Boost button functionality
    const boostButtons = document.querySelectorAll('.boost-btn');
    boostButtons.forEach(button => {
        button.addEventListener('click', function() {
            const businessId = this.dataset.businessId;
            const businessName = this.dataset.businessName;
            
            // Add to cart
            cart.addItem(businessId, 'boost', `Boost for ${businessName}`, 99, '7 days');
        });
    });
    
    // Subscription button functionality
    const subscriptionButtons = document.querySelectorAll('.subscription-btn');
    subscriptionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const planId = this.dataset.planId;
            const planName = this.dataset.planName;
            const planPrice = parseFloat(this.dataset.planPrice);
            const businessId = this.dataset.businessId;
            
            if (businessId) {
                cart.addItem(planId, 'subscription', `${planName} Subscription`, planPrice, '30 days');
            } else {
                // Prompt user to select a business first
                alert('Please select a business first or add a new business.');
            }
        });
    });
});

// Helper function to get CSRF token
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

// AJAX helper function
function makeRequest(url, options = {}) {
    const defaults = {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        }
    };
    
    const config = { ...defaults, ...options };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export for global access
window.CapeBiz = {
    makeRequest,
    debounce
};
