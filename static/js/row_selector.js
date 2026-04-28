// make entire rows clickable
document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('tr[data-href]');
    rows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', (e) => {
            // allow buttons to redirect to their corresponding pages
            // don't overwrite functionality for buttons
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                window.location.href = row.dataset.href;
            }
        });
    });
});
