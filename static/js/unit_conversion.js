let toggle = document.getElementById('km_toggle')

toggle.addEventListener('change', (e) => {
    if (e.target.checked) {
        toggleKm()
    } else {
        toggleMi()
    }
})

function toggleMi() {
    let distance = document.querySelectorAll('.distance')
    let labels = document.querySelectorAll('.distance-label')
    let durations = document.querySelectorAll('.pace')

    for (let dist of distance) {
        dist.innerHTML = parseFloat(dist.dataset.mi)
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
        dist.innerHTML = (parseFloat(dist.dataset.mi) * 1.60934).toFixed(2)
    }

    for (let label of labels) {
        label.innerHTML = 'km'
    }

    for (let duration of durations) {
        let distance = (parseFloat(duration.dataset.mi) * 1.60934).toFixed(2)
        let totalSeconds = duration.dataset.seconds
        let minutes = parseInt((totalSeconds / distance) / 60)
        let seconds = parseInt((totalSeconds /distance) % 60)
        duration.innerHTML = `${minutes}:${seconds}`
    }
}
