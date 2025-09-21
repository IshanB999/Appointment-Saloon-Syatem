/**
 * Created by Sushant Gauchan
 * Email : sushant.gauchan11@gmail.com
 */

var $ = jQuery;
var winWidth = $(window).width();

$(document).ready(function () {
    sliderInit();
    navInit();
    addClassInit();

    setTimeout(function(){
        $('.common-banner-section').addClass('visible');
    }, 350);

    jQuery(window).scroll(function () {
        var winHeight = jQuery(window).height();
        var offset = 0.5;
        var scrollTop = jQuery(window).scrollTop();
        var visibleArea = scrollTop + (winHeight * offset);

        jQuery('.animation-area').each(function () {
            if(jQuery(this).offset().top < visibleArea) {
                jQuery(this).find('.ani-fade-top').addClass('normal');
            }
        });
    });
});

if(winWidth >= 767){
    document.addEventListener("DOMContentLoaded", function () {
        const lenis = new Lenis();
        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
    });
}

/*------------------------------- Functions Starts -------------------------------*/
function sliderInit() {
    $('.common-banner-section .banner-slider').slick({
        arrows: true,
        dots: false,
        speed: 500,
        autoplay: false,
        pauseOnHover: false,
        fade: true,
        cssEase: 'linear',
        slidesToShow: 1,
        slidesToScroll: 1,
    });

    $('.common-instagram-section .instagram-container').slick({
        arrows: false,
        dots: false,
        speed: 500,
        autoplay: true,
        pauseOnHover: false,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    arrows: false,
                    dots: false,
                }
            },
        ]
    });
/*    $('.product-gallery-slider').slick({
        asNavFor: '.product-gallery-nav'
        arrows: false,
        fade: true,
        slidesToShow: 1,
        slidesToScroll: 1,
    });

    $('.product-gallery-nav').slick({
        asNavFor: '.product-gallery-slider',
        dots: false,
        arrows: false,
        focusOnSelect: true,
        slidesToShow: 5,
        slidesToScroll: 5,
        responsive: [
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
        ]
    });*/

}

function navInit() {
    var scrollTop = 0;
    var lastScrollTop = 0;

    jQuery(window).scroll(function(){
        scrollTop = jQuery(window).scrollTop();
        if (scrollTop >= 550) {
            jQuery('#header-wrapper-slide').addClass('nav-scroll');
        } else if (scrollTop < 550) {
            jQuery('#header-wrapper-slide').removeClass('nav-scroll');
        }
        lastScrollTop = scrollTop;
    });

    $('.common-toggle.type-menu').click(function (){
        $('body').addClass('body-height');
        $('body').toggleClass('menu-open');
    });
    $('.common-toggle.type-menu.type-close').click(function (){
        $('body').removeClass('body-height');
        $('body').removeClass('menu-open');
    });
}

function addClassInit() {

}

/*-------------------------------- Functions Ends --------------------------------*/
