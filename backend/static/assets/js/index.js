
const toastLiveExample = document.getElementsByClassName('toast')

const triggerToast = (item) => {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
    toastBootstrap.show()
}

for (let toast of toastLiveExample){
    triggerToast(toast)
}


const forms = document.querySelectorAll('.needs-validation')

Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
    }, false)
})