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
        let miles = parseFloat(dist.dataset.mi);
        let km = Math.round((miles * 1.60934) * 100) / 100;
        dist.innerHTML = km.toFixed(2);    }

    for (let label of labels) {
        label.innerHTML = 'km'
    }

    for (let duration of durations) {
        let totalSeconds = duration.dataset.seconds
        if (totalSeconds > 0) {
            let distance = (parseFloat(duration.dataset.mi) * 1.60934).toFixed(2)
            let minutes = parseInt((totalSeconds / distance) / 60)
            let seconds = parseInt((totalSeconds /distance) % 60)
            duration.innerHTML = `${minutes}:${seconds}`
        } else {
            duration.innerHTML = "0:00"
        }

    }
}
