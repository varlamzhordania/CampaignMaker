const stepNext = document.querySelectorAll('.step-next');
const stepBack = document.querySelectorAll('.step-back');
const progress = document.querySelector('#progress');


Array.from(stepBack).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value - 35);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.remove("done")
    })
})


Array.from(stepNext).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value + 35);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.add("done")
    })
})