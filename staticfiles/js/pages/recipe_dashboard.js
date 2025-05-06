import { initToasts, showSuccessModal } from '../common/notifications.js';
import { debounce } from '../common/base.js';

import { initTooltips, initPopovers } from '../common/base.js';
import { lazyLoadImages } from '../common/utils.js';


document.addEventListener('DOMContentLoaded', function() {
    // Select/Deselect all checkboxes
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.recipe-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkDeleteBtn();
        });
    }

    // Update bulk delete button state
    function updateBulkDeleteBtn() {
        const checkedCount = document.querySelectorAll('.recipe-checkbox:checked').length;
        const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
        if (bulkDeleteBtn) {
            bulkDeleteBtn.disabled = checkedCount === 0;
            bulkDeleteBtn.innerHTML = checkedCount > 0 ? 
                `<i class="bi bi-trash"></i> Delete Selected (${checkedCount})` : '<i class="bi bi-trash"></i> Delete Selected';
        }
    }

    // Checkbox change event
    document.querySelectorAll('.recipe-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkDeleteBtn);
    });

    // Bulk delete form submission
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    if (bulkDeleteBtn) {
        bulkDeleteBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete the selected recipes?')) {
                document.getElementById('bulkDeleteForm').submit();
            }
        });
    }

    // Individual delete button handling
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const recipeId = this.getAttribute('data-id');
            const deleteForm = document.getElementById('deleteForm');
            deleteForm.action = `/delete-recipe/${recipeId}/`;
            
            const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
            modal.show();
        });
    });
});