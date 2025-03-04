  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// FAQ accordion functionality
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const item = question.parentElement;
        item.classList.toggle('active');
    });
});

// Simple testimonial slider
const testimonialsSlider = document.querySelector('.testimonials-slider');
let isDown = false;
let startX;
let scrollLeft;

testimonialsSlider.addEventListener('mousedown', (e) => {
    isDown = true;
    startX = e.pageX - testimonialsSlider.offsetLeft;
    scrollLeft = testimonialsSlider.scrollLeft;
});

testimonialsSlider.addEventListener('mouseleave', () => {
    isDown = false;
});

testimonialsSlider.addEventListener('mouseup', () => {
    isDown = false;
});

testimonialsSlider.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - testimonialsSlider.offsetLeft;
    const walk = (x - startX) * 2; // Scroll speed
    testimonialsSlider.scrollLeft = scrollLeft - walk;
});

// Add animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.feature-card, .step, .demo-point, .stat-item');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

// Set initial styles for animation
document.querySelectorAll('.feature-card, .step, .demo-point, .stat-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
});

// Call animation function on scroll
window.addEventListener('scroll', animateOnScroll);
// Call once on page load
window.addEventListener('load', animateOnScroll);

// Mobile menu toggle (add a hamburger menu button in your HTML)
const mobileMenuButton = document.createElement('div');
mobileMenuButton.classList.add('mobile-menu-button');
mobileMenuButton.innerHTML = '<i class="fas fa-bars"></i>';
document.querySelector('nav').appendChild(mobileMenuButton);

mobileMenuButton.addEventListener('click', () => {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('show');
});

// Add some styles for the mobile menu
const style = document.createElement('style');
style.textContent = `
    .mobile-menu-button {
        display: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
    
    @media (max-width: 768px) {
        .mobile-menu-button {
            display: block;
        }
        
        .nav-links.show {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 80px;
            left: 0;
            right: 0;
            background-color: white;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        .nav-links.show li {
            margin: 10px 0;
        }
    }
`;
document.head.appendChild(style);