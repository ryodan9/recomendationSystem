// Scrolling Navigation Bar
// const nav = document.querySelector("nav");
// const sectionOne = document.querySelector(".jumbotron");

// const sectionOneOptions = {
//     rootMargin: "-600px 0px 0px 0px"
// };

// const sectionOneObserver = new IntersectionObserver
// (function(
//     entries, 
//     sectionOneObserver
// ){
//     entries.forEach(entry => {
//         if(!entry.isIntersecting) {
//             nav.classList.add("nav-scrolled");
//         } else {
//             nav.classList.remove("nav-scrolled");
//         }
//     });
// }, 
// sectionOneOptions);

// sectionOneObserver.observe(sectionOne);

var nav = document.querySelector('nav'); // Identify target
var navLink = document.querySelectorAll('.nav-link');
var navBrand = document.querySelector('.navbar-brand');

window.addEventListener('scroll', function(event) { // To listen for event
    event.preventDefault();

    if (window.scrollY <= 150) { // 
        nav.style.backgroundColor = 'transparent'; // or default color
        nav.style.boxShadow = "0px 0px 0px black";
        navBrand.style.color = '#000';
        navLink.forEach(link => {
          link.style.color = "black";
        });
    } else {
        nav.style.backgroundColor = '#069fbf';
        nav.style.boxShadow = "1px 2px 15px black";
        navBrand.style.color = '#fff';
        navLink.forEach(link => {
          link.style.color = "white";
        });
    }
});

// document.getElementById('recForm').onsubmit = function (event) {
//   event.preventDefault(); // Mencegah form melakukan submit biasa

//   // Mengarahkan ke div dengan ID 'targetDiv'
//   document.getElementById('hasil-rekomendasi').scrollIntoView({ behavior: 'smooth' });
// };