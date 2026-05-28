(function () {
    const minus = document.getElementById('portions-minus');
    const plus = document.getElementById('portions-plus');
    const display = document.getElementById('portions-display');
    if (!minus || !plus || !display) return;

    const measures = document.querySelectorAll('.measure');
    const MIN = 1;
    const MAX = 5;
    let multiplier = 1;

    function parseAndMultiply(original, mult) {
        if (!original || original.includes('/')) return original;
        const match = original.match(/^(\d+(?:\.\d+)?)(.*)$/);
        if (!match) return original;
        const num = parseFloat(match[1]) * mult;
        const numStr = Number.isInteger(num) ? num.toString() : num.toFixed(1);
        return numStr + match[2];
    }

    function update() {
        display.textContent = `x${multiplier}`;
        measures.forEach((el) => {
            el.textContent = parseAndMultiply(el.dataset.original, multiplier);
        });
    }

    minus.addEventListener('click', () => {
        if (multiplier > MIN) { multiplier--; update(); }
    });

    plus.addEventListener('click', () => {
        if (multiplier < MAX) { multiplier++; update(); }
    });
})();
