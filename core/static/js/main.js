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

    /////////////////////////////////////////
    document.addEventListener('DOMContentLoaded', function() {
        // Example: Automatically adjust the height of the carousel items
        function adjustCarouselHeight() {
            var items = document.querySelectorAll('.carousel-item');
            var maxHeight = 0;
    
            items.forEach(function(item) {
                var height = item.offsetHeight;
                if (height > maxHeight) {
                    maxHeight = height;
                }
            });
    
            items.forEach(function(item) {
                item.style.height = maxHeight + 'px';
            });
        }
    
        adjustCarouselHeight();
        window.addEventListener('resize', adjustCarouselHeight);
    });


    $(document).ready(function() {
        // Handle pagination link clicks
        $(document).on('click', '.store-pagination a', function(e) {
            e.preventDefault(); // Prevent the default link behavior
    
            var url = $(this).attr('href'); // Get the URL from the clicked link
    
            $.ajax({
                url: url,
                type: 'GET',
                success: function(data) {
                    // Update the product list and pagination controls
                    $('#productList').html($(data).find('#productList').html());
                    $('.store-pagination').html($(data).find('.store-pagination').html());
                },
                error: function(xhr, status, error) {
                    console.error('AJAX Error:', status, error);
                }
            });
        });
    
        // Optionally handle filter form submission via AJAX if needed
        $('#price-filter-form, #product-name-filter-form').on('submit', function(e) {
            e.preventDefault(); // Prevent the default form submission
    
            var form = $(this);
            var url = form.attr('action');
            var data = form.serialize();
    
            $.ajax({
                url: url,
                type: 'GET', // Assuming you want to use GET for filtering
                data: data,
                success: function(data) {
                    // Update the product list and pagination controls after filtering
                    $('#productList').html($(data).find('#productList').html());
                    $('.store-pagination').html($(data).find('.store-pagination').html());
                },
                error: function(xhr, status, error) {
                    console.error('AJAX Error:', status, error);
                }
            });
        });
    });


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
