// Handle all notification toasts
function initToasts() {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    const toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(toast => toast.show());
}

function showSuccessModal() {
    const successMessages = document.querySelectorAll('.alert-success');
    if (successMessages.length > 0) {
        const successModalElement = document.getElementById('successModal');
        if (successModalElement) {
            setTimeout(() => {
                const successModal = new bootstrap.Modal(successModalElement);
                successModal.show();
            }, 1000);
        }
    }
}

export { initToasts, showSuccessModal };