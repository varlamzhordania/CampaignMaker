const toastLiveExample = document.getElementsByClassName('toast')
const megaMenuToggle = document.getElementById("mega-menu-toggle");
const megaMenu = document.querySelector(".mega-menu");
const attributes = document.querySelectorAll(".attributes-p")


if (attributes)
    attributes.forEach((item,index) => {
        let max = parseInt(item.getAttribute("data-number"))
        new Counter(`#attributes-${index+1}`, {
            target: max,
            type: 'numeric',
            duration:3000,
        });
    })

// Function to close the mega menu
function closeMegaMenu() {
    megaMenu.classList.remove("active");
}

// Toggle mega menu on button click
if (megaMenuToggle)
    megaMenuToggle.addEventListener("click", (e) => {
        if (megaMenu.classList.contains("active")) {
            megaMenu.classList.remove("active");
        } else {
            megaMenu.classList.add("active");
        }
    });

// Close the mega menu when clicking outside
if (megaMenu)
    document.addEventListener("click", (e) => {
        if (!megaMenu.contains(e.target) && e.target !== megaMenuToggle) {
            closeMegaMenu();
        }
    });


const triggerToast = (item) => {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
    toastBootstrap.show()
}

for (let toast of toastLiveExample) {
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

if (document.querySelector(".swiper")) {
    const swiper = new Swiper('.swiper', {
        // Optional parameters
        direction: 'horizontal',
        loop: false,
        grabCursor: true,
        slidesPerView: 1,
        spaceBetween: 30,
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 4,
                spaceBetween: 40,
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 50,
            },
        },
        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },


        // Navigation arrows
        // navigation: {
        //     nextEl: '.swiper-button-next',
        //     prevEl: '.swiper-button-prev',
        // },

        // And if we need scrollbar
        // scrollbar: {
        //     el: '.swiper-scrollbar',
        // },
    });
}
