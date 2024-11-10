const slides = document.querySelectorAll(".slideshow-image");
let counter = 0;

const updateSlides = () => {
    slides.forEach((slide, index) => {
        slide.classList.remove("active");
        if (index === counter) {
            slide.classList.add("active");
        }
    });
};

const goNext = () => {
    counter = (counter + 1) % slides.length;
    updateSlides();
};

const goPrev = () => {
    counter = (counter - 1 + slides.length) % slides.length;
    updateSlides();
};

setInterval(goNext, 5000);

updateSlides();
