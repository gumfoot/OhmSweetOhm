$(document).ready(function() {
    "use strict";

    // Mobile Nav toggle
    $('.menu-toggle > a').on('click', function (e) {
        e.preventDefault();
        $('#responsive-nav').toggleClass('active');
    });

    // Fix cart dropdown from closing
    $('.cart-dropdown').on('click', function (e) {
        e.stopPropagation();
    });

$(document).ready(function() {
    $('.tab-nav a').click(function(e) {
        e.preventDefault();
        $(this).tab('show');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const leftSlider = document.querySelector('.left-slider .slider');
    const rightSlider = document.querySelector('.right-slider .slider');

    let leftIndex = 0;
    let rightIndex = 0;

    function slideLeft() {
        leftIndex = (leftIndex + 1) % leftSlider.children.length;
        leftSlider.style.transform = `translateX(-${leftIndex * 100}%)`;
    }

    function slideRight() {
        rightIndex = (rightIndex + 1) % rightSlider.children.length;
        rightSlider.style.transform = `translateX(-${rightIndex * 100}%)`;
    }

    setInterval(slideLeft, 3000); // Slide every 3 seconds for the left slider
    setInterval(slideRight, 3000); // Slide every 3 seconds for the right slider
});




    /////////////////////////////////////////

    // Initialize Slick sliders

    // Products Slick
    $('.products-slick').each(function() {
        var $this = $(this),
                $nav = $this.attr('data-nav');

        $this.slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            infinite: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
            responsive: [{
                breakpoint: 991,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            },
            ]
        });
    });

    // Products Widget Slick
    $('.products-widget-slick').each(function() {
        var $this = $(this),
                $nav = $this.attr('data-nav');

        $this.slick({
            infinite: true,
            autoplay: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
        });
    });

    // Product Main img Slick
    $('#product-main-img').slick({
        infinite: true,
        speed: 300,
        dots: false,
        arrows: true,
        fade: true,
        asNavFor: '#product-imgs',
    });

    // Product imgs Slick
    $('#product-imgs').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: true,
        centerMode: true,
        focusOnSelect: true,
        centerPadding: 0,
        vertical: true,
        asNavFor: '#product-main-img',
        responsive: [{
            breakpoint: 991,
            settings: {
                vertical: false,
                arrows: false,
                dots: true,
            }
        },
        ]
    });

    // Product img zoom
    var zoomMainProduct = document.getElementById('product-main-img');
    if (zoomMainProduct) {
        $('#product-main-img .product-preview').zoom();
    }

    /////////////////////////////////////////

    // Handle automatic image switching on hover
    $('.thumb-image').on('mouseover', function() {
        var imgSrc = $(this).attr('src');
        $('#product-main-img img').attr('src', imgSrc);
    });

    // Input number
    $('.input-number').each(function() {
        var $this = $(this),
        $input = $this.find('input[type="number"]'),
        up = $this.find('.qty-up'),
        down = $this.find('.qty-down');

        down.on('click', function () {
            var value = parseInt($input.val()) - 1;
            value = value < 1 ? 1 : value;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
        });

        up.on('click', function () {
            var value = parseInt($input.val()) + 1;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
        });
    });

    var priceInputMax = document.getElementById('price-max'),
            priceInputMin = document.getElementById('price-min');

    priceInputMax.addEventListener('change', function(){
        updatePriceSlider($(this).parent() , this.value);
    });

    priceInputMin.addEventListener('change', function(){
        updatePriceSlider($(this).parent() , this.value);
    });

    function updatePriceSlider(elem , value) {
        if ( elem.hasClass('price-min') ) {
            priceSlider.noUiSlider.set([value, null]);
        } else if ( elem.hasClass('price-max')) {
            priceSlider.noUiSlider.set([null, value]);
        }
    }

    // Price Slider
    var priceSlider = document.getElementById('price-slider');
    if (priceSlider) {
        noUiSlider.create(priceSlider, {
            start: [1, 999],
            connect: true,
            step: 1,
            range: {
                'min': 1,
                'max': 999
            }
        });

        priceSlider.noUiSlider.on('update', function( values, handle ) {
            var value = values[handle];
            handle ? priceInputMax.value = value : priceInputMin.value = value;
        });
    }

});


const getCookie = (name) => {
    const value = " " + document.cookie;
    console.log("value", `==${value}==`);
    const parts = value.split(" " + name + "=");
    return parts.length < 2 ? undefined : parts.pop().split(";").shift();
  };
  
  const setCookie = function (name, value, expiryDays, domain, path, secure) {
    const exdate = new Date();
    exdate.setHours(
      exdate.getHours() +
        (typeof expiryDays !== "number" ? 365 : expiryDays) * 24
    );
    document.cookie =
      name +
      "=" +
      value +
      ";expires=" +
      exdate.toUTCString() +
      ";path=" +
      (path || "/") +
      (domain ? ";domain=" + domain : "") +
      (secure ? ";secure" : "");
  };



  function acceptCookies() {
    // Implement logic to accept cookies (e.g., set cookies)
    // For demonstration, hide the banner
    document.querySelector('.cookies-eu-banner').style.display = 'none';
}

function denyCookies() {
    // Implement logic to deny cookies (e.g., do not set cookies)
    // For demonstration, show a message or perform other actions
    alert('You have denied all cookies. Some features may not work properly.');
}



document.addEventListener("DOMContentLoaded", function() {
    const banner = document.querySelector('.cookies-eu-banner');
    const acceptBtn = document.querySelector('.accept-btn');

    // Check if acceptBtn and banner exist
    if (acceptBtn && banner) {
        acceptBtn.addEventListener('click', function() {
            banner.style.display = 'none'; // Hide the banner
        });
    }
});




