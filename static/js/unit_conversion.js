let unitToggle = document.getElementById('km_toggle')

function applyUnits(useKm) {
    unitToggle.checked = useKm
    if (useKm) {
        toggleKm()
    } else {
        toggleMi()
    }
}

unitToggle.addEventListener('change', (e) => {
    if (e.target.checked) {
        localStorage.setItem('unit','km')
        applyUnits(true)
    } else {
        localStorage.setItem('unit','mi')
        applyUnits(false)
    }
})

// load the localStorage item if there is one
window.addEventListener('DOMContentLoaded', () => {
    let savedUnit = localStorage.getItem('unit')

    if (savedUnit === 'km') {
        applyUnits(true)
    }
})

function toggleMi() {
    let distance = document.querySelectorAll('.distance')
    let labels = document.querySelectorAll('.distance-label')
    let durations = document.querySelectorAll('.pace')

    for (let dist of distance) {
        dist.innerHTML = (parseFloat(dist.dataset.mi)).toFixed(2)
    }

    for (let label of labels) {
        label.innerHTML = 'mi'
    }

    for (let duration of durations) {
        duration.innerHTML = duration.dataset.miPace
    }

}

function toggleKm() {
    let distance = document.querySelectorAll('.distance')
    let labels = document.querySelectorAll('.distance-label')
    let durations = document.querySelectorAll('.pace')

    for (let dist of distance) {
        let miles = parseFloat(dist.dataset.mi)
        let km = miles * 1.60934
        dist.innerHTML = km.toFixed(2)
    }

    for (let label of labels) {
        label.innerHTML = 'km'
    }

    for (let duration of durations) {
        let totalSeconds = duration.dataset.seconds
        if (totalSeconds > 0) {
            let distance = (parseFloat(duration.dataset.mi) * 1.60934)
            let minutes = parseInt((totalSeconds / distance) / 60)
            let seconds = parseInt((totalSeconds /distance) % 60)
            duration.innerHTML = `${minutes}:${seconds}`
        } else {
            duration.innerHTML = "0:00"
        }

    }
}

// for convert initial values of update forms
window.addEventListener('DOMContentLoaded', () => {
    const currentUnit = localStorage.getItem('unit') || 'mi';

    // convert if km is toggled on
    if (currentUnit === 'km') {
        let inputs = document.querySelectorAll('input[name$="-distance"]');
        inputs.forEach(input => {
            if (input.value) {
                let miles = parseFloat(input.value);
                input.value = (miles * 1.60934).toFixed(2);
            }
        });

        // update headers
        const header = document.getElementById('unit-header')
        const hiddenInput = document.getElementById('unit_type')
        if (header) {
            header.innerText = 'Distance (km)'
        }
        if (hiddenInput) {
            hiddenInput.value = 'km'
        }
    }
});