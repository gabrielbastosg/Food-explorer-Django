(function () {
    const list = document.querySelector('.ingredients-list');
    if (!list) return;

    const mealId = list.dataset.mealId;
    const storageKey = `ingredients_checked_${mealId}`;
    const checkboxes = list.querySelectorAll('.ingredient-check');

    // 1. Restaurar estado salvo
    const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
    checkboxes.forEach((cb) => {
        if (saved.includes(cb.dataset.index)) {
            cb.checked = true;
        }
    });

    // 2. Salvar a cada mudança
    list.addEventListener('change', () => {
        const checked = [];
        checkboxes.forEach((cb) => {
            if (cb.checked) checked.push(cb.dataset.index);
        });
        localStorage.setItem(storageKey, JSON.stringify(checked));
    });
})();