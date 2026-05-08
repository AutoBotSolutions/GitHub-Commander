// GitHub Commander - Sci-Fi Theme JavaScript

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

// Dynamic star field
function createStars() {
    const starsContainer = document.querySelector('.stars');
    const numberOfStars = 100;
    
    for (let i = 0; i < numberOfStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.animationDelay = Math.random() * 5 + 's';
        starsContainer.appendChild(star);
    }
}

// Add parallax effect to hero section
function initParallax() {
    const hero = document.querySelector('.hero');
    const heroVisual = document.querySelector('.hero-visual');
    
    window.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        if (heroVisual) {
            heroVisual.style.transform = `translateY(-50%) translate(${x}px, ${y}px)`;
        }
    });
}

// Glitch effect enhancement
function enhanceGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch');
    
    glitchElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                element.style.animation = 'none';
                element.offsetHeight; // Trigger reflow
                element.style.animation = '';
            }
        }, 100);
    });
}

// Typing effect for hero subtitle
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Intersection Observer for animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Observe doc links
    document.querySelectorAll('.doc-link').forEach((link, index) => {
        link.style.animationDelay = `${index * 0.1}s`;
        observer.observe(link);
    });
}

// Add CSS animation class
const style = document.createElement('style');
style.textContent = `
    .feature-card, .doc-link {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease-out;
    }
    
    .feature-card.animate-in, .doc-link.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// Navigation background on scroll
function handleScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(5, 5, 8, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 240, 255, 0.2)';
        } else {
            navbar.style.background = 'rgba(10, 10, 20, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Button hover sound effect (optional - visual feedback)
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    createStars();
    initParallax();
    enhanceGlitchEffect();
    initScrollAnimations();
    handleScroll();
    initButtonEffects();
    
    // Typing effect for hero subtitle
    const heroSubtitle = document.querySelector('.hero-subtitle');
    if (heroSubtitle) {
        const originalText = heroSubtitle.textContent;
        typeWriter(heroSubtitle, originalText, 30);
    }
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Console easter egg
console.log('%c GitHub Commander ', 'background: #00f0ff; color: #0a0a0f; font-size: 20px; font-weight: bold; padding: 10px;');
console.log('%c The Future of GitHub Management ', 'color: #00f0ff; font-size: 14px;');
console.log('%c Initializing systems... ', 'color: #00ff88; font-size: 12px;');
console.log('%c Systems online. Welcome, Commander. ', 'color: #ff00ff; font-size: 12px;');
