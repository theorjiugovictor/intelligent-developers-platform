// Modern API Documentation JavaScript

// Active navigation link highlighting
document.addEventListener('DOMContentLoaded', () => {
    // Handle navigation link clicks
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Update active link based on scroll position
    const sections = document.querySelectorAll('.section');
    const observerOptions = {
        root: null,
        rootMargin: '-100px 0px -66%',
        threshold: 0
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    sections.forEach(section => observer.observe(section));

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button to code blocks
    document.querySelectorAll('.code-block').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.title = 'Copy to clipboard';
        
        button.addEventListener('click', () => {
            const code = block.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.innerHTML = '<i class="fas fa-check"></i>';
                button.style.color = '#10b981';
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-copy"></i>';
                    button.style.color = '';
                }, 2000);
            });
        });
        
        block.style.position = 'relative';
        block.appendChild(button);
    });
});

// Function to try API endpoints
async function tryEndpoint(endpoint) {
    const resultDiv = document.getElementById(`${endpoint}-result`);
    
    if (!resultDiv) {
        console.error('Result div not found for endpoint:', endpoint);
        return;
    }

    resultDiv.style.display = 'block';
    resultDiv.className = 'result-panel result-loading';
    resultDiv.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div class="spinner"></div>
            <span>Loading...</span>
        </div>
    `;

    let url;
    switch(endpoint) {
        case 'health':
            url = '/health';
            break;
        case 'status':
            url = '/api/v1/status';
            break;
        case 'metrics':
            url = '/api/v1/metrics';
            break;
        case 'recommendations':
            url = '/api/v1/recommendations';
            break;
        default:
            url = '/';
    }

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        resultDiv.className = 'result-panel result-success';
        resultDiv.innerHTML = `
            <h4><i class="fas fa-check-circle" style="color: #10b981;"></i> Success (${response.status})</h4>
            <div class="code-block">
                <pre><code>${JSON.stringify(data, null, 2)}</code></pre>
            </div>
        `;

        // Add copy button to the new code block
        const codeBlock = resultDiv.querySelector('.code-block');
        if (codeBlock && !codeBlock.querySelector('.copy-button')) {
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.innerHTML = '<i class="fas fa-copy"></i>';
            button.title = 'Copy to clipboard';
            
            button.addEventListener('click', () => {
                const code = codeBlock.querySelector('code').textContent;
                navigator.clipboard.writeText(code).then(() => {
                    button.innerHTML = '<i class="fas fa-check"></i>';
                    button.style.color = '#10b981';
                    setTimeout(() => {
                        button.innerHTML = '<i class="fas fa-copy"></i>';
                        button.style.color = '';
                    }, 2000);
                });
            });
            
            codeBlock.style.position = 'relative';
            codeBlock.appendChild(button);
        }
    } catch (error) {
        resultDiv.className = 'result-panel result-error';
        resultDiv.innerHTML = `
            <h4><i class="fas fa-exclamation-circle" style="color: #ef4444;"></i> Error</h4>
            <p style="color: #fca5a5; margin-top: 0.5rem;">${error.message}</p>
            <p style="color: var(--text-secondary); margin-top: 0.5rem; font-size: 0.875rem;">
                Make sure the API server is running on port 8000.
            </p>
        `;
    }
}

// Add styles for copy button dynamically
const style = document.createElement('style');
style.textContent = `
    .copy-button {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        padding: 0.5rem;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid var(--primary-color);
        border-radius: 0.375rem;
        color: var(--primary-light);
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
    }
    
    .copy-button:hover {
        background: rgba(99, 102, 241, 0.3);
        transform: scale(1.05);
    }
    
    .copy-button:active {
        transform: scale(0.95);
    }
`;
document.head.appendChild(style);

// Mobile menu toggle (for future enhancement)
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press '/' to focus search (if we add search later)
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        // Focus search input if it exists
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Add animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.endpoint-card, .feature-card, .card');
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    };
    
    const observer = new IntersectionObserver(observerCallback, observerOptions);
    
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(element);
    });
};

// Initialize animations when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', animateOnScroll);
} else {
    animateOnScroll();
}

// Console message
console.log('%c Intelligence Engine API Documentation ', 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 16px; font-weight: bold; padding: 10px 20px; border-radius: 5px;');
console.log('%c Built with ❤️ for developers ', 'color: #6366f1; font-size: 12px; font-style: italic;');