document.addEventListener('DOMContentLoaded', function() {
    const productSlider = document.getElementById('slick-new-products-horizontal');
    const products = productSlider.querySelectorAll('.product-item');
    const totalProducts = products.length;
    let currentIndex = 0;
    const intervalTime = 3000;

    // Clone products for continuous loop
    const clones = [];
    const cloneCount = Math.min(3, totalProducts); // Number of clones per side (adjust as needed)
    
    for (let i = 0; i < cloneCount; i++) {
        clones.push(products[i].cloneNode(true)); // Clones from the beginning
        clones.unshift(products[totalProducts - 1 - i].cloneNode(true)); // Clones from the end
    }

    clones.forEach(clone => productSlider.appendChild(clone)); // Append all clones

    // Update products after adding clones
    const updatedProducts = productSlider.querySelectorAll('.product-item');
    const totalSlides = updatedProducts.length;

    // Calculate total width needed for continuous sliding
    const itemWidth = updatedProducts[0].offsetWidth + 10; // Adjust margin if necessary
    productSlider.style.width = itemWidth * totalSlides + 'px';

    function showNextProduct() {
        currentIndex++;

        // Calculate the translate value
        const translateValue = -1 * currentIndex * itemWidth;

        // Apply transform to slide
        productSlider.style.transform = `translateX(${translateValue}px)`;

        // Check if we've reached the last clone
        if (currentIndex >= totalSlides - (2 * cloneCount)) {
            // Reset back to the beginning without transition
            setTimeout(() => {
                currentIndex = cloneCount - 1; // Set to the first clone item
                productSlider.style.transition = 'none';
                productSlider.style.transform = `translateX(${-1 * currentIndex * itemWidth}px)`;
            }, 400);
        }

        // Restore transition after resetting
        setTimeout(() => {
            productSlider.style.transition = 'transform 0.4s ease-in-out';
        }, 500);
    }

    // Start the sliding animation
    setInterval(showNextProduct, intervalTime); // Change slide every 3 seconds
});



$(document).ready(function(){
    $('.category-slider .products-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        dots: false,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 3000 // Adjust autoplay speed as needed
    });
});

$(document).ready(function(){
    function filterProducts() {
        var selectedCategories = [];
        var minPrice = parseFloat($('#minPrice').val()) || 0;
        var maxPrice = parseFloat($('#maxPrice').val()) || Infinity;
        $('.category-filter:checked').each(function(){
            selectedCategories.push($(this).val());
        });
        $('#productList .product-item').each(function(){
            var category = $(this).data('category');
            var price = parseFloat($(this).data('price'));
            var categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category.toString());
            var priceMatch = price >= minPrice && price <= maxPrice;
            if (categoryMatch && priceMatch) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $('#price-filter-form').on('submit', function(e){
        e.preventDefault();
        filterProducts();
    });

    $('#category-filter-form').on('submit', function(e){
        e.preventDefault();
        filterProducts();
    });

    $('.category-filter, #minPrice, #maxPrice').on('change', filterProducts);
});



$(document).ready(function(){
    function filterProducts() {
        var selectedCategories = [];
        var minPrice = parseFloat($('#minPrice').val()) || 0;
        var maxPrice = parseFloat($('#maxPrice').val()) || Infinity;
        var productName = $('#productName').val().toLowerCase(); 

        $('.category-filter:checked').each(function(){
            selectedCategories.push($(this).val());
        });

        $('#productList .product-item').each(function(){
            var category = $(this).data('category');
            var price = parseFloat($(this).data('price'));
            var productNameInItem = $(this).find('.product-name a').text().toLowerCase(); // Adjust based on your product name display

            var categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category.toString());
            var priceMatch = price >= minPrice && price <= maxPrice;
            var productNameMatch = productName === '' || productNameInItem.includes(productName);

            if (categoryMatch && priceMatch && productNameMatch) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $('#price-filter-form').on('submit', function(e){
        e.preventDefault();
        filterProducts();
    });

    $('#category-filter-form').on('submit', function(e){
        e.preventDefault();
        filterProducts();
    });

    $('.category-filter, #minPrice, #maxPrice, #productName').on('change keyup', filterProducts);
});
$(document).ready(function() {
    // Apply initial color to each swatch
    $('.color-swatch').each(function() {
        var color = $(this).data('color');
        if (color) {
            $(this).css('background-color', color);
        }
    });

    // Handle color swatch clicks
    $('.color-swatch').on('click', function() {
        // Remove 'selected' class from all swatches
        $('.color-swatch').removeClass('selected');

        // Add 'selected' class to the clicked swatch
        $(this).addClass('selected');

        // Get the new color from the data attribute
        var newColor = $(this).data('color');
        if (newColor) {
            // Optionally update background color
            $('#color-background').css('background-color', newColor);
        }

        // Get the new image URL from the data attribute
        var newImageUrl = $(this).data('image-url');
        if (newImageUrl) {
            // Update the src of the main image
            $('#main-image').attr('src', newImageUrl);
        }

        // Get the new thumbnail images from the data attribute
        var newThumbImages = $(this).data('thumb-images');
        if (newThumbImages) {
            $('#product-imgs').html(newThumbImages);
        }
    });

    // Handle thumbnail clicks
    $('#product-imgs').on('click', '.thumb-image', function() {
        var newSrc = $(this).attr('src');
        $('#main-image').attr('src', newSrc);
    });
});