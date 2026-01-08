// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Форма загрузки данных
    const runMainForm = document.getElementById('run-main-form');
    if (runMainForm) {
        runMainForm.addEventListener('submit', function() {
            const btn = document.getElementById('run-main-btn');
            const loading = document.getElementById('loading');

            btn.disabled = true;
            btn.textContent = 'Загружается...';
            loading.style.display = 'block';
        });
    }

    // Форма бюджетолога
    const budgetologForm = document.getElementById('budgetolog-form');
    if (budgetologForm) {
        budgetologForm.addEventListener('submit', function() {
            const btn = document.getElementById('recalculate-btn');
            const loading = document.getElementById('loading');

            btn.disabled = true;
            btn.textContent = 'Пересчитывается...';
            loading.style.display = 'block';
        });
    }
});