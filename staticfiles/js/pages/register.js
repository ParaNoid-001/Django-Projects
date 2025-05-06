import { initToasts, showSuccessModal } from '../common/notifications.js';
import { debounce } from '../common/base.js';
// static/js/register.js

// static/js/pages/register.js

/**
 * Registration Page JavaScript
 * Handles form validation, password strength, and profile picture preview
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all registration page functionality
    initProfilePicturePreview();
    initPasswordStrengthMeter();
    initPasswordConfirmation();
    initPasswordVisibilityToggles();
    initFormValidation();
});

/**
 * Initialize profile picture preview functionality
 */
function initProfilePicturePreview() {
    const profilePicInput = document.getElementById("id_profile_pic");
    
    if (profilePicInput) {
        profilePicInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imagePreview').style.backgroundImage = 'url(' + e.target.result + ')';
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}

/**
 * Initialize password strength meter
 */
function initPasswordStrengthMeter() {
    const password1 = document.getElementById('password1');
    if (!password1) return;

    const strengthBar = document.getElementById('password-strength-bar');
    const length = document.getElementById('length');
    const letter = document.getElementById('letter');
    const number = document.getElementById('number');
    const special = document.getElementById('special');
    
    password1.addEventListener('input', function() {
        const value = password1.value;
        let strength = 0;
        
        // Validate requirements
        const hasLength = value.length >= 8;
        const hasLetter = /[A-Za-z]/.test(value);
        const hasNumber = /\d/.test(value);
        const hasSpecial = /[^A-Za-z0-9]/.test(value);
        
        // Update requirements UI
        updateRequirement(length, hasLength);
        updateRequirement(letter, hasLetter);
        updateRequirement(number, hasNumber);
        updateRequirement(special, hasSpecial);
        
        // Calculate strength
        strength += hasLength ? 25 : 0;
        strength += hasLetter ? 25 : 0;
        strength += hasNumber ? 25 : 0;
        strength += hasSpecial ? 25 : 0;
        
        // Update strength bar
        strengthBar.style.width = strength + '%';
        updateStrengthBarColor(strengthBar, strength);
    });

    function updateRequirement(element, isValid) {
        if (!element) return;
        
        if (isValid) {
            element.classList.remove('text-muted');
            element.classList.add('text-success');
            element.querySelector('i').className = 'bi bi-check-circle-fill text-success me-1';
        } else {
            element.classList.remove('text-success');
            element.classList.add('text-muted');
            element.querySelector('i').className = 'bi bi-circle text-muted me-1';
        }
    }

    function updateStrengthBarColor(bar, strength) {
        if (strength < 50) {
            bar.className = 'progress-bar bg-danger';
        } else if (strength < 75) {
            bar.className = 'progress-bar bg-warning';
        } else {
            bar.className = 'progress-bar bg-success';
        }
    }
}

/**
 * Initialize password confirmation check
 */
function initPasswordConfirmation() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    
    if (!password1 || !password2) return;
    
    password2.addEventListener('input', function() {
        const feedback = document.getElementById('password-match-feedback');
        if (password2.value !== password1.value) {
            password2.classList.add('is-invalid');
            if (feedback) feedback.style.display = 'block';
        } else {
            password2.classList.remove('is-invalid');
            if (feedback) feedback.style.display = 'none';
        }
    });
}

/**
 * Initialize password visibility toggles
 */
function initPasswordVisibilityToggles() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('bi-eye-fill', 'bi-eye-slash-fill');
            } else {
                input.type = 'password';
                icon.classList.replace('bi-eye-slash-fill', 'bi-eye-fill');
            }
        });
    });
}

/**
 * Initialize form validation
 */
function initFormValidation() {
    'use strict';
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}