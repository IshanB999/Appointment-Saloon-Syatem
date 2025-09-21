/**
 * Created by Sushant Gauchan
 * Email : sushant.gauchan11@gmail.com
 */


var winWidth = $(window).width();

$(document).ready(function () {
    navInit();
    tableInit();
    addClassInit();


    $('.select2Init').select2();

    $('.comma_separated').on('keyup',function(){
        updateTextView($(this));
    });
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});

/*------------------------------- Functions Starts -------------------------------*/

function updateTextView(_obj){
    var num = getNumber(_obj.val());
    if(num==0){
        _obj.val('');
    }else{
        _obj.val(num.toLocaleString());
    }
}
function getNumber(_str){
    var arr = _str.split('');
    var out = new Array();
    for(var cnt=0;cnt<arr.length;cnt++){
        if(isNaN(arr[cnt])==false){
            out.push(arr[cnt]);
        }
    }
    return Number(out.join(''));
}

function navInit() {
    if(winWidth <= 991){
        $('.has-sub-menu > a').click(function (e) {
            e.preventDefault();
            if($(this).parents('li').hasClass('menu-active')){
                $('.has-sub-menu').removeClass('menu-active');
                $(this).parents('li').removeClass('menu-active');
            }else{
                $('.has-sub-menu').removeClass('menu-active');
                $(this).parents('li').addClass('menu-active');
            }
        });
    }

    if(winWidth <= 767){
        $('.common-header-section .has-drop-down > a').click(function (e) {
            e.preventDefault();
            if($(this).parents('li').hasClass('menu-active')){
                $('.has-sub-menu').removeClass('menu-active');
                $(this).parents('li').removeClass('menu-active');
            }else{
                $('.has-sub-menu').removeClass('menu-active');
                $(this).parents('li').addClass('menu-active');
            }
        });

    }
}

function tableInit() {
    /*$('#custom-table').DataTable();*/
}

function addClassInit() {
    $('.password-toggle').click(function (e){
        var pass = $(this).parent().children('input');
        if (pass.attr('type') === "password") {
            pass.prop('type', 'text');
            $(this).parent().addClass('visible');
        } else {
            pass.prop('type', 'password');
            $(this).parent().removeClass('visible');
        }
    });

    $('.menu-toggle').click(function (e){
        $('body').addClass('menu-open');
    });
    $('.contact-toggle').click(function (e){
        $('.common-side-drawer').addClass('open');
    });
    $('.co-btn.type-toggle').click(function (e){
        $('.co-btn.type-toggle').toggleClass('active')
        $('.common-table .drop-form-container').toggleClass('open');
    });
    $('.drawer-toggle').click(function (e){
        $('#side-drawer').addClass('open');
    });
    $('.bottom-drawer-toggle').click(function () {
        $('.common-mobile-drawer').addClass('open');
    });


    var $triggerClass;
    $('.common-drawer-trigger').click(function (e){
        $('.common-side-drawer').removeClass('open');
        $triggerClass = $(this).attr("id");
        $('#drawer-'+$triggerClass).addClass('open');
        /*$('.common-side-drawer').*/
    });

    $('.menu-toggle, .contact-toggle, .common-drawer-trigger, .drawer-toggle, .bottom-drawer-toggle').click(function (e){
        $('body').addClass('overlay-visible');
    });
    $('.common-overlay, .common-toggle.type-close').click(function (e){
        $('body').removeClass('overlay-visible menu-open');
        $('.common-mobile-drawer').removeClass('open');
        $('.common-side-drawer').removeClass('open');
        $('#side-drawer').removeClass('open');
    });
}


/*-------------------------------- Functions Ends --------------------------------*/
