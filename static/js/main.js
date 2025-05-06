// Import common functionality
import { initTooltips, initPopovers } from './common/base.js';
import { lazyLoadImages } from './common/utils.js';

// Initialize common components
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    lazyLoadImages();
});

// Dynamic page script loading
function loadPageScript() {
    const bodyId = document.body.id;
    const pageScriptMap = {
        'recipe': '/static/js/pages/recipe.js',
        'recipe_dashboard': '/static/js/pages/recipe_dashboard.js',
        'recipe-detail': '/static/js/pages/recipe-detail.js'
        
    };

    if (bodyId && pageScriptMap[bodyId]) {
        import(pageScriptMap[bodyId]).catch(error => {
            console.error('Error loading page script:', error);
        });
    }
}

// Load page-specific scripts after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadPageScript);
} else {
    loadPageScript();
}