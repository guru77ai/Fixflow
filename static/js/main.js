/**
 * FixSoftRepair Pro - Main JavaScript File
 */

// ===== Document Ready =====
document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initTheme();
    initLanguage();
    initNotifications();
    initDataTables();
    initCharts();
    initHTMX();
    initKeyboardShortcuts();
    initFormEnhancements();
});

// ===== Sidebar =====
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.querySelector('.main-wrapper');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const menuToggle = document.querySelector('.menu-toggle');
    
    // Toggle sidebar
    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
        if (mainWrapper) {
            mainWrapper.classList.toggle('sidebar-open');
        }
    }
    
    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleSidebar);
    }
    
    // HTMX event for sidebar toggle
    document.addEventListener('toggle-sidebar', toggleSidebar);
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 992) {
            if (sidebar && !sidebar.contains(e.target) && 
                !e.target.closest('.menu-toggle') && 
                !e.target.closest('.sidebar-toggle')) {
                sidebar.classList.remove('open');
                if (mainWrapper) {
                    mainWrapper.classList.remove('sidebar-open');
                }
            }
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            if (sidebar) {
                sidebar.classList.add('open');
            }
            if (mainWrapper) {
                mainWrapper.classList.add('sidebar-open');
            }
        }
    });
}

// ===== Theme =====
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'system';
    applyTheme(savedTheme);
    
    // Theme toggle button
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            let newTheme;
            
            if (currentTheme === 'dark') {
                newTheme = 'light';
            } else if (currentTheme === 'light') {
                newTheme = 'system';
            } else {
                newTheme = 'dark';
            }
            
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
            updateThemeIcon(newTheme);
        });
    }
    
    // Watch for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        const theme = localStorage.getItem('theme') || 'system';
        if (theme === 'system') {
            applyTheme('system');
        }
    });
    
    // Update theme icon
    function updateThemeIcon(theme) {
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 
                               theme === 'light' ? 'bi bi-moon-fill' : 
                               'bi bi-circle-half';
            }
        }
    }
}

function applyTheme(theme) {
    const html = document.documentElement;
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (theme === 'system') {
        html.setAttribute('data-bs-theme', systemDark ? 'dark' : 'light');
    } else {
        html.setAttribute('data-bs-theme', theme);
    }
    
    // Dispatch theme change event
    document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
}

// ===== Language =====
function initLanguage() {
    // Language switcher functionality is handled by Django
    // This just ensures the UI is updated
}

// ===== Notifications =====
function initNotifications() {
    const notificationBadge = document.querySelector('.notifications .badge');
    const notificationItems = document.querySelectorAll('.notification-item.unread');
    
    // Update badge count
    if (notificationBadge) {
        const count = notificationItems.length;
        notificationBadge.textContent = count > 0 ? count : '';
    }
    
    // Mark as read when clicked
    notificationItems.forEach(item => {
        item.addEventListener('click', function() {
            const notificationId = this.dataset.notificationId;
            if (notificationId) {
                markNotificationAsRead(notificationId);
            }
        });
    });
}

