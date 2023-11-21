// Script to return to top of page when logo is pressed 
document.addEventListener('DOMContentLoaded', function () {
   

        const logo = document.querySelector('header img');
        logo.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        });
    });