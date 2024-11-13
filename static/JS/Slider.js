const slides = document.querySelectorAll('.slideshow-image');
const donateButton = document.getElementById('donateButton');
let currentSlide = 0;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i !== 3) donateButton.classList.remove('show');
        if (i !== 2) donateButton.classList.remove('show2');
    });

    slides[index].classList.add('active');

    if (index === 3) {
        donateButton.classList.add('show');
    }
    if (index === 2) {
        donateButton.classList.add('show2');
    }
}

function goPrev() {
    currentSlide = (currentSlide === 0) ? slides.length - 1 : currentSlide - 1;
    showSlide(currentSlide);
}

function goNext() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

showSlide(currentSlide);