function markNotificationAsRead(notificationId) {
    // Send AJAX request to mark notification as read
    fetch(`/api/v1/notifications/${notificationId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`.notification-item[data-notification-id="${notificationId}"]`);
            if (item) {
                item.classList.remove('unread');
            }
            updateNotificationCount();
        }
    })
    .catch(error => {
        console.error('Error marking notification as read:', error);
    });
}

function updateNotificationCount() {
    const unreadItems = document.querySelectorAll('.notification-item.unread');
    const badge = document.querySelector('.notifications .badge');
    
    if (badge) {
        const count = unreadItems.length;
        badge.textContent = count > 0 ? count : '';
        badge.style.display = count > 0 ? 'block' : 'none';
    }
}

// ===== DataTables =====
function initDataTables() {
    // Initialize all DataTables
    const tables = document.querySelectorAll('table.dataTable:not(.initialized)');
    
    tables.forEach(table => {
        table.classList.add('initialized');
        
        const config = {
            responsive: true,
            processing: true,
            serverSide: false,
            pageLength: 20,
            lengthMenu: [10, 20, 50, 100],
            order: [[0, 'desc']],
            language: {
                url: getDataTablesLanguageUrl()
            },
            dom: '<"row"<"col-md-6"l><"col-md-6"f>>rt<"row"<"col-md-6"i><"col-md-6"p>>'
        };
        
        // Check for custom configuration
        const customConfig = table.dataset.datatablesConfig;
        if (customConfig) {
            try {
                Object.assign(config, JSON.parse(customConfig));
            } catch (e) {
                console.error('Error parsing DataTables config:', e);
            }
        }
        
        // Initialize
        $(table).DataTable(config);
    });
}

function getDataTablesLanguageUrl() {
    const lang = document.documentElement.lang || 'fr';
    const urls = {
        'fr': 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/fr.json',
        'ar': 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ar.json',
        'en': 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/en-GB.json'
    };
    return urls[lang] || urls['fr'];
}

// ===== Charts =====
function initCharts() {
    // Initialize all chart containers
    const chartContainers = document.querySelectorAll('.chart-container:not(.initialized)');
    
    chartContainers.forEach(container => {
        container.classList.add('initialized');
        
        const canvas = container.querySelector('canvas');
        if (!canvas) return;
        
        const config = JSON.parse(canvas.dataset.chartConfig || '{}');
        const ctx = canvas.getContext('2d');
        
        // Apply RTL support for Arabic
        if (document.documentElement.dir === 'rtl') {
            config.options = config.options || {};
            config.options.plugins = config.options.plugins || {};
            config.options.plugins.legend = config.options.plugins.legend || {};
            config.options.plugins.legend.rtl = true;
        }
        
        new Chart(ctx, config);
    });
}

// ===== HTMX =====
function initHTMX() {
    // HTMX is loaded via CDN, but we can add custom configurations
    if (typeof htmx !== 'undefined') {
        // Configure HTMX
        htmx.config.defaults = {
            ...htmx.config.defaults,
            // Add custom settings
        };
        
        // Add loading indicators
        htmx.onLoad(function(content) {
            // Add loading class to forms
            const forms = content.querySelectorAll('form[hx-post], form[hx-put], form[hx-patch], form[hx-delete]');
            forms.forEach(form => {
                form.addEventListener('htmx:request', function() {
                    form.classList.add('loading');
                });
                form.addEventListener('htmx:afterRequest', function() {
                    form.classList.remove('loading');
                });
            });
        });
        
        // Show loading indicator
        document.body.addEventListener('htmx:request', function() {
            showLoading();
        });
        
        // Hide loading indicator
        document.body.addEventListener('htmx:afterRequest', function() {
            hideLoading();
        });
    }
}

function showLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
}

function hideLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
}

// ===== Keyboard Shortcuts =====
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for global search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-box input');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals and dropdowns
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const closeBtn = openModal.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }
            
            const openDropdown = document.querySelector('.dropdown-menu.show');
            if (openDropdown) {
                // Close all dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
            }
        }
    });
}

// ===== Form Enhancements =====
function initFormEnhancements() {
    // Auto-focus first input on modal open
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = modal.querySelector('input:not([type="hidden"]), select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
    
    // Clear form on modal close
    modals.forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function() {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
        });
    });
    
    // Form validation feedback
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('needs-validation')) {
            e.target.addEventListener('submit', function(event) {
                if (!this.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                this.classList.add('was-validated');
            }, { once: true });
        }
    });
    
    // File input styling
    document.querySelectorAll('.custom-file-input').forEach(input => {
        input.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                if (this.files && this.files.length > 0) {
                    label.textContent = this.files[0].name;
                } else {
                    label.textContent = label.dataset.defaultText || 'Choose file';
                }
            }
        });
    });
}

// ===== Utility Functions =====
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

function showToast(message, type = 'info', title = '') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${title ? `<strong>${title}</strong><br>` : ''}
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1100';
    document.body.appendChild(container);
    return container;
}

function formatNumber(number, decimals = 2) {
    return number.toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function formatCurrency(amount, currency = 'DZD') {
    return new Intl.NumberFormat(undefined, {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

function formatDateTime(date) {
    return new Intl.DateTimeFormat(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// ===== Confirmation Dialogs =====
function confirmAction(message, callback) {
    const confirmModal = document.getElementById('confirm-modal');
    if (confirmModal) {
        const messageEl = confirmModal.querySelector('.modal-body');
        if (messageEl) {
            messageEl.textContent = message;
        }
        
        const confirmBtn = confirmModal.querySelector('.btn-primary');
        if (confirmBtn) {
            confirmBtn.onclick = function() {
                callback(true);
                const modal = bootstrap.Modal.getInstance(confirmModal);
                modal.hide();
            };
        }
        
        const modal = new bootstrap.Modal(confirmModal);
        modal.show();
    } else {
        // Fallback to browser confirm
        if (confirm(message)) {
            callback(true);
        }
    }
}

// ===== Export Functions =====
function exportToPDF(url, filename) {
    window.open(url, '_blank');
}

function exportToExcel(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ===== Print Functions =====
function printDocument(url) {
    const printWindow = window.open(url, '_blank');
    printWindow.onload = function() {
        printWindow.print();
    };
}

// ===== Barcode Scanner =====
function initBarcodeScanner() {
    // Check if browser supports barcode scanning
    if ('BarcodeDetector' in window) {
        const barcodeInput = document.querySelector('input[autocomplete="barcode"]');
        if (barcodeInput) {
            // Listen for barcode scan events
            document.addEventListener('keydown', function(e) {
                // Check for barcode scan pattern (rapid keypresses)
                // This is a simple implementation
            });
        }
    }
}

// ===== Initialize on HTMX content load =====
if (typeof htmx !== 'undefined') {
    htmx.onLoad(function(content) {
        initDataTables();
        initCharts();
        initFormEnhancements();
    });
}

// ===== Make functions globally available =====
window.FixSoftRepair = {
    showToast,
    confirmAction,
    formatNumber,
    formatCurrency,
    formatDate,
    formatDateTime,
    exportToPDF,
    exportToExcel,
    printDocument,
    getCSRFToken
};
