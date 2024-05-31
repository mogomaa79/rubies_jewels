// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// overlay menu
function openNav() {
    document.getElementById("myNav").classList.toggle("menu_width");
    document.querySelector(".custom_menu-btn").classList.toggle("menu_btn-style");
}


/** google_map js **/

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// lightbox gallery
$(document).on("click", '[data-toggle="lightbox"]', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});

$(document).ready(function() {
    $('.carousel').carousel({
      interval: 1000
    });
  });


$('#productCarousel').on('click', '.carousel-item img', function() {
    var src = $(this).attr('src');
    $('#modalImage').attr('src', src);
    $('#imageModal').modal('show');
});

document.addEventListener('DOMContentLoaded', function() {
    var carousel = $('#productCarousel');
    var modalImage = document.getElementById('modalImage');
  
    // Ensure the carousel works smoothly
    carousel.carousel({
      interval: 3000
    });
  
    // Image click event to open modal with larger image
    document.querySelectorAll('#productCarousel img').forEach(function(image) {
      image.addEventListener('click', function() {
        modalImage.src = image.src;
      });
    });
  });
  
  function changeImage(element) {
    document.getElementById('mainImage').src =  element.src;
    document.getElementById('mainImage').style.transform = 'scale(1.1)';
    setTimeout(function() {
      document.getElementById('mainImage').style.transform = 'scale(1)';
    }, 300);
  }
  