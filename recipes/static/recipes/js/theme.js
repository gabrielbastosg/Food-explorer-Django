(function () {
    const button = document.getElementById('theme-toggle');
    if (!button) return;

    const html = document.documentElement;
    const STORAGE_KEY = 'theme';

    // 1. Aplicar tema salvo (ou claro por padrão)
    if (localStorage.getItem(STORAGE_KEY) === 'dark') {
        html.setAttribute('data-theme', 'dark');
        button.textContent = '☀️';
    }

    // 2. Toggle ao clicar
    button.addEventListener('click', () => {
        const isDark = html.getAttribute('data-theme') === 'dark';
        if (isDark) {
            html.removeAttribute('data-theme');
            button.textContent = '🌙';
            localStorage.setItem(STORAGE_KEY, 'light');
        } else {
            html.setAttribute('data-theme', 'dark');
            button.textContent = '☀️';
            localStorage.setItem(STORAGE_KEY, 'dark');
        }
    });
})();
