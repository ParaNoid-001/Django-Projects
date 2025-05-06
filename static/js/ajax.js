

class ContactForm {
  constructor(formId, sendbutton, responseId) {
    this.form = document.getElementById(formId);
    this.submitBtn = document.getElementById(sendbutton);
    this.response = document.getElementById(responseId);
    
    if (!this.form || !this.submitBtn || !this.response) return;
    
    this.init();
  }

  init() {
    // Real-time validation
    this.form.querySelectorAll('input, textarea').forEach(field => {
      field.addEventListener('input', () => this.validateField(field));
    });

    // Form submission
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  handleSubmit(e) {
    e.preventDefault();
    
    // Validate all fields
    let isValid = true;
    this.form.querySelectorAll('[required]').forEach(field => {
      if (!this.validateField(field)) {
        isValid = false;
      }
    });

    if (!isValid) {
      this.form.classList.add('was-validated');
      this.showResponse(false, 'Please fill all required fields correctly.');
      this.scrollToResponse();
      return;
    }

    this.submitForm();
  }

  submitForm() {
    // Prepare form data
    const formData = new FormData(this.form);
    
    // UI updates
    this.toggleSubmitButton(true);
    this.clearResponse();

    // AJAX request
    fetch(this.form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      }
    })
    .then(response => response.json())
    .then(data => this.handleResponse(data))
    .catch(error => this.handleError(error))
    .finally(() => {
      this.toggleSubmitButton(false);
      this.scrollToResponse();
    });
  }

  handleResponse(data) {
    this.showResponse(data.success, data.message);
    if (data.success) {
      this.resetForm();
    }
  }

  handleError(error) {
    console.error('Error:', error);
    this.showResponse(false, 'An error occurred while sending your message. Please try again later.');
  }

  validateField(field) {
    const isValid = field.checkValidity();
    
    if (field.type === 'email' && field.value) {
      const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value);
      if (!emailValid) {
        field.setCustomValidity('Please enter a valid email address');
        this.updateFieldClasses(field, false);
        return false;
      }
    }
    
    if (isValid) {
      field.setCustomValidity('');
      this.updateFieldClasses(field, true);
      return true;
    } else {
      this.updateFieldClasses(field, false);
      return false;
    }
  }

  updateFieldClasses(field, isValid) {
    if (isValid) {
      field.classList.add('is-valid');
      field.classList.remove('is-invalid');
    } else {
      field.classList.add('is-invalid');
      field.classList.remove('is-valid');
    }
  }

  showResponse(isSuccess, message) {
    const alertClass = isSuccess ? 'alert-success' : 'alert-danger';
    this.response.innerHTML = `
      <div class="alert ${alertClass} alert-dismissible fade show">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
  }

  scrollToResponse() {
    this.response.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
  }

  toggleSubmitButton(isLoading) {
    this.submitBtn.disabled = isLoading;
    this.submitBtn.innerHTML = isLoading
      ? '<span class="spinner-border spinner-border-sm" aria-hidden="true"></span> Sending...'
      : '<i class="bi bi-send-fill me-2"></i>Send Message';
  }

  clearResponse() {
    this.response.innerHTML = '';
  }

  resetForm() {
    this.form.reset();
    this.form.classList.remove('was-validated');
    this.form.querySelectorAll('.is-valid').forEach(el => {
      el.classList.remove('is-valid');
    });
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ContactForm('contactForm', 'submitBtn', 'responseMessage');
});
