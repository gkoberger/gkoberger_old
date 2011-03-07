$(function(){
    if($('#detect_mobile').is(':hidden')) {
        $('body').addClass('mobile');
    } else {
        $('body').addClass('screen');
    }

    if(typeof initBoth == 'function') {
      initBoth();
    }

    if($('body').hasClass('.mobile')) {
      if(typeof initMobile == 'function') {
        initMobile();
      }
    } else {
      if(typeof initScreen == 'function') {
        initScreen();
      }
    }

    if($('#notebook').length > 0) {
      initNotepad();
    }
});


function initNotepad() {

  // TODO: Optimize this!!
  function scrollSidebar(instant){
    var top_offset = $(window).scrollTop();

    instant = (instant == true);

    $('.note').each(function(){
      if($(this).find('.sidebar').offset()['top'] < top_offset || $(this).find('.sidebar').offset()['top'] > 0) {
        var newscroll = top_offset - $(this).find('.sidebar').offset()['top'];

        if(newscroll + $(this).find('.sidebar_scroll').outerHeight() > $(this).find('.text').outerHeight()) {
          newscroll = $(this).find('.text').outerHeight() - $(this).find('.sidebar_scroll').outerHeight();
        }

        if(newscroll < 0) {
          newscroll = 0;
        } else {
          $(this).find('.sidebar .title').show();
        }

        var $sidebar_scroll = $(this).find('.sidebar_scroll');

        var speed = instant ? 0 : 'slow';
        $(this).find('.sidebar_scroll').animate({'top': newscroll}, speed, function(){
          if(newscroll == 0) {
            $sidebar_scroll.find('.title').hide();
          }
        });
      }
    });

  }

  scrollSidebar(true);
  $(document).scroll(debounce(scrollSidebar, 500));
}


/* Created by Potch
 * http://potch.me/8/updates_to_truncation_script */

function debounce(fn, ms, ctxt) {
    var ctx = ctxt || window;
    var it, to, del = ms, fun = fn;
    return function () {
        var args = arguments;
        if (!it) {
            it = setInterval(function () {
                fun.apply(ctx, args);
            },del);
        }
        clearTimeout(to);
        to = setTimeout(function() {
            clearInterval(it);
            it = false;
        },del);
    };
}

