$(function(){
    if($('#detect_mobile').is(':hidden')) {
        $('body').addClass('mobile');
    } else {
        $('body').addClass('screen');
    }
    
    initBoth();
    if($('body').hasClass('.mobile')) {
        initMobile();
    } else {
        initScreen();
    }
});