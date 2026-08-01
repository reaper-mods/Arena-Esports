// ARENA ESPORTS - Main JavaScript File

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
    loadNotifications();
});

// Main app initialization
function initializeApp() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Lazy load images
    lazyLoadImages();
}

// Setup global event listeners
function setupEventListeners() {
    // Search functionality
    const searchInput = document.querySelector('.search-box');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', validateForm);
    });

    // Logout confirmation
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', confirmLogout);
    }

    // Auto-hide alerts
    setTimeout(autoHideAlerts, 5000);
}

// Check if user is authenticated
function checkAuthStatus() {
    const userMenu = document.querySelector('.user-menu');
    if (!userMenu) {
        // Redirect to login if trying to access protected pages
        const protectedPages = ['/profile', '/wallet', '/admin'];
        const currentPath = window.location.pathname;
        
        if (protectedPages.some(page => currentPath.startsWith(page))) {
            window.location.href = '/login';
        }
    }
}

// Load notifications (to be implemented with API)
function loadNotifications() {
    // Placeholder for notification system
    console.log('Loading notifications...');
}

// Search handler
function handleSearch(event) {
    const query = event.target.value.trim();
    if (query.length >= 3) {
        // Make API call for search
        fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => displaySearchResults(data))
            .catch(error => console.error('Search error:', error));
    }
}

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;

    if (results.length === 0) {
        resultsContainer.innerHTML = '<p class="text-center text-muted">No results found</p>';
        return;
    }

    resultsContainer.innerHTML = results.map(result => `
        <div class="search-result-item p-2 border-bottom">
            <a href="${result.url}" class="text-decoration-none">
                ${result.title}
            </a>
        </div>
    `).join('');
}

// Form validation
function validateForm(event) {
    const form = event.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            showFieldError(field, 'This field is required');
        } else {
            removeFieldError(field);
        }
    });

    // Validate email
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        if (!isValidEmail(emailField.value)) {
            isValid = false;
            showFieldError(emailField, 'Please enter a valid email address');
        }
    }

    // Validate phone
    const phoneField = form.querySelector('input[type="tel"]');
    if (phoneField && phoneField.value) {
        if (!isValidPhone(phoneField.value)) {
            isValid = false;
            showFieldError(phoneField, 'Please enter a valid phone number');
        }
    }

    if (!isValid) {
        event.preventDefault();
    }
}

// Show field error
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    let feedbackDiv = field.nextElementSibling;
    if (!feedbackDiv || !feedbackDiv.classList.contains('invalid-feedback')) {
        feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'invalid-feedback';
        field.parentNode.insertBefore(feedbackDiv, field.nextElementSibling);
    }
    
    feedbackDiv.textContent = message;
}

// Remove field error
function removeFieldError(field) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
}

// Email validation
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Phone validation
function isValidPhone(phone) {
    const re = /^\d{10,15}$/;
    return re.test(phone);
}

// Confirm logout
function confirmLogout(event) {
    if (!confirm('Are you sure you want to logout?')) {
        event.preventDefault();
    }
}

// Auto hide alerts
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Debounce function
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

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// API helper functions
const API = {
    get: async (url) => {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },
    
    post: async (url, data) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }
};

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}