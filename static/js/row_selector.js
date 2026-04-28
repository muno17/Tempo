// make entire rows clickable
document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('tr[data-href]');
    rows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', (e) => {
            console.log("clicked")
            // allow buttons to redirect to their proper pages
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                window.location.href = row.dataset.href;
            }
        });
    });

});
