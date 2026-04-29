function initializeUnits() {
    const unitPref = localStorage.getItem('unit') || 'mi';

    // update the table/header label
    const unitHeader = document.getElementById('unit-header');
    if (unitHeader) {
        unitHeader.innerText = `Distance (${unitPref})`;
    }

    // update the hidden input before submission
    const form = document.querySelector('form');
    const hiddenInput = document.getElementById('unit_type');

    if (form && hiddenInput) {
        form.addEventListener('submit', function() {
            hiddenInput.value = localStorage.getItem('unit') || 'mi';
        });
    }
}

window.addEventListener('DOMContentLoaded', initializeUnits);