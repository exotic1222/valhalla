document.addEventListener('DOMContentLoaded', function() {
    var carousel = document.querySelector('.carousel-3d-inner');
    var items = document.querySelectorAll('.carousel-3d-item');
    var angle = 360 / items.length;
    var currentIndex = 0;

    function rotateCarousel() {
        var rotateAngle = currentIndex * -angle;
        carousel.style.transform = 'rotateY(' + rotateAngle + 'deg)';
    }

    document.querySelector('.carousel-control-next').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % items.length;
        rotateCarousel();
    });

    document.querySelector('.carousel-control-prev').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        rotateCarousel();
    });

    setInterval(function() {
        currentIndex = (currentIndex + 1) % items.length;
        rotateCarousel();
    }, 3000);
});