document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.cocktail-item img, .cocktail-item h3, .cocktail-item p');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
            }
        });
    }, { threshold: 0.1 });

    items.forEach(item => {
        observer.observe(item);
    });
});