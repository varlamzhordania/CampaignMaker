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


// Function to check if all required fields within the current step's form are completed and the form is visible
function checkFormCompletion() {
    var currentStepForm = document.querySelector('.collapse.show'); // Assuming this selects the currently visible form
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

    console.log(button_one)
    console.log(counter)
    var nextButton = document.querySelector(`.step-next.${counter}`);
    nextButton.disabled = !isFormComplete;
}

// Add event listeners to form fields to trigger the checkFormCompletion function
var formFields = document.querySelectorAll('input, select, textarea');
formFields.forEach(function (field) {
    field.addEventListener('input', checkFormCompletion);
});

// Trigger the checkFormCompletion function when the second step is shown (assuming you use Bootstrap collapse)
var secondStep = document.getElementById('collapseTwo');
secondStep.addEventListener('shown.bs.collapse', checkFormCompletion);