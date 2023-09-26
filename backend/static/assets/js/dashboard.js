const stepNext = document.querySelectorAll('.step-next');
const stepBack = document.querySelectorAll('.step-back');
const progress = document.querySelector('#progress');
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


const disapproveModal = new bootstrap.Modal('#disapprove-modal')


const disapproveButtons = document.querySelectorAll(".disapprove-button")


disapproveButtons.forEach(button => {
    button.addEventListener("click", (e) => {
        const campaign_id = e.currentTarget.getAttribute("data-ca")
        document.getElementById("disapprove-modal-title").innerHTML = `Disapprove campaign-${campaign_id}`
        document.getElementById("disapprove-campaign-id").value = campaign_id
        disapproveModal.show()
    })

})


Array.from(stepBack).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value - 25);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.remove("done")
    })
})


Array.from(stepNext).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value + 25);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.add("done")
    })
})


function checkFormCompletion() {
    var currentStepForm = document.querySelector('.collapse.show');
    var requiredFields = currentStepForm.querySelectorAll('[required]');
    var isFormComplete = true;
    let counter

    requiredFields.forEach(function (field) {
        if (!field.value) {
            isFormComplete = false;
        }
    });
    let button_one = currentStepForm.classList.contains("one")
    let button_two = currentStepForm.classList.contains("two")
    let button_three = currentStepForm.classList.contains("three")
    let button_forth = currentStepForm.classList.contains("forth")


    if (button_one)
        counter = "one"
    if (button_two)
        counter = "two"
    if (button_three)
        counter = "three"
    if (button_forth)
        counter = "forth"

    var nextButton = document.querySelector(`.step-next.${counter}`);
    nextButton.disabled = !isFormComplete;
}

var formFields = document.querySelectorAll('input, select, textarea');
formFields.forEach(function (field) {
    field.addEventListener('input', checkFormCompletion);
});

var secondStep = document.getElementById('collapseTwo');
secondStep.addEventListener('shown.bs.collapse', checkFormCompletion);