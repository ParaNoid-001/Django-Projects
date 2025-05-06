import { initToasts, showSuccessModal } from '../common/notifications.js';
import { debounce } from '../common/base.js';

function initCarousel() {
    const myCarousel = document.getElementById('recipeCarousel');
    if (myCarousel) {
        const carousel = new bootstrap.Carousel(myCarousel, {
            interval: 5000,
            ride: 'carousel'
        });

        // Parallax effect
        window.addEventListener('scroll', debounce(function() {
            const scrollPosition = window.pageYOffset;
            myCarousel.style.transform = `translateY(${scrollPosition * 0.2}px)`;
        }, 10));
    }
}

function animateCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('animate-fade-in');
        card.classList.add(`delay-${index % 4 + 1}`);
    });
}

function initNewsletterModal() {
    setTimeout(() => {
        const newsletterModalElement = document.getElementById('newsletterModal');
        if (newsletterModalElement) {
            new bootstrap.Modal(newsletterModalElement).show();
        }
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    initCarousel();
    animateCards();
    initNewsletterModal();
    initToasts();
    showSuccessModal();
});

