const toastLiveExample = document.getElementsByClassName('toast')
const megaMenuToggle = document.getElementById("mega-menu-toggle");
const megaMenu = document.querySelector(".mega-menu");
const attributes = document.querySelectorAll(".attributes-p")


document.addEventListener("DOMContentLoaded", function () {


    const header = document.getElementById("header");

    function updateHeaderStyles() {
        if (window.scrollY > 30) {
            header.classList.add("shadow-lg")
        } else {
            header.classList.remove("shadow-lg")
        }
    }

// Listen for the scroll event and call the updateHeaderStyles function
    window.addEventListener("scroll", updateHeaderStyles);

    document.querySelectorAll(".animate").forEach(item => {
        const options = {
            threshold: 0.3,
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                console.log("not visited", entry.target)
                if (entry.isIntersecting) {

                    console.log("visited", entry.target)
                    entry.target.classList.toggle("opacity-0")
                    let animation = entry.target.getAttribute("data-animate")
                    entry.target.classList.add("animate__animated");
                    entry.target.classList.add(animation);


                    observer.disconnect();
                }
            });
        }, options);

        if (item)
            observer.observe(item);
    })


    if (attributes)
        attributes.forEach((item, index) => {
            let max = parseInt(item.getAttribute("data-number"))
            new Counter(`#attributes-${index + 1}`, {
                target: max,
                type: 'numeric',
                duration: 2000,
            });
        })


    function closeMegaMenu() {
        megaMenu.classList.remove("active");
    }


    if (megaMenuToggle)
        megaMenuToggle.addEventListener("click", (e) => {
            if (megaMenu.classList.contains("active")) {
                megaMenu.classList.remove("active");
            } else {
                megaMenu.classList.add("active");
            }
        });


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
                576: {
                    slidesPerView: 2,
                    spaceBetween: 20,
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 40,
                },
                992: {
                    slidesPerView: 4,
                    spaceBetween: 50,
                },
                1200: {
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


})

